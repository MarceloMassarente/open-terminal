import asyncio
import json
from typing import Optional

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

app = FastAPI(title="open-terminal")


class ExecRequest(BaseModel):
    command: str
    timeout: Optional[float] = 30.0


class ExecResponse(BaseModel):
    exit_code: int
    stdout: str
    stderr: str


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/execute")
async def execute(req: ExecRequest, stream: bool = False):
    if stream:
        return _stream_response(req)

    try:
        proc = await asyncio.create_subprocess_shell(
            req.command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(), timeout=req.timeout
        )
    except asyncio.TimeoutError:
        proc.kill()
        await proc.communicate()
        return ExecResponse(
            exit_code=-1,
            stdout="",
            stderr=f"Command timed out after {req.timeout}s",
        )

    return ExecResponse(
        exit_code=proc.returncode or 0,
        stdout=stdout.decode(errors="replace"),
        stderr=stderr.decode(errors="replace"),
    )


def _stream_response(req: ExecRequest):
    async def generate():
        proc = await asyncio.create_subprocess_shell(
            req.command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        async def read_stream(s, label):
            async for line in s:
                yield json.dumps({"type": label, "data": line.decode(errors="replace")}) + "\n"

        async for chunk in read_stream(proc.stdout, "stdout"):
            yield chunk
        async for chunk in read_stream(proc.stderr, "stderr"):
            yield chunk

        await proc.wait()
        yield json.dumps({"type": "exit", "data": proc.returncode}) + "\n"

    return StreamingResponse(generate(), media_type="application/x-ndjson")
