# スキル監査記録: phuryn/pm-skills(2026-07)

`engineering/skill-vetting` の手順で実施。

## 判定: 導入可

## 対象
- リポジトリ: https://github.com/phuryn/pm-skills(⭐23.9k、MIT、v2.1.0)
- 作者: Paweł Huryn(The Product Compass)
- 構成: Markdown 124 / JSON 10 / Python 3(ローカル検証・テストのみ)/ 画像。バイナリ・難読化なし

## 検査結果
| 観点 | 結果 |
|---|---|
| ネットワーク送信 | なし(grep一致2件は「feature requests」等の誤検知を目視確認) |
| 機密アクセス | なし(一致はセキュリティ監査チェックリストの説明文) |
| 実行系危険パターン(eval/base64/rm等) | 検出ゼロ |
| Pythonスクリプト | validate_plugins.py・tests/ ともファイル読み取りのみ。ネットワーク・サブプロセスなし |
| プロンプトインジェクション(隠し指示) | SKILL.md内のHTMLコメント・隠しテキストなし |

## 導入方針
- 高価値スキルを日本語化して当リポジトリに収録: product/prd-ja, product/product-discovery-ja, product/roadmap-okr-ja, management/premortem-redteam-ja, data-science/ab-test-analysis-ja
- 残り(SWOT/PESTLE/ペルソナ等の汎用フレームワーク)は本家をプラグインとして併用:
  `claude plugin marketplace add phuryn/pm-skills` → 必要なプラグインのみインストール
- **除外**: pm-toolkit の draft-nda / privacy-policy(英米法・GDPR前提。日本の契約・個人情報保護法にはそのまま使用不可)

## 再監査条件
バージョン更新時(スキル追加・スクリプト変更があった場合)に再実施。
