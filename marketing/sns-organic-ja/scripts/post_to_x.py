#!/usr/bin/env python3
"""承認済みの投稿ファイルをX(旧Twitter)へ投稿する。

使い方:
    python3 post_to_x.py sns-queue/20260715-2000-campaign.md [--dry-run]

投稿ファイル形式(frontmatter付きMarkdown):
    ---
    status: approved        # approvedのみ投稿可。postedは二重投稿として拒否
    platform: x
    scheduled_at: 2026-07-15 20:00
    media: img/a.png, img/b.png   # 任意
    ---
    投稿本文

必要: pip install requests requests-oauthlib
環境変数: X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET
投稿成功時、ファイルの status を posted に書き換え、投稿IDと日時を追記する。
"""
import argparse
import datetime
import os
import pathlib
import sys

POST_URL = "https://api.x.com/2/tweets"
MEDIA_URL = "https://upload.twitter.com/1.1/media/upload.json"


def parse_post(path: pathlib.Path):
    raw = path.read_text(encoding="utf-8")
    if not raw.lstrip().startswith("---"):
        sys.exit("エラー: frontmatter(---)がありません")
    try:
        _, fm, body = raw.split("---", 2)
    except ValueError:
        sys.exit("エラー: frontmatterが閉じていません")
    meta = {}
    for line in fm.strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.split("#")[0].strip()
    return meta, body.strip(), raw


def weighted_length(text: str) -> int:
    """Xの重み付き文字数(全角・かな・漢字=2、半角=1)の近似値。上限280。"""
    total = 0
    for ch in text:
        o = ord(ch)
        # CJK・かな・全角記号・ハングル等はウェイト2
        if (0x1100 <= o <= 0x11FF or 0x2E80 <= o <= 0x9FFF or
                0xA960 <= o <= 0xA97F or 0xAC00 <= o <= 0xD7FF or
                0xF900 <= o <= 0xFAFF or 0xFE30 <= o <= 0xFE4F or
                0xFF00 <= o <= 0xFF60 or 0xFFE0 <= o <= 0xFFE6):
            total += 2
        else:
            total += 1
    return total


def main() -> None:
    ap = argparse.ArgumentParser(description="承認済み投稿ファイルをXへ投稿")
    ap.add_argument("post_file", help="投稿ファイル(.md)")
    ap.add_argument("--dry-run", action="store_true", help="投稿せず内容確認のみ")
    args = ap.parse_args()

    path = pathlib.Path(args.post_file)
    if not path.exists():
        sys.exit(f"エラー: ファイルがありません: {path}")
    meta, body, raw = parse_post(path)

    status = meta.get("status", "")
    if status == "posted":
        sys.exit(f"拒否: すでに投稿済みです(posted_id: {meta.get('posted_id', '不明')})")
    if status != "approved":
        sys.exit(f"拒否: status が approved ではありません(現在: {status or '未設定'})。人間の承認後に実行してください")
    if not body:
        sys.exit("エラー: 本文が空です")

    length = weighted_length(body)
    if length > 280:
        sys.exit(f"エラー: 文字数超過({length}/280 重み付き)。本文を短くしてください")

    media_files = [m.strip() for m in meta.get("media", "").split(",") if m.strip()]
    for m in media_files:
        if not pathlib.Path(m).exists():
            sys.exit(f"エラー: メディアがありません: {m}")

    print(f"--- 投稿内容({length}/280) ---")
    print(body)
    if media_files:
        print(f"--- メディア: {', '.join(media_files)} ---")
    if args.dry_run:
        print("[dry-run] 投稿は実行していません")
        return

    for key in ("X_API_KEY", "X_API_SECRET", "X_ACCESS_TOKEN", "X_ACCESS_SECRET"):
        if not os.environ.get(key):
            sys.exit(f"エラー: 環境変数 {key} が未設定です")

    try:
        import requests
        from requests_oauthlib import OAuth1
    except ImportError:
        sys.exit("pip install requests requests-oauthlib が必要です")

    auth = OAuth1(
        os.environ["X_API_KEY"], os.environ["X_API_SECRET"],
        os.environ["X_ACCESS_TOKEN"], os.environ["X_ACCESS_SECRET"],
    )

    media_ids = []
    for m in media_files:
        with open(m, "rb") as f:
            r = requests.post(MEDIA_URL, auth=auth, files={"media": f}, timeout=60)
        if r.status_code != 200:
            sys.exit(f"メディアアップロード失敗({m}): {r.status_code} {r.text}")
        media_ids.append(r.json()["media_id_string"])

    payload = {"text": body}
    if media_ids:
        payload["media"] = {"media_ids": media_ids}
    r = requests.post(POST_URL, auth=auth, json=payload, timeout=60)
    if r.status_code != 201:
        sys.exit(f"投稿失敗: {r.status_code} {r.text}")

    tweet_id = r.json()["data"]["id"]
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    updated = raw.replace(
        f"status: {status}",
        f"status: posted\nposted_id: {tweet_id}\nposted_at: {now}", 1,
    )
    path.write_text(updated, encoding="utf-8")
    print(f"投稿完了: id={tweet_id}(ファイルを posted に更新済み)")


if __name__ == "__main__":
    main()
