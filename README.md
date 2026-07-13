# skills — 日本環境最適化 業務スキル集

Claude Code / Claude 向けの Agent Skills 集。海外製スキル(marketingskills, marketing-mode, Ryze, agent-team-orchestration ほか)の設計を参考に、**日本の法規制・広告仕様・商習慣・日本語の言語特性**に合わせて再設計したもの。

## 構成

```
marketing/        マーケティング(広告運用・SEO・コピー・レビュー)
engineering/      エンジニアリング(UI設計・スキル監査)
management/       経営・組織運営(AIチーム編成・レポート・監査ログ)
data-science/     データサイエンス(リサーチ・データ突合)
```

### マーケ

| スキル | 役割 | 元ネタ | 日本最適化ポイント |
|---|---|---|---|
| `marketing/google-ads-ja-ops` | 推論 | coreyhaines31/marketingskills | 医療広告ガイドライン、P-Max/入札判断、円建てCPA基準 |
| `marketing/rsa-copywriter-ja` | 実働 | 同上のRSA出力仕様 | 全角15/45文字制限、薬機法・医療広告セルフチェック |
| `marketing/negative-keyword-scanner` | レビュー | Ryze無料スキル集 | 日本語表記ゆれ(ひらがな/カタカナ/漢字)を考慮した除外判定 |
| `marketing/seo-content-scorer-ja` | レビュー | Ryze / kostja94 | 日本語KW配置・共起語・E-E-A-T(YMYL医療)採点 |
| `marketing/ja-humanizer` | レビュー | humanizer | 日本語特有のAI文体兆候(「〜しましょう」連発等)を除去 |
| `marketing/seo-strategy-ja` | 推論 | kostja94/marketing-skills | Technical→On-Page→Content→Off-Pageを日本市場向けに編成 |

### エンジニア

| スキル | 役割 | 元ネタ | 日本最適化ポイント |
|---|---|---|---|
| `engineering/frontend-design-ja` | 推論 | anthropics/frontend-design | 日本語タイポグラフィ(約物・行長・フォントスタック) |
| `engineering/skill-vetting` | レビュー | skill-vetting系 | 導入前のマルウェア・データ流出パターン監査手順 |

### 経営

| スキル | 役割 | 元ネタ | 日本最適化ポイント |
|---|---|---|---|
| `management/agent-team-orchestration-ja` | 推論 | agent-team-orchestration | 稟議・報連相を模したレビュー/引き継ぎ様式 |
| `management/client-report-generator-ja` | 実働 | report-generator | 月次報告書の定型(サマリ→実績→分析→翌月施策) |
| `management/command-logger` | レビュー | command-logger | hooksによる全コマンド監査ログ(JSONL) |

### データサイエンス

| スキル | 役割 | 元ネタ | 日本最適化ポイント |
|---|---|---|---|
| `data-science/seo-research-ja` | 実働 | seo-research | 日本のSERP機能(強調スニペット/ローカルパック)前提の調査手順 |
| `data-science/data-reconciliation` | レビュー | 自作 | Looker Studio定義とAPI生データの突合QA |

## インストール

個人スキルとして使う場合、各スキルディレクトリを `~/.claude/skills/` 配下にコピー:

```bash
cp -r marketing/google-ads-ja-ops ~/.claude/skills/
```

プロジェクトスキルとして使う場合は、対象リポジトリの `.claude/skills/` 配下に配置。

## 最短ルート(広告運用フロー)

まず入れる3点セット:

1. `marketing/google-ads-ja-ops` — 運用判断の頭脳
2. `marketing/negative-keyword-scanner` — 検索語句レポート→除外KWの実務
3. `management/command-logger` — 実行権限を渡す前の監査基盤

## ⚠️ 外部スキル導入時の注意

外部配布スキル(ClawHub等)には悪意あるコードが混入している事例が報告されている。導入前に必ず `engineering/skill-vetting` の手順でソースをレビューすること。
