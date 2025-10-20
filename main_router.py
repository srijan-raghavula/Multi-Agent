from fastapi import FastAPI, Request
from agents.l1_agent import handle_l1
from agents.l2_agent import handle_l2
from agents.l3_agent import handle_l3
from common.router_engine import Router
from common.utils import log

app = FastAPI(title="Airtel Support AI System")

router = Router()

@app.post("/query")
async def process(request: Request):
    try:
        data = await request.json()
        query = data.get("query", "")
        log("Router", f"Received: {query}")

        route = router.classify(query)
        level = route["level"]

        # Route to the appropriate agent
        if level == "L1":
            result = handle_l1(query)
            if result["status"] == "escalate":
                result = handle_l2(query)
                if result["status"] == "escalate":
                    result = handle_l3(query)
        elif level == "L2":
            result = handle_l2(query)
            if result["status"] == "escalate":
                result = handle_l3(query)
        else:
            result = handle_l3(query)

        result["route_info"] = route
        log("Router", f"Final result: {result}")
        return result

    except Exception as e:
        log("Router", f"Error processing query: {str(e)}")
        return {"error": str(e)}

@app.get("/health")
def health():
    return {"status": "ok", "router": "embedding", "model": "Gemini"}
