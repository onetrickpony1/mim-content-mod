#!/usr/bin/env bash
# Builds the mod and takes the art screenshots in-game on an invisible, silent desktop.
#   tools/run-art.sh     -> mod/build/smoke-run/screenshots/*.png
# Needs: Java 25 (env.sh), KDE's kwin_wayland, ~6 GB of free memory.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
NEED_KB=6000000
until [ "$(awk '/MemAvailable/{print $2}' /proc/meminfo)" -gt "$NEED_KB" ]; do
	echo "waiting for memory..."; sleep 15
done
mkdir -p "$ROOT/mod/build"
display="$(python3 "$ROOT/tools/test_display.py" start)"
trap 'python3 "$ROOT/tools/test_display.py" stop >/dev/null 2>&1 || true' EXIT
export DISPLAY="$(python3 -c 'import json,sys; print(json.loads(sys.argv[1])["DISPLAY"])' "$display")"
export WAYLAND_DISPLAY="$(python3 -c 'import json,sys; print(json.loads(sys.argv[1])["WAYLAND_DISPLAY"])' "$display")"
export __NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia __VK_LAYER_NV_optimus=NVIDIA_only
export ALSOFT_DRIVERS=null
if [ -f "$ROOT/env.sh" ]; then source "$ROOT/env.sh"; fi
cd "$ROOT/mod"
rm -rf build/smoke-run/saves build/smoke-run/screenshots
bash ./gradlew build runSmoke --console=plain "$@" > build/smoke.log 2>&1 && status=0 || status=$?
grep -E "\[smoke\]|AssertionError|Exception|error:|BUILD|FAILED" build/smoke.log | grep -v '	at ' | cut -c1-300 | tail -40 || true
echo "log: mod/build/smoke.log (exit $status)"
exit $status
