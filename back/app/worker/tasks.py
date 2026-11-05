import asyncio
import json
from sqlalchemy import select
from confluent_kafka import Producer

from worker.celery import celery_app
from pentest.test_prompt_injection import PromptInjectionTests
from database.database import AsyncSessionLocal, engine
from models.reports import TestReport
from exceptions import ReportException
from services.crypt_service import decrypt_secret
from services.build_result import build_report_result, build_full_report
from config import KAFKA_BOOTSTRAP_SERVER as kafka_server
from config import KAFKA_PRODUCER_TOPIC as kafka_producer_topic

def get_kafka_producer():
    return Producer({
        'bootstrap.servers': kafka_server
    })

def send_result_to_core(
        attack_id: str, 
        result: dict,
        error: str | None,
        task_id: str | None
):
    producer = get_kafka_producer()

    message = {
        "attack_id": attack_id,
        "result": result,
        "error": error
    }

    if task_id:
        message["task_id"] = task_id

    producer.produce(
        topic = kafka_producer_topic, 
        value = json.dumps(message).encode('utf-8')
    )
    producer.flush()

async def run_custom_llm_test_async(report_id):
    try:
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(TestReport).where(TestReport.id == report_id)
            )
            report = result.scalar_one_or_none()

            if report is None:
                raise ReportException(
                    message="Report is not found",
                    status_code=404
                )
            
            attack_id = report.attack_id
            task_id = report.task_id
            api_key_encrypted = report.target_auth_token_encrypted
            base_url = report.target_url
            model_name = report.target_model

            settings = [
                (name, params)
                for name, params in (report.test_settings or [])
            ]

            report.status = "running"
            report.test_settings = settings

            await db.commit()
            await db.refresh(report)
        
        test_data = PromptInjectionTests(
            attack_id=attack_id,
            api_key=decrypt_secret(api_key_encrypted),
            base_url=base_url,
            model=model_name,
            custom_basic_tests=settings if settings else None
            )
        
        test_result = await test_data.prompt_injection()

        if not test_result:
            raise ReportException(
                message="LLM test finished without results. Check model_url/api_key/model_name.",
                status_code=422
                )
        
        results = test_result.get("results", {})
        actual_settings = test_result.get("applied_settings", [])

        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(TestReport).where(TestReport.id == report_id)
            )

            report = result.scalar_one_or_none()
            
            report.result = build_report_result(results)
            report.test_settings = actual_settings
            report.status = "completed"
            report.full_report = build_full_report(attack_id = attack_id)

            await db.commit()
            await db.refresh(report)

        result_payload = {"status": "completed"}

        send_result_to_core(
            attack_id=attack_id,
            result=result_payload,
            error=None,
            task_id=task_id
        )
    
    except Exception as exc:
        error_msg = str(getattr(exc, 'message', exc))

        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(TestReport).where(TestReport.id == report_id)
            )
            report = result.scalar_one_or_none()

            if report is not None:
                attack_id = attack_id or report.attack_id
                report.result = {"status": "failed", "error_details": {"message": error_msg}}
                report.status = "failed"
                report.error = error_msg
                await db.commit()
                await db.refresh(report)

            if attack_id:
                send_result_to_core(
                    attack_id=attack_id,
                    result={"status": "failed", "error_details": {"message": error_msg}},
                    error=error_msg,
                    task_id=None
                )

async def run_custom_llm_test_entrypoint(report_id: int):
    try:
        await run_custom_llm_test_async(report_id)
    finally:
        await engine.dispose()


@celery_app.task(
    name="run_custom_llm_test",
    rate_limit="10/m"
)
def run_custom_llm_test(report_id: int):
    asyncio.run(run_custom_llm_test_entrypoint(report_id))