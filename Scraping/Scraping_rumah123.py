import csv, os, time, random
from playwright.sync_api import sync_playwright
import re

BASE_URL = "https://www.rumah123.com/jual/rumah/?page={}"
MAX_DATA = 3000
OUTPUT_FILE = os.path.join("..", "Data", "Raw", "rumah123_raw.csv")
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

# Ambil lokasi dari link
def ambil_lokasi_dari_link(link):
    try:
        m = re.search(r'/properti/([^/]+)/', link)
        if m:
            loc = m.group(1).replace('-', ' ').title()
            return loc
    except:
        pass
    return ""

def scraping_rumah123():
    collected = 0
    page_number = 1
    seen = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        # jangan ambil resource yang berat
        page.route("**/*", lambda route, request:
            route.abort() if request.resource_type in ["image","media","font","stylesheet"]
            else route.continue_()
        )

        # buat file + header kalau belum ada
        if not os.path.exists(OUTPUT_FILE):
            with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(["title","price","location","link"])

        print("\n MULAI SCRAPING...\n")

        try:
            while collected < MAX_DATA:
                print(f"Scraping page {page_number}...")

                # coba buka page, kalau gagal skip
                try:
                    page.goto(BASE_URL.format(page_number), wait_until="domcontentloaded", timeout=60000)
                except Exception as e:
                    print(f"Gagal membuka page {page_number}: {e}, lanjut ke page berikutnya")
                    page_number += 1
                    time.sleep(random.uniform(2,5))
                    continue

                # ambil semua link properti, title, dan harga
                links = page.query_selector_all("a[href*='/properti/']")
                titles = page.query_selector_all("h2")
                prices = page.query_selector_all("text=Rp")

                if len(links) == 0:
                    print("Tidak ada listing lagi, stop scraping.")
                    break

                rows = []
                for i in range(len(links)):
                    if collected >= MAX_DATA:
                        break

                    link = links[i].get_attribute("href")
                    if not link:
                        continue
                    if not link.startswith("http"):
                        link = "https://www.rumah123.com" + link
                    if link in seen:
                        continue
                    seen.add(link)

                    title = titles[i].inner_text() if i < len(titles) else ""
                    price = prices[i].inner_text() if i < len(prices) else ""
                    location = ambil_lokasi_dari_link(link)

                    rows.append([title.strip(), price.strip(), location, link])
                    collected += 1

                # CSV
                if rows:
                    with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
                        csv.writer(f).writerows(rows)

                print(f"Total terkumpul: {collected}\n")
                page_number += 1
                time.sleep(random.uniform(2,5))  # delay

        except KeyboardInterrupt:
            print("\nDihentikan manual, data aman.")

        finally:
            browser.close()
            print("\nSELESAI")
            print("File:", os.path.abspath(OUTPUT_FILE))
            print("Total data akhir:", collected)

if __name__ == "__main__":
    scraping_rumah123()
