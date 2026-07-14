---
name: connection-setup-ja
description: 各種API・MCP接続のセットアップアシスタント。Google Ads/GA4/Search Console/LINE/X/HubSpot/Meta/WordPress等の認証情報の取得手順を案内し、接続テストで検証して接続レジストリに登録する。「◯◯を接続したい」「APIキーの設定」「連携セットアップ」「接続が動かない」などの依頼、およびPDCA運転で未接続が実行のボトルネックになったときに起動。
---

# 接続セットアップアシスタント

実働スキルの「実行」を可能にする配線工事を、ユーザーと二人三脚で進める。ユーザーがやるのは**各サービスの管理画面での発行操作だけ**(手順をこのスキルが指示する)。取得した認証情報の設定・検証・登録はこちらで行う。

## 進め方(共通)

1. **必要な接続から繋ぐ**: `docs/connections.md`(接続レジストリ)と進行中のPDCA台帳を見て、実行が止まっている接続を優先。「全部繋いでおく」はしない(使わないキーはリスクでしかない)
2. ユーザーに発行手順を**画面操作の単位で**案内(下記ランブック)
3. 受け取った認証情報を `.env` に設定(**チャットに貼られたキーは設定後にローテーション推奨と伝える**)
4. **検証コマンドで疎通確認**(読み取り系の最小操作)→ 成功して初めて「接続済み」
5. `docs/connections.md` に登録(接続先/状態/できること/認証の所在/発行者/発行日)
6. `engineering/security-review-ja` §1の観点で最終確認(コミット対象外か、スコープ最小か)

### キー管理の共通原則
- スコープ・権限は**必要最小**で発行(全権限トークンを作らない)
- 発行は可能な限り**組織・サービスアカウント**で(個人アカウント発行は退職・担当変更で全接続が死ぬ)
- `.env` は `.gitignore` 済みであること。キーの共有はチャット・メール平文でなくシークレット管理の手段で
- 四半期に一度、connections.md を棚卸し(使っていない接続の失効・ローテーション)

## ランブック(サービス別)

### Google Ads API(除外KW登録・レポート取得)
1. MCCアカウント(なければ作成)→ ツール「APIセンター」で**デベロッパートークン**申請(テストアクセスは即時、基本アクセスは審査あり・数日)
2. Google Cloudで OAuthクライアントID(デスクトップ)作成 → リフレッシュトークン取得
3. 環境変数: `GOOGLE_ADS_DEVELOPER_TOKEN` / `GOOGLE_ADS_CLIENT_ID` / `GOOGLE_ADS_CLIENT_SECRET` / `GOOGLE_ADS_REFRESH_TOKEN` / `GOOGLE_ADS_LOGIN_CUSTOMER_ID`(MCCのID)
4. 検証: GAQLでキャンペーン名を1件取得
- ハマりどころ: 審査前のトークンは本番アカウントに使えない/customer_idはハイフン抜き10桁

### GA4 Data API(実績データ取得)
1. Google Cloudでプロジェクト作成 → 「Google Analytics Data API」を有効化 → **サービスアカウント**作成しJSONキーを取得
2. GA4管理画面 → プロパティのアクセス管理 → サービスアカウントのメールを**閲覧者**で追加
3. 環境変数: `GOOGLE_APPLICATION_CREDENTIALS`(JSONのパス)+ プロパティID
4. 検証: runReportで直近7日のセッション数を取得
- ハマりどころ: 追加先を「アカウント」でなく「プロパティ」にする/JSONキーファイルは .gitignore 必須

### Search Console API(検索パフォーマンス取得)
1. 上記と同じGCPプロジェクトで「Search Console API」を有効化(サービスアカウント流用可)
2. Search Console → 設定 → ユーザーと権限 → サービスアカウントのメールを追加(制限付きで可)
3. 検証: searchanalytics.query で直近7日のクエリ上位10件
- ハマりどころ: ドメインプロパティは `sc-domain:example.com` 形式で指定

### LINE Messaging API(配信実行)
1. LINE Developersコンソール → プロバイダー作成 → Messaging APIチャネル作成(既存の公式アカウントに紐付け)
2. チャネル設定 → Messaging API → **チャネルアクセストークン(長期)**を発行
3. 環境変数: `LINE_CHANNEL_ACCESS_TOKEN`
4. 検証: `GET https://api.line.me/v2/bot/info`(送信なしでbot情報が返る)
- ハマりどころ: 配信は従量課金。検証段階でbroadcastを叩かない(実配信は承認キュー経由のみ)

### X API(投稿実行)
1. developer.x.com でアプリ作成(無料枠で投稿可)→ User authentication settings で **Read and Write** を設定
2. API Key/Secret と Access Token/Secret(自アカウント)を取得
3. 環境変数: `X_API_KEY` / `X_API_SECRET` / `X_ACCESS_TOKEN` / `X_ACCESS_SECRET`
4. 検証: `post_to_x.py --dry-run`(構成確認)+ `GET /2/users/me`
- ハマりどころ: 権限をRead and Writeにする**前**に発行したAccess Tokenは書き込み不可(再発行が必要)

### HubSpot(CRM読み書き)
1. 設定 → 連携 → プライベートアプリ作成 → スコープは必要最小(例: `crm.objects.contacts.read/write`)
2. 環境変数: `HUBSPOT_ACCESS_TOKEN`。公式MCPサーバーを使う場合はHubSpot開発者ドキュメントの手順で `claude mcp add`
3. 検証: コンタクト1件の取得(読み取り)
- ハマりどころ: Super Adminのみプライベートアプリを作成可/一括更新系スコープは最初は付けない

### Meta / Instagram Graph API(IG投稿・広告データ)
1. InstagramをプロアカウントにしてFacebookページと連携 → developers.facebook.com でアプリ作成
2. 必要権限(`instagram_content_publish` 等)でユーザートークン取得 → **長期トークンに交換** → IGユーザーIDを取得
3. 環境変数: `IG_ACCESS_TOKEN` / `IG_USER_ID`
4. 検証: `GET /v21.0/{IG_USER_ID}?fields=username`
- ハマりどころ: 長期トークンも約60日で失効(更新をPDCAの月次タスクに入れる)/画像は公開URL必須

### WordPress REST API(記事入稿)
1. WP管理画面 → ユーザー → プロフィール → **アプリケーションパスワード**を発行(専用の投稿者権限ユーザーを作るのが望ましい)
2. 環境変数: `WP_BASE_URL` / `WP_USER` / `WP_APP_PASSWORD`
3. 検証: `GET {WP_BASE_URL}/wp-json/wp/v2/users/me`(Basic認証)
- ハマりどころ: HTTPS必須/セキュリティプラグインがREST APIやアプリケーションパスワードを無効化している場合がある(その設定変更から案内する)

### OpenSEO / DataForSEO(SEOデータ)
→ `data-science/openseo-ja` §1の手順に従う(監査→Docker→APIキー→MCP接続)。

## トラブルシュート(共通)

| 症状 | まず疑う |
|---|---|
| 401 | キーの誤り・期限切れ・環境変数の読み込み漏れ(`echo ${VAR:+set}` で確認) |
| 403 | スコープ不足・アカウント権限不足・API未有効化(GCP系) |
| 429 | レート制限。リトライは指数バックオフ、恒常的なら取得頻度を設計から見直す |
| 動いていたのに突然失敗 | トークン失効(Meta 60日等)・プラン変更・API仕様変更。connections.mdの発行日を確認 |

原因調査が2手で終わらなければ `engineering/systematic-debugging-ja` のプロセスへ。

## 完了の定義

「キーをもらった」ではなく、**検証コマンドが通り、connections.md に登録され、依頼元のスキル(除外KW登録・配信実行等)が実際に1回動くまで**。接続完了後は依頼元のPDCA台帳の「未接続(手動実行待ち)」を解消する。
