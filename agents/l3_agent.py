from common.llm_client import query_llm
from common.prompt_templates import L3_PROMPT
from common.utils import log
import requests

def handle_l3(query: str):
    log("L3", f"Received query: {query}")
    resp = query_llm(L3_PROMPT + f"\nUser: {query}\nAnswer:")
    requires_mcp = "requires_mcp" in resp.lower()
    if "requires_mcp" in resp.lower() or "account" in query.lower() or "billing" in query.lower():
        log("L3", "Routing to MCP tool...")
        try:
            mcp_resp = requests.post(
                "http://localhost:8080/handle_l3",  # adjust route name to match your MCP server
                json={"query": query},
                timeout=15
            )
            return {
                "agent": "L3",
                "status": "resolved",
                "response": mcp_resp.text,
                "requires_mcp": True
            }
        except Exception as e:
            return {
                "agent": "L3",
                "status": "error",
                "response": f"MCP call failed: {e}",
                "requires_mcp": True
            }

    # fallback: normal LLM route
    return {"agent": "L3", "status": "resolved", "response": resp, "requires_mcp": requires_mcp}
