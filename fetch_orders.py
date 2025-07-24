# fetch_orders.py
import asyncio
from playwright.async_api import async_playwright
import csv
import os

EMAIL = os.getenv("ROYALMAIL_EMAIL")
PASSWORD = os.getenv("ROYALMAIL_PASSWORD")
OUTPUT_FILE = "orders.csv"

async def fetch_orders():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # Step 1: Login
        await page.goto("https://business.parcel.royalmail.com")
        await page.fill("#Email", EMAIL)
        await page.fill("#Password", PASSWORD)
        await page.click("button.cnd-login-button")

        # Step 2: Go to orders page
        await page.wait_for_url("**/dashboard")
        await page.goto("https://business.parcel.royalmail.com/orders/")
        await page.wait_for_selector("table#openorders")

        # Step 3: Scrape order data
        rows = await page.query_selector_all("table#openorders tbody tr")
        data = []

        for row in rows:
            cells = await row.query_selector_all("td, th")
            values = [await cell.inner_text() for cell in cells]

            # Extract only relevant columns (based on HTML structure)
            order_data = {
                "Order": values[1],
                "Date": values[2],
                "Batch": values[3],
                "Customer": values[4],
                "Package Format": values[5],
                "Shipping Service": values[6],
                "Tracking": values[7],
                "Status": values[9]
            }
            data.append(order_data)

        # Step 4: Save to CSV
        with open(OUTPUT_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

        print(f"Exported {len(data)} orders to {OUTPUT_FILE}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(fetch_orders())
