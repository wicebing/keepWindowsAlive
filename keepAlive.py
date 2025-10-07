"""keepAlive.py

Small utility to keep a Windows machine awake. When run it will periodically
call the Windows API to reset the system/display idle timer. Optionally it
can also nudge the mouse by a pixel (uses pyautogui if installed).

Build into a single exe using PyInstaller (see README.md or the
included build_exe.ps1 script).
"""
import sys
import time
import logging
import argparse

try:
    import pyautogui
    _HAS_PYAUTOGUI = True
except Exception:
    _HAS_PYAUTOGUI = False


def prevent_sleep(interval: float = 30.0, nudge: bool = False) -> None:
    """Prevent the system and display from going idle.

    On Windows this calls SetThreadExecutionState periodically which is a
    supported way to inform the OS that the system is in use. On non-Windows
    platforms this function will optionally fall back to small mouse nudges if
    pyautogui is available.
    """
    logging.info("keepAlive started: interval=%s seconds, nudge=%s", interval, nudge)

    # Flags from Windows API
    ES_CONTINUOUS = 0x80000000
    ES_SYSTEM_REQUIRED = 0x00000001
    ES_DISPLAY_REQUIRED = 0x00000002
    flags = ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED

    try:
        while True:
            if sys.platform == "win32":
                # Tell Windows to keep system and display on
                try:
                    ctypes = __import__("ctypes")
                    ctypes.windll.kernel32.SetThreadExecutionState(flags)
                    logging.debug("Called SetThreadExecutionState(flags)")
                except Exception as e:
                    logging.warning("Failed to call SetThreadExecutionState: %s", e)
                    # fall back to mouse nudge if available
                    if _HAS_PYAUTOGUI and nudge:
                        _nudge_mouse()
            else:
                # Non-windows fallback: nudge mouse if requested and available
                if _HAS_PYAUTOGUI and nudge:
                    _nudge_mouse()

            # Also optionally do a tiny mouse movement on Windows if pyautogui exists
            if sys.platform == "win32" and _HAS_PYAUTOGUI and nudge:
                _nudge_mouse()

            time.sleep(interval)
    except KeyboardInterrupt:
        logging.info("Interrupted by user - restoring execution state and exiting")
        if sys.platform == "win32":
            try:
                ctypes = __import__("ctypes")
                # Clear previous request by setting continuous only
                ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
            except Exception:
                pass


def _nudge_mouse() -> None:
    """Move the mouse by one pixel and back to create activity.

    This is a no-op if pyautogui isn't available.
    """
    if not _HAS_PYAUTOGUI:
        return
    try:
        x, y = pyautogui.position()
        # move and move back
        pyautogui.moveTo(x + 1, y)
        pyautogui.moveTo(x, y)
        logging.debug("Nudged mouse at %s,%s", x, y)
    except Exception as e:
        logging.debug("Mouse nudge skipped: %s", e)


def parse_args():
    p = argparse.ArgumentParser(description="Keep Windows awake (prevent sleep/display off)")
    p.add_argument("-i", "--interval", type=float, default=30.0,
                   help="How often (seconds) to reset the idle timer (default: 30)")
    p.add_argument("-n", "--nudge", action="store_true",
                   help="Also perform a tiny mouse nudge (requires pyautogui)")
    p.add_argument("--debug", action="store_true", help="Enable debug logging")
    return p.parse_args()


def main():
    args = parse_args()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO,
                        format="%(asctime)s %(levelname)s: %(message)s")

    if args.nudge and not _HAS_PYAUTOGUI:
        logging.warning("pyautogui not available - mouse nudge disabled")

    prevent_sleep(interval=args.interval, nudge=args.nudge)


if __name__ == "__main__":
    main()