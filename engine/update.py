"""Is this copy of ExamsHelp behind the published one?

The check is deliberately timid. It reads one small file over HTTPS, at most
once a day, on a background thread, and every failure is silent. A machine with
no network must not pay for this at startup, and a practice harness has no
business complaining that GitHub was unreachable.

Nothing in the UI ever waits on it: the answer is cached in its own small file
and shown on the *next* start. `version` is the one exception -- somebody who
types it is asking to wait, so that path checks synchronously.

The cache is a separate file rather than a corner of the state file on purpose:
the background thread would otherwise be writing the same JSON the main thread
saves progress into, and the loser of that race is the student's progress.
"""

import json
import os
import re
import threading
import time
import urllib.request

from engine.version import VERSION

SOURCE_URL = (
    "https://raw.githubusercontent.com/wxsonz/w_examshelp/main/engine/version.py"
)
CHECK_INTERVAL = 24 * 60 * 60
TIMEOUT = 4

_VERSION_LINE = re.compile(r'^VERSION\s*=\s*"([^"]+)"', re.M)


def disabled():
    """EXAMSHELP_NO_UPDATE_CHECK=1 turns the whole thing off, network included."""
    return os.environ.get("EXAMSHELP_NO_UPDATE_CHECK", "") not in ("", "0")


def parse(version):
    """"v0.6.0" -> (0, 6, 0). Anything unparseable sorts lowest."""
    numbers = re.findall(r"\d+", version or "")
    return tuple(int(n) for n in numbers[:3]) or (0,)


def is_newer(candidate, current=VERSION):
    return parse(candidate) > parse(current)


def cache_path(state_file):
    return os.path.join(
        os.path.dirname(os.path.abspath(state_file)), ".examshelp_update.json"
    )


def _read_cache(state_file):
    try:
        with open(cache_path(state_file), encoding="utf-8") as f:
            record = json.load(f)
        return record if isinstance(record, dict) else {}
    except Exception:
        return {}


def _write_cache(state_file, latest):
    record = {"latest": latest, "checked_at": time.time()}
    path = cache_path(state_file)
    temporary = f"{path}.tmp"
    try:
        with open(temporary, "w", encoding="utf-8") as f:
            json.dump(record, f)
        os.replace(temporary, path)
    except Exception:
        pass


def fetch_latest(url=None, timeout=TIMEOUT):
    """The published version string, or None if we could not find out.

    The default is read here rather than bound at import, so a test can point
    SOURCE_URL somewhere it controls and have it actually take effect.
    """
    if disabled():
        return None
    try:
        with urllib.request.urlopen(url or SOURCE_URL, timeout=timeout) as response:
            body = response.read(4096).decode("utf-8", "replace")
    except Exception:
        return None
    found = _VERSION_LINE.search(body)
    return found.group(1) if found else None


def pending(state_file):
    """A newer version we have already heard about, or None. Never blocks."""
    latest = _read_cache(state_file).get("latest")
    return latest if latest and is_newer(latest) else None


def refresh_later(state_file):
    """Start the daily check in the background. Returns the thread, or None."""
    if disabled():
        return None
    if time.time() - _read_cache(state_file).get("checked_at", 0) < CHECK_INTERVAL:
        return None

    def run():
        latest = fetch_latest()
        if latest:
            _write_cache(state_file, latest)

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    return thread


def check_now(state_file):
    """Check synchronously, for `version`. Returns the published version or None."""
    latest = fetch_latest()
    if latest:
        _write_cache(state_file, latest)
    return latest
