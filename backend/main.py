import asyncio

import uvicorn

from core.application import create_app

app = asyncio.run(create_app())


if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8000, log_level="info")
