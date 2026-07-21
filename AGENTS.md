# Codex runtime safety

- Do not stream sustained or verbose subprocess output into the chat. This is especially important for `llama-cli --verbose`, model conversion, training, and long test runs.
- Redirect stdout and stderr from noisy commands to a log file. Report process state while the command runs, then read at most the last 80 lines after it exits.
- Use `protocols/run_llama_cli_safely.ps1` for `llama-cli` checks. Keep any direct tool output below 4,000 tokens.
- Do not resume the large historical rollouts in `codex-chat-sessions/sessions`. Start a fresh thread and recover state from repository files or a concise handoff instead.
- Never stop, kill, restart, or broadly clean up `codex`, `codex-code-mode-host`, `node`, or their process trees from inside a Codex session. These processes and launchers may own other live sessions or shared runtime channels.
- If Codex itself needs a restart, preserve the session data, explain why, and ask the user to restart Codex outside the active session. Limit automated process cleanup to a workload process launched by the current tool call whose identity and ancestry have been verified.
- Treat Codex SQLite databases, WAL files, session rollouts, caches, and runtime state as read-only while Codex is running. Do not delete, truncate, vacuum, migrate, or replace them as a repair step from an active session.
