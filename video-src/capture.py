#!/usr/bin/env python3
"""Capture BOUNTY RUSH gameplay for the bring-the-humans-03 TikTok ad.

Records the deterministic autopilot run with Playwright's video recording
in headless Chromium, 1080x1920, then saves one still frame for a visual
check. Run with the task venv:
  ~/workspace/makefun/tt-day1-venv/bin/python capture.py
Output: gameplay.webm (~12 s) + frame-gameplay.png
"""
import pathlib
import shutil

from playwright.sync_api import sync_playwright

WORK = pathlib.Path(__file__).resolve().parent
SECONDS = 12


def main():
    url = f"file://{WORK / 'game.html'}"
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--force-device-scale-factor=1"])
        ctx = browser.new_context(
            viewport={"width": 1080, "height": 1920},
            device_scale_factor=1,
            record_video_dir=str(WORK),
            record_video_size={"width": 1080, "height": 1920},
        )
        page = ctx.new_page()
        page.goto(url)
        page.wait_for_function("window.__ready === true")
        page.wait_for_timeout(2000)
        sim = page.evaluate("({t: window.__sim.t, score: window.__sim.score})")
        print("sim after 2s:", sim)
        assert sim["t"] > 1.0, "sim is not advancing"
        page.wait_for_timeout((SECONDS - 2) * 1000)
        sim = page.evaluate(
            "({t: window.__sim.t, score: window.__sim.score,"
            " coins: window.__sim.coins, shields: window.__sim.shields})"
        )
        print("sim at end:", sim)
        page.screenshot(path=str(WORK / "frame-gameplay.png"))
        video = page.video
        ctx.close()
        browser.close()
        src = pathlib.Path(video.path())
        dst = WORK / "gameplay.webm"
        if dst.exists():
            dst.unlink()
        shutil.move(str(src), str(dst))
        print("wrote", dst, dst.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
