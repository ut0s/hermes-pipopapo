# PipoPapo for Hermes Agent

PipoPapo plays short electronic cues when Hermes finishes a turn or pauses for a person to answer a question, approve an action, or enter a password. The [PipoPapo CLI](https://ut0s.github.io/pipopapo/) generates and plays each cue on the machine running Hermes.

## Requirements

- Hermes Agent 0.23.3 or later.
- A working audio output on the machine running Hermes.
- PipoPapo CLI 0.1.2 or newer on Hermes's PATH. The published Homebrew build supports macOS.

```sh
brew install ut0s/pipopapo/pppp
hermes plugins install ut0s/hermes-pipopapo --enable
```

Homebrew checks the checksum published in the [official Tap](https://github.com/ut0s/homebrew-pipopapo). Restart the Hermes process or gateway after installing the CLI so it can find `pppp`. If the CLI is missing, Hermes logs an install hint and continues silently.

If you previously used `pppp setup hermes`, remove that integration with `pppp plugin uninstall hermes` before installing this package into the same Hermes profile. Both use the plugin name `pipopapo`.

The plugin registers `post_llm_call` and `on_human_input_request`. Each hook starts a short cue and returns immediately. If a cue is already playing, the next cue is skipped.

## Privacy and execution

The plugin runs the separately installed `pppp say` as a short-lived local subprocess with fixed text (`Done` or `Input needed`), a volume of 55%, and a one-second playback limit. `pppp` uses its normal local playback lock and audio device. The plugin ships only Python source and metadata. It ignores hook payloads, makes no network requests, stores no credentials or telemetry, and never approves or changes an agent action.
