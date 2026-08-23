# 外部ソース調査記録・第2弾(2026-07)

X投稿2件(アンチスロップ10選 / AIエージェント6リポジトリ)を評価。

## アンチスロップ10選(juampitech)
stop-slop, no-ai-slop, humanizer(×2), unslop, slopbeth, deslop, anti-slop, humanize, anti-ai-slop-writing

**判定: 全て `marketing/ja-humanizer` でカバー済み**(英語向けAI文体除去の同種スキル群)。日本語では自作版が優位。
- 取り込んだ差分: 検出ツール(slopbeth)発想の**公開前AI臭スコアリング(検出ゲート)**を ja-humanizer に追加。英語コンテンツのレビューにも読み替え適用可と明記。
- 新規スキルは作らない(10本とも重複)。

## AIエージェント6リポジトリ(robiartec)
| # | リポジトリ | 判定 |
|---|---|---|
| 1 | Graft(Claude Code高速化・低コスト化) | ツール/最適化レイヤー。スキルでない。効果は要実測、導入するなら別途検証 |
| 2 | Agency agents(232サブエージェント/16分野) | 大半が汎用英語エージェント。当リポジトリの55スキルと重複領域が多く、丸ごと導入はノイズ増。必要分野が出たら個別に監査 |
| 3 | Codebase memory mcp | **導入済み**(connection-setup-ja、external-repos-2026-07.md) |
| 4 | OpenMontage(動画制作パイプライン) | **採用** → creative/video-creation-ja として methodology を新設(既存の空白=動画を埋める) |
| 5 | Agent-Reach(ネット閲覧・X/Reddit/YouTube/GitHub検索) | ツール/MCP。導入するなら connection-setup 経由+skill-vetting。「無料API」の送信先確認が必須。現時点はWebFetch/WebSearchで代替可のため見送り |
| 6 | Orca(複数エージェント並列管理) | **評価済み**(実行環境。スキル化せず) |

## 導入したもの
- `marketing/ja-humanizer`: 公開前AI臭スコアリング(検出ゲート)を追記
- `creative/video-creation-ja`(新規): マーケ・SNS向け動画制作の工程設計

## 方針の一貫性
- 重複(アンチスロップ、Agency agentsの汎用分)は取り込まず、差分のみ既存強化
- ツール/実行環境(Graft, Agent-Reach, Orca)はスキル化せず、必要時に接続
- 空白(動画)はスキル化
