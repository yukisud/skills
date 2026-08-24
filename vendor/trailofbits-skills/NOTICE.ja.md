# Trail of Bits Skills(ベンダー取り込み)

このディレクトリは、Trail of Bits 社が公開する Claude Code 用セキュリティ監査スキル集を**原文のまま(改変なし)**取り込んだものです。

## 出典・帰属(CC-BY-SA 4.0 の表示義務)
- 原著作者: **Trail of Bits**
- 元リポジトリ: https://github.com/trailofbits/skills
- 取り込み時のコミット: `293fb74c3151cceda32a85a545fe8acd67f8f5c6`
- 取り込み日: 2026-07
- ライセンス: **Creative Commons Attribution-ShareAlike 4.0 International(CC-BY-SA 4.0)** — 全文は同ディレクトリの `LICENSE` を参照

## ライセンス上の注意
- 本ディレクトリ配下は CC-BY-SA 4.0 で提供される Trail of Bits の著作物であり、**当リポジトリ他部分のライセンスとは別**に扱う。
- 内容は**未改変**(日本語化・編集をしていない)。改変して再配布する場合は CC-BY-SA の継承条件(同一ライセンスでの公開・変更点の明示)に従うこと。
- 日本語化しない理由: 内容が言語・ツール特化で日本固有の観点がなく、再著述は誤りを持ち込むリスクが上回るため(監査記録 `docs/skill-audits/trailofbits-skills-2026-07.md` 参照)。

## 位置づけ
当スキル集の `engineering/security-review-ja`(広く浅い一次レビュー+日本の法令)に対し、こちらは**深い技術監査**(C/Rust・暗号・スマートコントラクト・サプライチェーン・静的解析ルール自作など)を担う委譲先。security-review-ja の「深い技術監査への委譲」節から対応表で参照している。

## 導入(プラグインとして使う場合)
リポジトリに取り込んだこのコピーとは別に、公式マーケットプレイスからプラグインとして有効化することもできる:
```
/plugin marketplace add trailofbits/skills
/plugin menu
```

## 更新
Trail of Bits の更新に追随する場合は、元リポジトリの変更履歴を確認し、このディレクトリを新しいコミットの内容で置き換え、上記コミットハッシュと取り込み日を更新する。
