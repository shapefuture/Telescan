"""
Deployment orchestration script for Telegram Insight Agent.
"""

import subprocess
import logging
from typing import List

logger = logging.getLogger("telegram_insight_agent.scripts.deploy")

def run_command(cmd: List[str]) -> int:
    """
    Run a shell command, logging output and errors.

    Args:
        cmd: List of command arguments.

    Returns:
        The command's return code.
    """
    logger.info(f"Running command: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        logger.info(f"stdout: {result.stdout}")
        if result.stderr:
            logger.warning(f"stderr: {result.stderr}")
        logger.info(f"Command exited with code {result.returncode}")
        return result.returncode
    except Exception as e:
        logger.error(f"Command execution failed: {e}")
        return -1

def main() -> None:
    """
    Example: Deploy the app using Fly.io CLI.
    """
    logger.info("Starting deployment")
    ret = run_command(["flyctl", "deploy"])
    if ret == 0:
        logger.info("Deployment succeeded.")
    else:
        logger.error(f"Deployment failed with code {ret}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()

# --- Pytest skeleton ---

"""
def test_run_command_success(monkeypatch):
    from scripts.deploy import run_command
    monkeypatch.setattr("subprocess.run", lambda cmd, **kwargs: type("R", (), {"stdout": "ok", "stderr": "", "returncode": 0})())
    assert run_command(["echo", "hi"]) == 0

def test_run_command_error(monkeypatch):
    from scripts.deploy import run_command
    monkeypatch.setattr("subprocess.run", lambda cmd, **kwargs: (_ for _ in ()).throw(Exception("fail")))
    assert run_command(["fail"]) == -1
"""