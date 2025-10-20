from common.llm_client import query_llm
from common.prompt_templates import L1_PROMPT
from common.utils import log

def handle_l1(query: str):
    log("L1", f"Received query: {query}")
    resp = query_llm(L1_PROMPT + f"\nUser: {query}\nAnswer:")
    if "ESCALATE" in resp.upper():
        log("L1", "Escalating to L2")
        return {"agent": "L1", "status": "escalate", "response": "Escalating to L2"}
    return {"agent": "L1", "status": "resolved", "response": resp}
