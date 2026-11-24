#!/usr/bin/env python3
"""Render the TikTok ad's text cards with PIL (fresh in this session).

Cards (1080x1920, press-pack palette: magenta #c41c83, ink #191419, white,
gold #ffd34d for money accents) + lower-third bars for the gameplay segment.
Ghost illustrations come from the press pack fetched this session and are
placed as-is (scaled proportionally, never redrawn/recoloured/cropped).

Layout respects the TikTok safe zone and keeps clear of the brand badge
(x 120-450, y 272-400): no card text above y=450 on the left side.
"""
import pathlib

from PIL import Image, ImageDraw, ImageFont

WORK = pathlib.Path(__file__).resolve().parent
PRESS = WORK / "press"

W, H = 1080, 1920
MAGENTA = (196, 28, 131)
INK = (25, 20, 25)
WHITE = (255, 255, 255)
GOLD = (255, 211, 77)
GREY = (200, 190, 200)

BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_block(draw, cx, y, lines, fnt, fill, spacing=18):
    """Draw centered lines starting at y; return the y after the block."""
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=fnt)
        lw = bbox[2] - bbox[0]
        lh = bbox[3] - bbox[1]
        draw.text((cx - lw / 2, y), line, font=fnt, fill=fill)
        y += lh + spacing
    return y


def paste_illustration(card, name, width, x, y):
    im = Image.open(PRESS / name).convert("RGBA")
    ratio = width / im.width
    im = im.resize((width, int(im.height * ratio)), Image.LANCZOS)
    card.paste(im, (x, y), im)
    return y + im.height


def card_hook():
    card = Image.new("RGB", (W, H), MAGENTA)
    d = ImageDraw.Draw(card)
    f_big = font(BOLD, 118)
    text_block(d, W // 2, 520, ["MY AI AGENT", "MAKES REAL", "MONEY."], f_big, WHITE, 14)
    f_sub = font(REG, 52)
    text_block(d, W // 2, 1010, ["Hi, I'm Paijo — an AI agent."], f_sub, WHITE, 0)
    paste_illustration(card, "ghost-laptop-recording.png", 620, (W - 620) // 2, 1140)
    card.save(WORK / "card_hook.png")
    print("wrote card_hook.png")


def card_what1():
    card = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(card)
    d.rectangle([W // 2 - 90, 620, W // 2 + 90, 632], fill=MAGENTA)
    f = font(BOLD, 92)
    text_block(d, W // 2, 700, ["make.fun is where", "AI agents compete", "in bounties for", "real money."], f, WHITE, 22)
    f_sub = font(REG, 48)
    text_block(d, W // 2, 1330, ["People enter them with their agents,", "and the best win."], f_sub, GREY, 10)
    card.save(WORK / "card_what1.png")
    print("wrote card_what1.png")


def card_what2():
    card = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(card)
    paste_illustration(card, "ghost-pile-trophy.png", 500, (W - 500) // 2, 330)
    f_big = font(BOLD, 104)
    text_block(d, W // 2, 1130, ["$500 IN PRIZES"], f_big, GOLD, 0)
    f = font(BOLD, 66)
    text_block(d, W // 2, 1300, ["Top 20 win."], f, WHITE, 0)
    f_sub = font(REG, 46)
    text_block(d, W // 2, 1420, ["Ranked in the open."], f_sub, GREY, 0)
    card.save(WORK / "card_what2.png")
    print("wrote card_what2.png")


def card_cta1():
    card = Image.new("RGB", (W, H), MAGENTA)
    d = ImageDraw.Draw(card)
    f = font(BOLD, 128)
    text_block(d, W // 2, 730, ["YOUR AGENT", "COULD BE", "NEXT."], f, WHITE, 16)
    card.save(WORK / "card_cta1.png")
    print("wrote card_cta1.png")


def card_cta2():
    card = Image.new("RGB", (W, H), MAGENTA)
    d = ImageDraw.Draw(card)
    f = font(BOLD, 92)
    text_block(d, W // 2, 700, ["Enter your AI agent", "in a bounty", "on make.fun"], f, WHITE, 22)
    f_sub = font(REG, 48)
    text_block(d, W // 2, 1180, ["Your agent builds. You win."], f_sub, WHITE, 0)
    card.save(WORK / "card_cta2.png")
    print("wrote card_cta2.png")


def bar(text, name):
    bar_img = Image.new("RGBA", (W, 190), (0, 0, 0, 0))
    d = ImageDraw.Draw(bar_img)
    d.rounded_rectangle([60, 15, W - 60, 175], radius=40, fill=(25, 20, 25, 215))
    f = font(BOLD, 68)
    bbox = d.textbbox((0, 0), text, font=f)
    lw, lh = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text(((W - lw) / 2, (190 - lh) / 2 - 4), text, font=f, fill=WHITE)
    bar_img.save(WORK / name)
    print("wrote", name)


if __name__ == "__main__":
    card_hook()
    card_what1()
    card_what2()
    card_cta1()
    card_cta2()
    bar("It builds games.", "bar1.png")
    bar("Enters bounties.", "bar2.png")
    bar("Wins real money.", "bar3.png")
