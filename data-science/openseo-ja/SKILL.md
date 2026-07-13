---
name: openseo-ja
description: OpenSEO(Semrush/Ahrefs のOSS代替、DataForSEO従量課金)のセットアップと運用。キーワード調査・順位取得・競合データの取得基盤として、SEO系スキル群にデータを供給する。「OpenSEOをセットアップ」「キーワードデータを取って」「検索ボリューム調べて」「順位データの取得」などの依頼、およびSEO系スキルが実データを必要とするときに起動。
---

# OpenSEO運用スキル(SEOデータ基盤)

OpenSEO(https://github.com/every-app/open-seo)を、当スキル集のSEO系スキルの**データ層**として使う。役割分担を固定する:

- **データ取得** = OpenSEO(検索ボリューム・順位・競合・被リンク候補)
- **判断・日本語対応・法令・アウトプット** = 当リポジトリのスキル群

## 0. 導入前の確認(スキップ不可)

- [ ] `engineering/skill-vetting` の手順でリポジトリを監査する(OSSでも導入時・アップデート時に毎回。外部送信先がDataForSEOと自ホスト以外にないか)
- [ ] コスト理解: アプリ自体は無料、**DataForSEO APIが従量課金**(最低チャージ$50、新規$1クレジット)。月の上限予算を先に決める
- [ ] APIキーの管理: `.env` に置き**コミット禁止**(`engineering/security-review-ja` §1)

## 1. セットアップ

```bash
git clone https://github.com/every-app/open-seo && cd open-seo
cp .env.example .env
# DataForSEOのダッシュボードで認証情報(Base64表記)を取得し
# .env の DATAFORSEO_API_KEY に設定
docker compose up -d
# http://localhost:3001 で起動確認
```

- Claude Code との接続: アプリのヘッダー「AI & Agents」からMCP接続の案内に従う(公式スキルのインストール手順は https://openseo.so/docs/skills/setup )
- Cloudflareへのセルフホストも可(常時運用・チーム共有するならこちら。公開URLにする場合は必ず認証を付ける)

## 2. 日本市場向けの取得設定(重要)

- クエリの location は **Japan**、language は **ja** を明示する(既定のUS/enのまま取ると日本の実態と全く違う数字が返る)
- ローカルビジネスの順位系データは市区町村レベルの location 指定が使えるか確認し、使えない場合はその旨を分析結果に注記(`seo-research-ja` の計測メモ欄)
- 日本語KWの表記ゆれ(漢字/カナ/送り仮名)は**別KWとして返る**。ボリューム評価は主要表記を合算する(`seo-strategy-ja` の原則と同じ)

## 3. 当スキル集との連携マップ

| OpenSEO側の機能・スキル | データを渡す先 | 用途 |
|---|---|---|
| keyword-research / keyword-clustering | `marketing/seo-strategy-ja` Phase3 | KWマップの検索ボリューム・グルーピング |
| 順位取得(rank tracking) | `data-science/seo-research-ja` | 週次順位チェックのデータ源(Search Consoleの補完) |
| competitive-landscape / competitor-analysis | `gtm/competitor-analysis-ja`・`data-science/seo-research-ja` | 検索面の競合把握・流入KW推定 |
| link-prospecting | `marketing/seo-strategy-ja` Phase4 | 被リンク候補の洗い出し(獲得判断は日本の現実性で選別) |
| seo-coach / seo-project-setup | 原則使わない | 戦略判断は `seo-strategy-ja` が担当(日本市場前提・法令・MEO優先度を持っているため)。英語圏の一般論と判断が割れたら当スキル集を優先 |

## 4. コスト規律(従量課金の事故防止)

- 調査は**対象を絞ってから叩く**: KWリスト全件×毎日ではなく、戦略KW(〜50個)×週次から始める
- 同じデータを再取得しない: 取得結果は `docs/seo-data/YYYY-MM/` に保存して使い回す(`sc-ga4-report-ja` の蓄積方針と同じ)
- 月初にDataForSEOの残高と当月消費を確認し、月次レポートに「データ取得コスト」として計上する
- 大量取得(1,000KW超の一括調査等)は実行前に概算コストを出してユーザーに確認する

## 5. データの解釈の注意

- DataForSEOの検索ボリュームは推定値。**桁の判断(100か1,000か10,000か)に使い、1桁台の精度で意思決定しない**
- 順位データはSearch Consoleの実測と併用し、乖離したらSC側を正とする(`seo-research-ja` の原則)
- クライアント案件で使う場合、取得データの扱い(保持・削除)は `sc-ga4-report-ja` のスポットモードの規律に従う
