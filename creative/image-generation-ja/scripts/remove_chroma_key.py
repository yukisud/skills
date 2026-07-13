#!/usr/bin/env python3
"""クロマキー背景を除去してアルファチャンネル化するスクリプト。

単色背景(緑/マゼンタ等)で生成した画像から背景色を透過にする。
使い方:
    python3 remove_chroma_key.py input.png output.png --color "#00FF00" --threshold 60 [--despill]

依存: Pillow (pip install Pillow)
"""
import argparse
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow が必要です: pip install Pillow")


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    v = value.lstrip("#")
    if len(v) != 6:
        raise argparse.ArgumentTypeError(f"色は #RRGGBB 形式で指定してください: {value}")
    return tuple(int(v[i : i + 2], 16) for i in (0, 2, 4))


def main() -> None:
    p = argparse.ArgumentParser(description="クロマキー背景の透過処理")
    p.add_argument("input", help="入力画像(単色背景)")
    p.add_argument("output", help="出力PNG(アルファ付き)")
    p.add_argument("--color", type=hex_to_rgb, default="#00FF00",
                   help="背景色 #RRGGBB(既定: #00FF00)")
    p.add_argument("--threshold", type=int, default=60,
                   help="背景と判定する色距離(既定: 60。フリンジが残るなら上げる)")
    p.add_argument("--soft", type=int, default=40,
                   help="半透明にする境界幅(既定: 40。0でハードエッジ)")
    p.add_argument("--despill", action="store_true",
                   help="輪郭に残った背景色被り(スピル)を抑える")
    args = p.parse_args()

    img = Image.open(args.input).convert("RGBA")
    px = img.load()
    kr, kg, kb = args.color
    th, soft = args.threshold, max(args.soft, 1)

    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = px[x, y]
            # ユークリッド色距離で背景らしさを判定
            dist = ((r - kr) ** 2 + (g - kg) ** 2 + (b - kb) ** 2) ** 0.5
            if dist <= th:
                px[x, y] = (r, g, b, 0)
            elif dist <= th + soft:
                # 境界は距離に応じて半透明化(髪・輪郭のジャギー軽減)
                alpha = int(a * (dist - th) / soft)
                px[x, y] = (r, g, b, alpha)

            if args.despill and px[x, y][3] > 0:
                r, g, b, a = px[x, y]
                # 背景色の主成分が他成分より突出していたら抑える(緑被り等の除去)
                dominant = max(kr, kg, kb)
                if dominant == kg and g > max(r, b):
                    px[x, y] = (r, max(r, b), b, a)
                elif dominant == kr and r > max(g, b):
                    px[x, y] = (max(g, b), g, b, a)
                elif dominant == kb and b > max(r, g):
                    px[x, y] = (r, g, max(r, g), a)

    img.save(args.output, "PNG")
    print(f"保存しました: {args.output}")


if __name__ == "__main__":
    main()
