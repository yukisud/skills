---
name: sns-organic-ja
description: X(Twitter)・Instagram等のSNS運用の実働。投稿の企画から完成原稿の制作、承認フロー、実際の投稿実行(X API・Instagram Graph API、同梱スクリプト)、計測までを一気通貫で行う。「SNS運用」「Xに投稿して」「投稿を作って予約して」「今月の投稿カレンダー」「インスタ運用」「炎上対応」などの依頼で起動。
---

# SNS運用スキル(制作から投稿実行まで)

案出しで止まらない。**完成原稿を作り、承認を経て、実際に投稿するところまで**がこのスキルの仕事。広告は `creative/ad-creative-ja`、LINE配信は `marketing/line-official-ja`、画像制作は `creative/image-generation-ja` と連携。

## 0. アカウント設計(初回のみ)

- 目的を1つに定める(認知/ファン化/採用/サポート)。目的が違えばKPIも投稿も別物
- 媒体特性: X=速報・拡散・テキスト(日本で特に強い)/ Instagram=世界観・保存・店舗/ TikTok=フォロワー外リーチ/ YouTube=資産化。**最初は1媒体に集中**
- プロフィール最適化(誰向けに何を発信+実績+導線リンク)。バズ流入の受け皿はプロフィール

## 1. 月次運用サイクル(このループを回す)

```
月初: 投稿カレンダー作成(型の配合を設計) 
  → 一括制作(完成原稿。2週間分をまとめて)
  → 人間の承認(status: approved に変更)
  → 投稿実行(予約時刻に §4 の手段で自動/手動投稿)
  → 実績記録 → 月末レビュー(§6)→ 翌月の配合に反映
```

- 型の配合: **役立ち・面白い2 : 舞台裏・人柄1 : 告知1以下**。告知だけのアカウントはフォローする理由がない
- 頻度は継続可能な水準で固定(週3を6ヶ月 > 毎日を3週間)。ネタ切れ防止のストック4系統: よくある質問/制作過程/失敗談/データ

## 2. 投稿制作(完成原稿ルール)

**「〜という内容はどうでしょう」の案で止めない。コピペで投稿できる完成形を書く:**

- 冒頭1行(タイムラインで見える範囲)で誰向けかとベネフィットを言い切る。1投稿1メッセージ
- 文字数: Xは全角140字相当(半角280。全角・かな・漢字は2カウント)。上限ギリギリを狙わず読みやすい改行を優先
- Instagramはキャプション冒頭2行(折りたたみ前)に要点、ハッシュタグは関連性の高いものに絞る。Xは0〜2個
- 画像・動画が要る投稿は `creative/image-generation-ja` への指示書(またはできた素材のパス)まで揃える。altテキストも書く
- 文体は `marketing/ja-humanizer` の基準で仕上げる(SNSはAI臭への感度が特に高い)
- トレンド便乗は自社の文脈と接続できるものだけ。**災害・事件・訃報・政治への便乗は全面禁止**

## 3. 承認と投稿キュー(外部公開ゲート)

投稿は外部公開なので**人間の承認なしに投稿を実行しない**(`management/agent-team-orchestration-ja` の原則)。承認を効率化するためキュー方式で運用する:

`sns-queue/YYYYMMDD-HHMM-<slug>.md` に1投稿1ファイルで保存:

```markdown
---
status: draft          # draft → approved(人間が変更) → posted(スクリプトが変更)
platform: x
scheduled_at: 2026-07-15 20:00
media: img/campaign.png   # 任意。カンマ区切りで複数可
---
(投稿本文の完成形)
```

- 承認者は本文と§5のチェック結果を見て `status: approved` に書き換える(まとめて週1回でよい)
- `posted` のファイルは投稿IDと日時が追記され、**二重投稿はスクリプト側で拒否**される
- 週次運用に慣れたら、信頼台帳の昇格基準(20回×95%)に沿って「型が固定された定常投稿のみ事後承認」へ緩和を検討

## 4. 投稿実行(実働)

### X(同梱スクリプト)
初回セットアップ: X開発者ポータルでアプリ作成(無料枠で投稿可。上限は公式で確認)→ API Key/Secret と Access Token/Secret(Read and Write権限)を取得し環境変数へ(`.env` 管理、コミット禁止):

```bash
export X_API_KEY=... X_API_SECRET=... X_ACCESS_TOKEN=... X_ACCESS_SECRET=...
pip install requests requests-oauthlib

# 動作確認(投稿されない)
python3 <スキルdir>/scripts/post_to_x.py sns-queue/20260715-2000-campaign.md --dry-run
# 本番投稿(status: approved のファイルのみ実行可能)
python3 <スキルdir>/scripts/post_to_x.py sns-queue/20260715-2000-campaign.md
```

- 予約投稿: cron / GitHub Actions(schedule)/ 定時セッションから `scheduled_at` を過ぎた approved ファイルを順に実行
- X用MCPサーバーや投稿管理ツール(Buffer等)が接続済みの環境ではそちらを優先(キューの承認フローは同じ)

### Instagram(Graph API)
ビジネス/クリエイターアカウント+Facebookアプリが前提。画像は公開URLが必要:

```bash
# 1. コンテナ作成
curl -X POST "https://graph.facebook.com/v21.0/${IG_USER_ID}/media" \
  -d "image_url=<画像URL>" -d "caption=<本文>" -d "access_token=${IG_ACCESS_TOKEN}"
# 2. 返ってきたcreation_idで公開
curl -X POST "https://graph.facebook.com/v21.0/${IG_USER_ID}/media_publish" \
  -d "creation_id=<id>" -d "access_token=${IG_ACCESS_TOKEN}"
```

トークンは長期トークンに交換して環境変数管理。API接続が用意できない場合は、完成原稿+画像+投稿日時のセットを納品し、予約投稿は媒体の公式機能(Meta Business Suite等)で行う手順を案内する。

## 5. 投稿前チェック(承認者向け・全投稿)

- [ ] 政治・宗教・ジェンダー・容姿・国籍に触れる表現はないか(意図せぬ文脈でも)
- [ ] 誰かを下げて笑いを取っていないか(自虐OK、他虐NG)
- [ ] 数字・事実の誤り、顧客・取引先が特定できる情報(写真の映り込み含む)はないか
- [ ] 大きな事故・災害の直後でないか → **予約投稿の一時停止を先に**
- [ ] ステマ規制: 関係者による宣伝・インフルエンサー案件は「PR」明示
- [ ] 規制業種は広告と同基準(`marketing/google-ads-ja-ops` §5)

### 炎上初動(発生時)
1. すぐ消さない・すぐ反論しない。事実確認(論点・拡散範囲)が先。**予約投稿を全停止**
2. 非がある→24時間以内に謝罪と対応を投稿。削除する場合は削除の旨を明記してから(黙って消すと二次炎上)
3. 事実誤認→事実を淡々と1回説明。論戦しない
4. 誹謗中傷・脅迫→証拠保全→法的対応検討。個別に反応しない

## 6. 計測と月次レビュー

- 主KPIは目的に応じて1つ(エンゲージ率/プロフィールアクセス/リンク遷移/保存数)。フォロワー数は補助指標
- posted ファイルが投稿台帳になる: 月次で「型×反応」を集計し、勝ちパターンの同型変奏を翌月カレンダーへ。学びは `gtm/positioning-messaging-ja` に還元
- SNS経由の流入・CVは `data-science/ga4-analysis-ja` のUTM規約で分離計測
