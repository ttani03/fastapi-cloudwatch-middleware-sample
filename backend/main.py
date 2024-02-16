from fastapi import FastAPI, Response
import asyncio
from middleware import CloudWatchMetricsMiddleware

app = FastAPI()

app.add_middleware(CloudWatchMetricsMiddleware)

def set_status_code(response: Response, code: int):
    if not 100 <= code <= 599:
        code = 400
    response.status_code = code

@app.get("/{color}")
async def read_color(color: str, code: int = 200, delay: int = 1000, response: Response = None):
    set_status_code(response, code)
    await asyncio.sleep(delay / 1000)
    return {"api": f"/{color}", "code": code, "delay": delay}
