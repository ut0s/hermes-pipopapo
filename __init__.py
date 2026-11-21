"""Play a local PipoPapo cue for selected Hermes events."""

import logging
import shutil
import subprocess
import threading

_LOG = logging.getLogger(__name__)


def register(ctx):
    binary = shutil.which("pppp")
    if binary is None:
        _LOG.warning("PipoPapo requires pppp on PATH. Install it with brew install ut0s/pipopapo/pppp.")

    lock = threading.Lock()
    current = None

    def play(text):
        nonlocal current
        if binary is None:
            return
        # Skip overlapping cues and reap the previous command before starting another.
        with lock:
            if current is not None and current.poll() is None:
                return
            try:
                current = subprocess.Popen(
                    [binary, "say", text, "--mode", "drop", "--volume", "55",
                     "--max-duration", "1", "--session", "hermes-marketplace"],
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            except OSError as error:
                _LOG.warning("PipoPapo could not start pppp: %s", error)

    def completed(**_kwargs):
        play("Done")

    def input_required(**_kwargs):
        play("Input needed")

    ctx.register_hook("post_llm_call", completed)
    ctx.register_hook("on_human_input_request", input_required)
