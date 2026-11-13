import os
import json
import requests
from render import Workflows
from render.workflows import FlowContext

app = Workflows()
BASE = "https://api.poyo.ai"



def call_poyo(method: str, path: str, body: str = "") -> dict:
    headers = {
        "Authorization": f"Bearer {os.environ['POYO_API_KEY']}",
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }
    r = requests.request(
        method.upper(), BASE + path, headers=headers,
        data=body.encode() if body else None, timeout=280,
    )
    try:
        data = r.json()
    except ValueError:
        data = r.text[:20000]
    return {"status": r.status_code, "body": data}


@app.flow(timeout_seconds=600)
def poyo(ctx: FlowContext, method: str, path: str, body: str = "") -> dict:
    return ctx.step("call_poyo", call_poyo, method, path, body)


if __name__ == "__main__":
    app.start()
