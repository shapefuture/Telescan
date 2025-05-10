import asyncio
import json
import logging
import os
from config import settings

class TdlExecutionError(Exception):
    pass

async def execute_tdl_command(args: list[str], timeout_sec: int = 300) -> dict:
    # args: list, e.g. ['chat', 'export', '-c', CHAT_ID, '--all', '-o', outpath]
    tdl_bin = "tdl"
    env = os.environ.copy()
    env["TDL_CONFIG_DIR"] = settings.TDL_CONFIG_DIR
    proc = await asyncio.create_subprocess_exec(
        tdl_bin, *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=env
    )
    try:
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout_sec)
    except asyncio.TimeoutError:
        proc.kill()
        raise TdlExecutionError(f"tdl command timed out: {' '.join(args)}")

    if proc.returncode != 0:
        raise TdlExecutionError(f"tdl exited with {proc.returncode}: {stderr.decode().strip()}")

    try:
        result = json.loads(stdout.decode())
        return result
    except Exception as e:
        logging.error(f"Failed to parse tdl output: {stdout.decode()}")
        raise TdlExecutionError(f"Failed to parse tdl output: {e}")