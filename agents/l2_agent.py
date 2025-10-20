from common.llm_client import query_llm
from common.prompt_templates import L2_PROMPT
from common.utils import log

def handle_l2(query: str):
    log("L2", f"Received query: {query}")
    resp = query_llm(L2_PROMPT + f"\nUser: {query}\nAnswer:")
    if "ESCALATE" in resp.upper():
        log("L2", "Escalating to L3")
        return {"agent": "L2", "status": "escalate", "response": "Escalating to L3"}
    return {"agent": "L2", "status": "resolved", "response": resp}
