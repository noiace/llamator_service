from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException, Request
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.database import get_db
from models.reports import TestReport

report_router = APIRouter()

class OutTestReport(BaseModel):
    pass

@report_router.get('/get_test_report', tags = ['report'], response_model = list[OutTestReport])
async def get_test_report(report_id: str, db: AsyncSession = Depends(get_db)):
    if report_id is None:
        raise HTTPException(
            status_code=428,
            detail=''
        )
    
    result = await db.execute(
        select(TestReport)
        .where(id == TestReport.id)
    )

    report = result.scalar_one_or_none()

    return OutTestReport(
        
    )
