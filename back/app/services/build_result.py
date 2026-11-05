from services.verdict_service import get_llamator_verdict

def build_report_result(result: dict) -> dict:
    if result is None:
        return {"tests": [], "error": "empty_result"} 
    
    if not result:
        return {
            "tests": [],
            "error": "empty_result"
        }
    
    tests = []
    
    for test_name, test_result in result.items():
        tests.append({
            "test_name": test_name,
            "broken": test_result.get("broken", 0),
            "resilient": test_result.get("resilient", 0),
            "errors": test_result.get("errors", 0),
            "verdict": get_llamator_verdict(test_result),
        })

    return {
        "tests": tests
    }

def build_full_report(attack_id: str):
    pass