from .database import SyncSessionLocal
from services.crypt_service import encrypt_secret
from models.reports import TestReport

def create_pending_report(
        attack_data: dict,
):
    encrypted_token = encrypt_secret(attack_data.get("target_auth_token"))

    with SyncSessionLocal() as db:
        new_report = TestReport(
            attack_id=attack_data.get("attack_id"),
            request_id=attack_data.get("request_id"),
            target_model=attack_data.get("target_model"),
            target_url=attack_data.get("target_url"),
            target_auth_token_encrypted=encrypted_token,
            test_settings=attack_data.get("attrs", {})
        )

        db.add(new_report)
        db.commit()
        db.refresh(new_report)
        
        return new_report.id
