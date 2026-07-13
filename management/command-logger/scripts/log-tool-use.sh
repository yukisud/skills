#!/usr/bin/env bash
# Claude Code PreToolUse hook: ツール実行をJSONLで監査ログに記録する。
# stdinにhookイベントのJSONが渡される。exit 0で実行を許可(記録のみ)。
set -u

AUDIT_DIR="${CLAUDE_PROJECT_DIR:-.}/.claude/audit"
mkdir -p "$AUDIT_DIR"
LOG_FILE="$AUDIT_DIR/tool-use-$(date +%Y%m%d).jsonl"

INPUT="$(cat)"

if command -v jq >/dev/null 2>&1; then
  printf '%s' "$INPUT" | jq -c \
    --arg ts "$(date +%Y-%m-%dT%H:%M:%S%z)" \
    '{ts: $ts, session_id: (.session_id // null), tool: (.tool_name // null), input: (.tool_input // null), cwd: (.cwd // null)}' \
    >> "$LOG_FILE"
else
  # jqがない環境では生イベントをそのまま1行で保存する
  printf '{"ts":"%s","raw":%s}\n' "$(date +%Y-%m-%dT%H:%M:%S%z)" "$INPUT" >> "$LOG_FILE"
fi

exit 0
