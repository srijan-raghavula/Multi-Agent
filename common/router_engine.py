from sentence_transformers import SentenceTransformer, util
import torch

ROUTER_EXAMPLES = [
    {"level": "L1", "text": "How to check my data balance?"},
    {"level": "L1", "text": "I want to recharge my phone."},
    {"level": "L2", "text": "I want a refund for a failed recharge."},
    {"level": "L2", "text": "Please escalate to a manager."},
    {"level": "L3", "text": "Adjust billing for user 12345."},
    {"level": "L3", "text": "Fetch account info for customer Ravi."},
]

class Router:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.examples = ROUTER_EXAMPLES
        self.embeddings = self.model.encode([e["text"] for e in self.examples], convert_to_tensor=True)

    def classify(self, query: str):
        query_emb = self.model.encode(query, convert_to_tensor=True)
        sims = util.cos_sim(query_emb, self.embeddings)[0]
        best_idx = int(torch.argmax(sims))
        best = self.examples[best_idx]
        requires_mcp = best["level"] == "L3"
        return {"level": best["level"], "score": float(sims[best_idx]), "requires_mcp": requires_mcp}
