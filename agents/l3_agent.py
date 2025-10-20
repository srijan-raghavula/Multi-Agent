from common.llm_client import query_llm
from common.prompt_templates import L3_PROMPT
from common.utils import log

def handle_l3(query: str):
    log("L3", f"Received query: {query}")
    resp = query_llm(L3_PROMPT + f"\nUser: {query}\nAnswer:")
    requires_mcp = "requires_mcp" in resp.lower()
    return {"agent": "L3", "status": "resolved", "response": resp, "requires_mcp": requires_mcp}
