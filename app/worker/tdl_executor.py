import asyncio
import json
import logging
import os
from typing import Any, Dict, List

from config import settings

logger = logging.getLogger("telegram_insight_agent.tdl_executor")

class TdlExecutionError(Exception):
    """Raised when tdl subprocess fails or output is invalid."""
    pass

async def execute_tdl_command(args: List[str], timeout_sec: int = 300) -> Dict[str, Any]:
    """
    Executes a tdl CLI command as a subprocess and returns parsed JSON output.

    Args:
        args: Command arguments (e.g. ['chat', 'export', ...])
        timeout_sec: Max seconds to wait for completion.

    Returns:
        Parsed JSON output from tdl.

    Raises:
        TdlExecutionError: On nonzero exit, timeout, or JSON parsing error.
    """
    tdl_bin = "tdl"
    env = os.environ.copy()
    env["TDL_CONFIG_DIR"] = settings.TDL_CONFIG_DIR
    logger.info(f"Executing tdl command: {tdl_bin} {' '.join(args)}")
    try:
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
            logger.error(f"tdl command timed out: {tdl_bin} {' '.join(args)}")
            raise TdlExecutionError(f"tdl command timed out: {' '.join(args)}")

        if proc.returncode != 0:
            logger.error(f"tdl exited with {proc.returncode}: {stderr.decode().strip()}")
            raise TdlExecutionError(f"tdl exited with {proc.returncode}: {stderr.decode().strip()}")

        try:
            result = json.loads(stdout.decode())
            logger.debug(f"tdl command output parsed: {result}")
            return result
        except Exception as e:
            logger.error(f"Failed to parse tdl output: {stdout.decode()} - {e}")
            raise TdlExecutionError(f"Failed to parse tdl output: {e}")
    except Exception as e:
        logger.exception(f"Error running tdl command: {args} - {e}")
        raise

# --- Test skeleton for execute_tdl_command ---

# Place in tests/test_tdl_executor.py

"""
import pytest
import asyncio
from app.worker.tdl_executor import execute_tdl_command, TdlExecutionError

@pytest.mark.asyncio
async def test_execute_tdl_command_success(monkeypatch):
    # monkeypatch asyncio.create_subprocess_exec to return a mock process
    # with .communicate() returning valid JSON
    pass

@pytest.mark.asyncio
async def test_execute_tdl_command_timeout(monkeypatch):
    # Simulate timeout
    pass

@pytest.mark.asyncio
async def test_execute_tdl_command_nonzero_exit(monkeypatch):
    # Simulate nonzero exit code and error output
    pass

@pytest.mark.asyncio
async def test_execute_tdl_command_json_error(monkeypatch):
    # Simulate invalid JSON output
    pass
"""