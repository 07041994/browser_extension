import os
import re
# from app2 import FOLDER_NAME
from concurrent.futures import ThreadPoolExecutor, as_completed
from playwright.async_api import async_playwright
import asyncio
from datetime import date, datetime
from logger.logg import log 

FOLDER_NAME = f"FullPageScreenshots_AmanSinghal_{date.today()}"
os.makedirs(FOLDER_NAME,exist_ok=True)

async def save_screenshot_async(urls: list[str]):
    valid_urls = [u for u in urls if u.startswith(("http://", "https://"))]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        # limit concurrency (VERY important)
        semaphore = asyncio.Semaphore(6)

        async def bounded_task(idx, url):
            async with semaphore:
                await process_single_url(browser, url, idx)

        tasks = [
            bounded_task(idx, url)
            for idx, url in enumerate(valid_urls, start=1)
        ]

        await asyncio.gather(*tasks)

        await browser.close()

    log.info("Parallel screenshot job finished")


async def process_single_url(browser, url: str, idx: int):
    page = None
    try:
        log.info(f"[{idx}] Processing {url}")

        page = await browser.new_page()
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(2000)

        title = safe_filename(await page.title())
        base_name = f"Tab{idx}_{title}"

        await scroll_and_capture(page, base_name)

    except Exception as e:
        log.error(f"[{idx}] Failed {url}: {e}")

    finally:
        if page:
            await page.close()


async def scroll_and_capture(page, base_name: str):
    total_height = await page.evaluate("document.body.scrollHeight")
    viewport_height = page.viewport_size["height"]

    scroll_y = 0
    count = 1

    while scroll_y < total_height:
        await page.evaluate(f"window.scrollTo(0, {scroll_y})")
        await page.wait_for_timeout(600)  # allow lazy loading

        file_name = f"{base_name}_{count}.png"
        path = os.path.join(FOLDER_NAME, file_name)

        await page.screenshot(path=path)
        log.info(f"Saved {path}")

        scroll_y += viewport_height
        count += 1

def safe_filename(text: str) -> str:
    """
    Make a string safe for Windows filenames
    """
    text = text.strip()
    text = re.sub(r'[<>:"/\\|?*]', '_', text)  # Windows invalid chars
    text = re.sub(r'\s+', '_', text)           # spaces -> _
    return text[:150]     