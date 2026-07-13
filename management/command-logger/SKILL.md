---
name: command-logger
description: Claude Codeの全ツール実行(Bashコマンド・ファイル編集等)を監査ログ(JSONL)に記録するhooks設定を導入・運用するスキル。エージェントに実行権限を渡す前の監査基盤づくり、ログの調査・集計にも使用。「監査ログ」「コマンドログ」「実行履歴を記録」「command logger」などの依頼で起動。
---

# コマンド監査ロガー

Claude Code の hooks 機能で全ツール実行を JSONL に記録する。エージェントへ実行権限を委譲する場合の前提インフラ。**hooksはClaude自身の判断ではなくハーネスが強制実行するため、記録漏れ・改変が起きない**のがポイント(スキルの指示文で「ログを取ってね」と書くだけでは監査にならない)。

## セットアップ手順

### 1. ログスクリプトの設置

`scripts/log-tool-use.sh` をプロジェクトの `.claude/hooks/` にコピーする(このスキルディレクトリに同梱)。

```bash
mkdir -p .claude/hooks
cp <このスキルのパス>/scripts/log-tool-use.sh .claude/hooks/
chmod +x .claude/hooks/log-tool-use.sh
```

### 2. settings.json への登録

`.claude/settings.json`(チーム共有)または `.claude/settings.local.json`(個人)に追記:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|Write|Edit|NotebookEdit",
        "hooks": [
          { "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/log-tool-use.sh" }
        ]
      }
    ]
  }
}
```

- 全ツールを記録したい場合は `matcher` を `"*"` にする(MCPツール・読み取り系も含まれログ量が増える)。
- ログの既定出力先: `.claude/audit/tool-use-YYYYMMDD.jsonl`(スクリプト内で変更可)。
- `.gitignore` に `.claude/audit/` を追加する(ログにはコマンド引数として機密が混ざりうるため、**リポジトリにコミットしない**)。

### 3. 動作確認

設定後に任意のBashコマンドを1つ実行し、ログファイルに行が追加されることを確認してから運用開始する。

## ログの中身(1行=1イベント)

```json
{"ts":"2026-07-13T10:23:45+09:00","session_id":"...","tool":"Bash","input":{"command":"..."},"cwd":"..."}
```

## 運用・調査レシピ

```bash
# 今日実行された全Bashコマンドを見る
jq -r 'select(.tool=="Bash") | .input.command' .claude/audit/tool-use-$(date +%Y%m%d).jsonl

# 外部送信の痕跡を探す(スキル監査の事後チェック)
grep -E "curl|wget|POST" .claude/audit/*.jsonl

# ツール別の実行回数集計
jq -r .tool .claude/audit/*.jsonl | sort | uniq -c | sort -rn
```

## 運用ルール

- ログは最低90日保持(業務委託でクライアントデータを扱う場合は契約に合わせる)。
- 週次で「外部送信・削除系(`rm`、`git push --force`)・権限変更(`chmod`)」の3パターンを目視レビューする。`engineering/skill-vetting` で導入した外部スキルの事後監査もこのログで行う。
- ログに個人情報・APIキーが記録された場合は該当行をマスキングし、キーはローテーションする。
- ブロック(実行拒否)機能を足したい場合は、このhookをexitコード2で終了させると当該ツール実行を拒否できる。危険コマンドのdenyリストは `update-config` 系の設定(permissions.deny)を第一選択にし、hookでのブロックは補完に留める。
