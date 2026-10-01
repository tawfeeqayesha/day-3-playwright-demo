
from playwright.sync_api import sync_playwright, TimeoutError

SCORE_SELECTOR = "span.font-medium.wb\\:font-semibold"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    try:
        # Open Cricbuzz
        page.goto(
            "https://www.cricbuzz.com/",
            wait_until="domcontentloaded"
        )

        # Wait for the score element
        page.wait_for_selector(
            SCORE_SELECTOR,
            state="visible",
            timeout=30000
        )

        # Get and print the score
        score = page.locator(SCORE_SELECTOR).first.inner_text().strip()

        if score:
            print("Latest score:", score)
        else:
            print("No live score is currently available.")

        # Take screenshot BEFORE closing the browser
        page.screenshot(path="score.png", full_page=True)
        print("Screenshot saved as score.png")

    except TimeoutError:
        print("The score element was not found within 30 seconds.")

        # Save a screenshot for debugging
        page.screenshot(path="score.png", full_page=True)
        print("Screenshot saved as score.png")

    finally:
        # Close browser while Playwright is still running
        browser.close()