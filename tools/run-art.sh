#!/usr/bin/env bash
# Builds the mod and takes the art screenshots in-game on an invisible, silent desktop.
#   tools/run-art.sh                -> mod/build/smoke-run/screenshots/*.png
#   ART_RUN=fish tools/run-art.sh   -> .art-runs/fish/build/smoke-run/screenshots/*.png
# With ART_RUN set, the run works on its own copy of mod/ (the current files, copied at the start) with its own
# desktop, so several runs can go at once. Each needs ~6 GB of free memory; a run waits until there is enough.
# Needs: Java 25 (env.sh), KDE's kwin_wayland.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
NEED_KB=6000000
PROJECT="$ROOT/mod"
if [ -n "${ART_RUN:-}" ]; then
	case "$ART_RUN" in *[!a-z0-9_-]*) echo "ART_RUN: use a-z, 0-9, - and _ only"; exit 2;; esac
	PROJECT="$ROOT/.art-runs/$ART_RUN"
	mkdir -p "$PROJECT"
	# refresh everything except the copy's own build and Gradle folders (kept, so later builds are quicker)
	find "$PROJECT" -mindepth 1 -maxdepth 1 ! -name build ! -name .gradle -exec rm -rf {} +
	for f in "$ROOT/mod/"* "$ROOT/mod/".[!.]*; do
		case "$(basename "$f")" in build|.gradle|run|'.[!.]*') ;; *) cp -a "$f" "$PROJECT/" ;; esac
	done
fi
export ART_RUN="${ART_RUN:-}"
# wait for memory, with a random start so parallel runs don't all pass the check at the same moment
sleep "$(( RANDOM % 10 ))"
until [ "$(awk '/MemAvailable/{print $2}' /proc/meminfo)" -gt "$NEED_KB" ]; do
	echo "waiting for memory..."; sleep 15
done
mkdir -p "$ROOT/mod/build" "$PROJECT/build"
display="$(python3 "$ROOT/tools/test_display.py" start)"
trap 'python3 "$ROOT/tools/test_display.py" stop >/dev/null 2>&1 || true' EXIT
export DISPLAY="$(python3 -c 'import json,sys; print(json.loads(sys.argv[1])["DISPLAY"])' "$display")"
export WAYLAND_DISPLAY="$(python3 -c 'import json,sys; print(json.loads(sys.argv[1])["WAYLAND_DISPLAY"])' "$display")"
export __NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia __VK_LAYER_NV_optimus=NVIDIA_only
export ALSOFT_DRIVERS=null
if [ -f "$ROOT/env.sh" ]; then source "$ROOT/env.sh"; fi
cd "$PROJECT"
rm -rf build/smoke-run/saves build/smoke-run/screenshots
bash ./gradlew build runSmoke --console=plain "$@" > build/smoke.log 2>&1 && status=0 || status=$?
grep -E "\[smoke\]|AssertionError|Exception|error:|BUILD|FAILED" build/smoke.log | grep -v '	at ' | cut -c1-300 | tail -40 || true
echo "screenshots: ${PROJECT#$ROOT/}/build/smoke-run/screenshots"
echo "log: ${PROJECT#$ROOT/}/build/smoke.log (exit $status)"
exit $status
