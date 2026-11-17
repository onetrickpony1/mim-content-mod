"""Own invisible desktop for the client tests, so a test window never appears on your screens.

A nested `kwin_wayland --virtual` (KDE) on a private D-Bus without portal services, with Xwayland, on its own
socket and helper folder. Linux with KDE's kwin only.

    python3 test_display.py start   -> prints the env (JSON) for the test client
    python3 test_display.py stop
"""
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

SOCKET = "mimcontent-test-wl"
RUN = Path(os.environ.get("XDG_RUNTIME_DIR", "/tmp")) / "mimcontent-test"
STATE = RUN / "state.json"
LOG = Path(__file__).resolve().parent.parent / "mod" / "build" / "test_display.log"


def _alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def _bus_config():
    svc = RUN / "dbus-services"
    svc.mkdir(exist_ok=True)
    for old in svc.iterdir():
        old.unlink()
    for d in (Path("/usr/share/dbus-1/services"), Path.home() / ".local/share/dbus-1/services"):
        for f in sorted(d.glob("*.service")) if d.is_dir() else ():
            if "portal" not in f.name.lower() and not (svc / f.name).exists():
                (svc / f.name).symlink_to(f)
    conf = RUN / "dbus-session.conf"
    conf.write_text(
        '<!DOCTYPE busconfig PUBLIC "-//freedesktop//DTD D-Bus Bus Configuration 1.0//EN"\n'
        ' "http://www.freedesktop.org/standards/dbus/1.0/busconfig.dtd">\n'
        "<busconfig>\n  <type>session</type>\n  <keep_umask/>\n  <listen>unix:tmpdir=/tmp</listen>\n"
        "  <auth>EXTERNAL</auth>\n"
        f"  <servicedir>{svc}</servicedir>\n"
        '  <policy context="default">\n    <allow send_destination="*" eavesdrop="true"/>\n'
        '    <allow eavesdrop="true"/>\n    <allow own="*"/>\n  </policy>\n</busconfig>\n')
    return conf


def start(timeout=40):
    RUN.mkdir(parents=True, exist_ok=True)
    try:
        st = json.loads(STATE.read_text())
        if _alive(st["pid"]):
            return st["env"]
    except (OSError, ValueError, KeyError):
        pass
    envfile = RUN / "display.env"
    envfile.unlink(missing_ok=True)
    for stale in (RUN.parent / SOCKET, RUN.parent / f"{SOCKET}.lock"):
        stale.unlink(missing_ok=True)
    helper = RUN / "hold.sh"
    helper.write_text('#!/bin/sh\nprintf \'{"DISPLAY": "%s", "WAYLAND_DISPLAY": "%s"}\' '
                      f'"$DISPLAY" "$WAYLAND_DISPLAY" > "{envfile}.tmp" && mv "{envfile}.tmp" "{envfile}"\n'
                      'exec sleep infinity\n')
    helper.chmod(0o755)
    conf = _bus_config()
    env = {k: v for k, v in os.environ.items() if k not in ("DISPLAY", "WAYLAND_DISPLAY")}
    with open(LOG, "a") as log:
        p = subprocess.Popen(["dbus-run-session", f"--config-file={conf}", "--", "kwin_wayland", "--virtual", "--xwayland",
                              "--width", "1600", "--height", "900", "--socket", SOCKET, str(helper)],
                             env=env, stdout=log, stderr=log, start_new_session=True)
    end = time.time() + timeout
    while time.time() < end:
        if envfile.exists():
            e = json.loads(envfile.read_text())
            if e.get("DISPLAY"):
                STATE.write_text(json.dumps(dict(pid=p.pid, env=e)))
                return e
        if p.poll() is not None:
            break
        time.sleep(0.5)
    stop(p.pid)
    raise RuntimeError(f"test desktop did not start (see {LOG})")


def stop(pid=None):
    if pid is None:
        try:
            pid = json.loads(STATE.read_text())["pid"]
        except (OSError, ValueError, KeyError):
            pid = None
    if pid and _alive(pid):
        try:
            os.killpg(pid, signal.SIGTERM)
        except OSError:
            pass
        for _ in range(20):
            if not _alive(pid):
                break
            time.sleep(0.25)
        else:
            try:
                os.killpg(pid, signal.SIGKILL)
            except OSError:
                pass
    STATE.unlink(missing_ok=True)


if __name__ == "__main__":
    if sys.argv[1:] == ["stop"]:
        stop()
    else:
        print(json.dumps(start()))
