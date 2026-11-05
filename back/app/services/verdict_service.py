def get_llamator_verdict(test_result: dict) -> str:
    if not test_result:
        return "error"
    
    if test_result.get("errors", 0) > 0: return "error"
    if test_result.get("broken", 0) > 0: return "failed"

    return "passed"