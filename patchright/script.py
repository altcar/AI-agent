SESSION_ID = "sk-dummyapikey"
import asyncio
import random
from patchright.async_api import async_playwright

TARGET_URL = "https://www.instagram.com/prettysushey/saved/all-posts/"


async def human_delay(min_sec=1.5, max_sec=3):
    await asyncio.sleep(random.uniform(min_sec, max_sec))


async def run_automation():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={"width": 1280, "height": 800})
        await context.add_cookies(
            [
                {
                    "name": "sessionid",
                    "value": SESSION_ID,
                    "domain": ".instagram.com",
                    "path": "/",
                    "secure": True,
                }
            ]
        )

        page = await context.new_page()
        print(f"Opening {TARGET_URL}...")
        await page.goto(TARGET_URL, wait_until="domcontentloaded")

        await page.wait_for_selector('a[href*="/p/"]', timeout=15000)
        processed_urls = set()

        while True:
            # Re-scan for post links
            posts = await page.query_selector_all('a[href*="/p/"]')

            for post in posts:
                post_url = await post.get_attribute("href")
                if post_url in processed_urls:
                    continue

                print(f"--> {post_url}")
                try:
                    await post.scroll_into_view_if_needed()
                    await post.click()

                    # Specific selector for the Save/Remove button
                    save_svg_selector = 'svg[aria-label="Save"], svg[aria-label="Remove"], svg[aria-label="Unsave"]'
                    await page.wait_for_selector(save_svg_selector, timeout=8000)

                    # Filter for the correct button div
                    btn = (
                        page.locator('div[role="button"]')
                        .filter(has=page.locator(save_svg_selector))
                        .last
                    )

                    # Get state and toggle
                    current_label = await btn.locator("svg").get_attribute("aria-label")

                    if current_label in ["Remove", "Unsave"]:
                        await btn.click()
                        await human_delay(1.5, 2)

                    await btn.click()  # Re-save
                    await human_delay(2, 3)

                    # Quick Verify
                    final_label = await btn.locator("svg").get_attribute("aria-label")
                    if final_label in ["Remove", "Unsave"]:
                        print("   ✅ Verified.")
                    else:
                        print("   ⚠️ Verification failed, retrying once...")
                        await btn.click()
                        await human_delay(2, 3)

                    await page.keyboard.press("Escape")
                    await human_delay(1, 1.5)

                except Exception as e:
                    print(f"   Critical Error: {e}")
                    await page.keyboard.press("Escape")

                processed_urls.add(post_url)

            # --- IMPROVED SCROLLING ---
            print("Scrolling for more posts...")
            last_height = await page.evaluate("document.body.scrollHeight")
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

            # Wait for potential loading spinner
            await human_delay(4, 6)

            # FIX FOR TYPEERROR: Resolve hrefs into a list before checking
            current_posts = await page.query_selector_all('a[href*="/p/"]')
            current_hrefs = []
            for p_element in current_posts:
                href = await p_element.get_attribute("href")
                current_hrefs.append(href)

            # Check if we've found any new content
            if all(h in processed_urls for h in current_hrefs):
                # Double-check: scroll a bit more or wait longer
                print("No new posts visible. Final scroll check...")
                await page.evaluate("window.scrollBy(0, -200)")  # Jiggle the scroll
                await human_delay(1, 2)
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await human_delay(3, 5)

                # Re-verify
                new_current_posts = await page.query_selector_all('a[href*="/p/"]')
                new_hrefs = [await x.get_attribute("href") for x in new_current_posts]
                if all(h in processed_urls for h in new_hrefs):
                    print("🏁 End of collection reached.")
                    break

        await browser.close()


if __name__ == "__main__":
    asyncio.run(run_automation())
