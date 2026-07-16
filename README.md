# skills — 日本環境最適化 業務スキル集

Claude Code / Claude 向けの Agent Skills 集。海外の高評価スキル(marketingskills, marketing-mode, Ryze, superpowers, agent-team-orchestration ほか)の設計を参考に、**日本の法規制・広告仕様・商習慣・日本語の言語特性**に合わせて再設計したもの。

**業種には依存しない汎用設計。** EC・SaaS・アプリ・店舗・BtoB・医療など幅広く使える。医療広告ガイドライン・薬機法などの規制対応は「該当業種のときだけ発動する条件分岐」として各スキルに組み込んである。

**完了の定義は「提案」ではなく「実行と記録」。** 実働スキルはAPI・スクリプト接続があれば実行まで行い(承認ゲート対象を除く)、結果をPDCA台帳(`management/pdca-runner-ja`)に記録して次サイクルへつなぐ。接続が未整備の場合のみ、入稿可能な完成物+実行手順の納品で代替する。

## 構成(6分野・47スキル)

```
gtm/              Go-To-Market(戦略・ポジショニング・競合・価格)
marketing/        マーケティング(広告運用・SEO・MEO・LINE・CRM・レビュー)
creative/         制作(LP・広告クリエイティブ・画像生成・資料・デザインレビュー)
engineering/      エンジニアリング(ツール開発・AI駆動開発・セキュリティ・デバッグ・UI)
management/       経営・業務(AIチーム編成・レポート・議事録・メール・監査ログ)
data-science/     データサイエンス(リサーチ・データ突合)
```

### GTM(戦略の上流)

| スキル | 役割 | 内容 |
|---|---|---|
| `gtm/gtm-strategy-ja` | 推論 | 市場投入計画の司令塔。チャネル選定マップ(LINE・Yahoo!・ポータル含む)、KPIツリー、撤退基準 |
| `gtm/positioning-messaging-ja` | 推論 | バリュープロップ定義→全チャネルへ一貫展開するメッセージングフレームワーク |
| `gtm/competitor-analysis-ja` | 推論 | 広告透明性センター・口コミ・登記等の日本の情報源による競合分析。打ち手接続まで必須 |
| `gtm/pricing-strategy-ja` | 推論 | 松竹梅設計、値上げの進め方、総額表示・二重価格の法令対応 |
| `gtm/customer-research-ja` | 推論 | 顧客インタビュー・アンケート設計。Mom Test原則、日本人回答者のバイアス対策 |

### マーケ

| スキル | 役割 | 内容 |
|---|---|---|
| `marketing/google-ads-ja-ops` | 推論 | 運用判断の頭脳。入札・P-Max・予算のCV件数別ロジック+医療広告GL/薬機法/景表法 |
| `marketing/seo-strategy-ja` | 推論 | Technical→On-Page→Content→Off-Pageの診断。MEO・ポータル支配SERP前提 |
| `marketing/rsa-copywriter-ja` | 実働 | RSA広告文。全角15/45文字カウント+法令セルフチェック付き出力 |
| `marketing/hubspot-ops-ja` | 実働 | CRM/MA設計。名寄せ・フリガナ・特定電子メール法・オフラインCV連携 |
| `marketing/meo-ja` | 実働 | Googleビジネスプロフィール運用。口コミ獲得・返信(医療の守秘義務対応)、ローカル順位改善 |
| `marketing/line-official-ja` | 実働 | LINE公式アカウント。友だち導線・リッチメニュー・リマインド配信でリピートを作る |
| `marketing/sns-organic-ja` | 実働 | SNS運用の一気通貫。完成原稿の制作→承認キュー→**実投稿の実行**(X投稿スクリプト同梱・IG Graph API手順)→計測。炎上管理込み |
| `marketing/press-release-ja` | 実働 | プレスリリース。ニュース価値判定、記者視点の逆三角形構成、配信・効果測定 |
| `marketing/negative-keyword-scanner` | レビュー | 検索語句レポート→除外KW。日本語表記ゆれ対応 |
| `marketing/seo-content-scorer-ja` | レビュー | 記事採点100点制。YMYL医療はE-E-A-T配点2倍 |
| `marketing/ja-humanizer` | レビュー | 日本語特有のAI文体兆候の除去 |

### 制作(Creative)

| スキル | 役割 | 内容 |
|---|---|---|
| `creative/lp-builder-ja` | 実働 | LP構成定石・EFO・法定表記・CV計測設計まで一気通貫 |
| `creative/ad-creative-ja` | 実働 | 訴求軸マトリクス、Meta/LINE/YouTube/GDN入稿規格、テスト・疲弊管理 |
| `creative/sales-deck-ja` | 実働 | 稟議で回覧される前提の提案書・営業資料。SLIDE.md方式でデザインと内容を分離 |
| `creative/image-generation-ja` | 実働 | 画像生成ワークフロー。指示の仕様化(Scene/Subject/Details/UseCase/Constraints)、形容詞→視覚情報変換、クロマキー透過スクリプト同梱 |
| `creative/design-review-ja` | レビュー | 3秒テスト・タイポ・打消し表示の視認性など出稿前レビュー |

### エンジニア

| スキル | 役割 | 内容 |
|---|---|---|
| `engineering/security-review-ja` | レビュー | **開発系タスクの完了前・リリース前に必須。** シークレット/インジェクション/認可/依存/CI/CD/個人情報保護法まで10章の網羅チェック |
| `engineering/systematic-debugging-ja` | 推論 | 再現→最小化→仮説検証→根本原因の体系的デバッグ。推測修正の禁止 |
| `engineering/tool-design-ja` | 推論 | ツール開発の上流。要件定義・作らない判断・技術選定・デプロイ先選定・仕様書 |
| `engineering/tool-development-ja` | 実働 | 仕様書からの開発実働。テスト・security-review必須ゲート・デプロイ・引き継ぎREADME |
| `engineering/tool-maintenance-ja` | 実働 | 既存ツールの解析→逆仕様書→安全な変更・修正。回帰確認と変更記録 |
| `engineering/frontend-design-ja` | 実働 | 日本語タイポグラフィ(行間・禁則・フォントスタック)込みのUI実装 |
| `engineering/skill-vetting` | レビュー | 外部スキル導入前のマルウェア・データ流出・プロンプトインジェクション監査 |
| `engineering/connection-setup-ja` | 実働 | API/MCP接続のセットアップ。Google Ads/GA4/SC/LINE/X/HubSpot/Meta/WP のランブック+検証+レジストリ登録 |
| `engineering/ai-agent-design-ja` | 推論 | AIエージェント設計。シンプル設計原則、ガードレール4層と権限L0-L4、構成図(契約書思想)、MCP権限5原則 |
| `engineering/prompt-engineering-ja` | 推論 | 業務プロンプト設計。ハルシネーション防止10パターン、投入前検証(通常/境界/敵対/長文の件数基準) |
| `engineering/rag-design-ja` | 推論 | RAG・ナレッジAI設計。チャンク設計の具体値、権限3層、インジェクション防御、Recall@10等の評価指標 |
| `engineering/ai-eval-harness-ja` | レビュー | 評価ハーネス構築4フェーズ、シャドー→カナリア段階投入、AI生成コードの自動採点3レーン |

### 経営・業務

| スキル | 役割 | 内容 |
|---|---|---|
| `management/agent-team-orchestration-ja` | 推論 | AI社員化の設計図。3層分離(推論/実働/レビュー)・報連相様式・人間承認ゲート・信頼台帳 |
| `management/pdca-runner-ja` | 実働 | **全施策のPDCA運転席。** 施策台帳(P→D→C→A)、承認ゲート初期ルール、接続レジストリ、定期起動での自走 |
| `management/client-report-generator-ja` | 実働 | 月次報告書の定型(サマリ→実績→分析→翌月施策) |
| `management/meeting-minutes-ja` | 実働 | 議事録。決定事項・TODO(担当/期日)構造化、社外配布版の出し分け |
| `management/business-email-ja` | 実働 | ビジネスメール。敬語添削表、依頼/催促/謝罪/断りの型 |
| `management/customer-support-ja` | 実働 | 問い合わせ・クレーム対応。一次対応の型、部分謝罪の使い分け、カスハラ打ち切り基準 |
| `management/ai-adoption-ja` | 推論 | AI駆動開発の組織導入。3新ロール(兼任禁止)、スキルマップ4軸、30/90/180日育成ゲート |
| `management/command-logger` | レビュー | hooksによる全ツール実行のJSONL監査ログ(スクリプト同梱) |

### データサイエンス

| スキル | 役割 | 内容 |
|---|---|---|
| `data-science/seo-research-ja` | 実働 | 順位・SERP・競合の週次モニタリング→ブリーフィング化 |
| `data-science/ga4-analysis-ja` | 実働 | GA4の設定監査と分析。しきい値・not set等の誤読防止、LP別・ファネル分析 |
| `data-science/sc-ga4-report-ja` | 実働 | Search Console×GA4統合分析。自社=常時蓄積/クライアント=スポット受領の2モード |
| `data-science/dashboard-design-ja` | レビュー | ダッシュボード設計規律(デジタル庁ガイド準拠)。構成比は横棒・軸0起点・定義注記必須 |
| `data-science/openseo-ja` | 実働 | OpenSEO(Semrush/AhrefsのOSS代替)をSEOデータ基盤化。日本向け設定・コスト規律・スキル連携マップ |
| `data-science/data-reconciliation` | レビュー | Looker Studio等と生データの突合QA。CV確定遅延・税込税抜等の頻出ズレ対応 |

## インストール

個人スキルとして使う場合、各スキルディレクトリを `~/.claude/skills/` 配下にコピー:

```bash
cp -r marketing/google-ads-ja-ops ~/.claude/skills/
```

プロジェクトスキルとして使う場合は、対象リポジトリの `.claude/skills/` 配下に配置。

## 推奨セット

**広告運用の最短ルート(3点)**
1. `marketing/google-ads-ja-ops` — 運用判断
2. `marketing/negative-keyword-scanner` — 除外KWの実務
3. `management/command-logger` — 実行権限を渡す前の監査基盤

**開発の必須セット(3点)**
1. `engineering/security-review-ja` — コードを外に出す前に必ず通す
2. `engineering/systematic-debugging-ja` — 障害対応の型
3. `engineering/skill-vetting` — 外部スキル導入時の門番

**新規事業・新サービスの立ち上げ(GTM一式)**
`gtm/` の4本 → 決まったメッセージを `creative/`・`marketing/` の実働スキルへ展開

**AI駆動開発セット(AI機能・エージェントを作るとき)**
`ai-agent-design-ja`(設計)→ `prompt-engineering-ja` / `rag-design-ja`(実装設計)→ `ai-eval-harness-ja`(品質)→ 組織定着は `ai-adoption-ja`

**ツール開発の一気通貫**
`tool-design-ja`(要件定義〜仕様書)→ `tool-development-ja`(実装〜デプロイ)→ 運用後の変更は `tool-maintenance-ja`。出荷前の `security-review-ja` は全ルート必須

## 品質管理

全スキルは6項目の監査基準(起動条件・入力定義・数値基準・出力形式・参照整合・事実正確性)でチェック済み。監査記録と**経年劣化しやすい項目の台帳**(媒体仕様・料金・法令など年1回要確認)は `docs/quality-audit-2026-07.md` を参照。数値基準は業界横断の経験則のため、自社実績が貯まったら実測値で上書きして育てること。

## ⚠️ 外部スキル導入時の注意

外部配布スキル(マーケットプレイス等)には悪意あるコードの混入事例が報告されている。導入前に必ず `engineering/skill-vetting` の手順でソースをレビューし、導入後は `management/command-logger` のログで事後監査すること。
