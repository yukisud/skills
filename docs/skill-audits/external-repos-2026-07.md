# 外部リポジトリ調査記録(2026-07)

ユーザー提示の7リポジトリを `skill-vetting` の観点で評価。判定と対応。

| リポジトリ | ⭐ | 正体 | 判定 | 対応 |
|---|---|---|---|---|
| DeusData/codebase-memory-mcp | 32.2k | コード知識グラフMCP(100%ローカル・MIT) | 導入 | connection-setup-ja にランブック追加 |
| mukul975/Anthropic-Cybersecurity-Skills | 25.7k | 817セキュリティスキル(dual-use・Apache2.0) | 防御サブセットのみ | security-operations-ja として防御領域を再構成。攻撃系は除外 |
| lfnovo/open-notebook | 35.6k | NotebookLM OSS版・自己ホスト(MIT) | 併用(別アプリ) | スキル化せず。rag-design-jaの実装例/リサーチ基盤として利用可 |
| stablyai/orca | 20.7k | 複数AIエージェント並列実行IDE(MIT) | 併用(実行環境) | スキル化せず。agent-team-orchestrationの実行環境として利用可 |
| JCodesMore/ai-website-cloner-template | 28.5k | サイト→Next.js再構築テンプレ(MIT) | 条件付き | **自社サイト移行限定**。他者サイトの無断クローンは著作権・不競法リスクで不採用 |
| usestrix/strix | 42.1k | 自律AIペネトレーションテスト(Apache2.0) | 見送り | dual-use(攻撃実行)。「攻撃自動化を入れない」既存方針により不採用。正当な診断は書面許可のある専門業者へ |
| asgeirtj/system_prompts_leaks | 58.4k | 各社システムプロンプト収集(CC0) | 見送り | スキル/業務ツールでない。prompt-engineering-jaが自前の設計論を保持しており不要 |

## 判断の原則(このスキル集の一貫方針)
- **攻撃・侵入・検出回避の自動化は入れない**(strix、Cybersecurity-Skillsの攻撃領域)。防御は入れる
- **スキルでなくアプリ/実行環境**は無理にスキル化せず「使うもの」として案内(open-notebook、orca)
- **法的リスクのある用途**は限定条件を明記(website-cloner=自社移行のみ)
- ローカル完結で業務に効くものは接続(codebase-memory-mcp)

## 導入したもの
- `engineering/connection-setup-ja`: codebase-memory-mcp ランブック
- `engineering/security-operations-ja`(新規): 防御セキュリティ運用

## 再監査条件
codebase-memory-mcp は導入実行時に install.sh とネットワーク挙動を実機で確認する(本記録は公開情報ベースの一次評価)。
