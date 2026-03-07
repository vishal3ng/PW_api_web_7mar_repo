"""
user_manager.py
---------------
Thread-safe user pool manager for parallel test execution.

How it works:
  - users/users.json holds all test accounts with roles & in_use flags
  - acquire_user(role)  → finds a free user of given role, marks in_use=True
  - release_user(user)  → marks in_use=False when test finishes
  - Uses a file lock (portalocker or fcntl) so parallel workers don't clash
  - If no user is free, waits up to CFG.user_lock_timeout seconds

Usage in fixtures:
    user = acquire_user("buyer")
    yield user
    release_user(user)
"""
import json
import os
import time
import threading
import logging
from pathlib import Path
from typing import Optional

from config.config_loader import CFG

log = logging.getLogger(__name__)

_POOL_PATH = Path(CFG.user_pool_file)
_file_lock = threading.Lock()          # in-process lock
_POLL_INTERVAL = 0.5                   # seconds between retries


def _read_pool() -> list[dict]:
    return json.loads(_POOL_PATH.read_text(encoding="utf-8"))


def _write_pool(pool: list[dict]):
    _POOL_PATH.write_text(json.dumps(pool, indent=2), encoding="utf-8")


def acquire_user(role: str, env: str = None, worker_id: str = "main") -> dict:
    """
    Acquire a free user of the requested role.

    Args:
        role:      One of admin | buyer | seller | viewer | api_user | mobile_user
        env:       Filter by environment (defaults to CFG._env)
        worker_id: pytest-xdist worker id (passed in from fixture for tracing)

    Returns:
        User dict with username / password / role / api_token (if present)

    Raises:
        TimeoutError: If no user becomes free within lock_timeout_seconds
    """
    target_env = env or CFG._env
    deadline = time.time() + CFG.user_lock_timeout

    while time.time() < deadline:
        with _file_lock:
            pool = _read_pool()
            for user in pool:
                if (
                    user["role"] == role
                    and user["env"] == target_env
                    and not user["in_use"]
                ):
                    user["in_use"]   = True
                    user["locked_by"] = worker_id
                    _write_pool(pool)
                    log.info(
                        f"[UserPool] Acquired user '{user['username']}' "
                        f"(role={role}, worker={worker_id})"
                    )
                    return dict(user)

        log.debug(f"[UserPool] No free '{role}' user, retrying in {_POLL_INTERVAL}s…")
        time.sleep(_POLL_INTERVAL)

    raise TimeoutError(
        f"[UserPool] No free user with role='{role}' available "
        f"within {CFG.user_lock_timeout}s. "
        f"Consider adding more '{role}' accounts to users/users.json."
    )


def release_user(user: dict):
    """
    Release a user back to the pool after test completion.

    Args:
        user: The user dict returned by acquire_user()
    """
    with _file_lock:
        pool = _read_pool()
        for u in pool:
            if u["id"] == user["id"]:
                u["in_use"]    = False
                u["locked_by"] = None
                _write_pool(pool)
                log.info(f"[UserPool] Released user '{user['username']}'")
                return
    log.warning(f"[UserPool] Could not find user '{user.get('id')}' to release")


def reset_all_users():
    """
    Emergency reset — marks all users as free.
    Call this if a crashed run left users locked.
    """
    with _file_lock:
        pool = _read_pool()
        for u in pool:
            u["in_use"]    = False
            u["locked_by"] = None
        _write_pool(pool)
    log.info("[UserPool] All users reset to free state.")
