import csv, os, time, random, re
from playwright.sync_api import sync_playwright, TimeoutError

BASE_URL = "https://www.rumah123.com/jual/rumah/?page={}"
MAKS_DATA = 2000
OUTPUT = "../Data/Raw/rumah123_raw.csv"
os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

def ambil_lokasi(link):
    cocok = re.search(r'/properti/([^/]+)/', link)
    return cocok.group(1).replace('-', ' ').title() if cocok else ""

def scraping_rumah():
    total_data, nomor_halaman = 0, 1
    sudah_ada = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)

        halaman = browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width":1280, "height":800}
        )

        halaman.route("**/*", lambda r, req:
            r.abort() if req.resource_type in ["image","media","font"]
            else r.continue_()
        )

        print("\nMulai scraping...\n")

        with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(["title","price","location","link"])

        while total_data < MAKS_DATA:
            print(f"Halaman {nomor_halaman}")

            try:
                halaman.goto(BASE_URL.format(nomor_halaman), timeout=60000)
            except:
                print("Gagal membuka halaman, lanjut ke halaman berikutnya")
                nomor_halaman += 1
                time.sleep(random.uniform(2,5))
                continue

            cards = halaman.query_selector_all("div:has(a[href*='/properti/'])")

            if not cards:
                print("Tidak ada card, stop.")
                break

            baris_data = []

            for card in cards:
                if total_data >= MAKS_DATA:
                    break

                link_el = card.query_selector("a[href*='/properti/']")
                if not link_el:
                    continue

                link = link_el.get_attribute("href")
                if not link:
                    continue

                link = link if link.startswith("http") else "https://www.rumah123.com" + link
                if link in sudah_ada:
                    continue
                sudah_ada.add(link)

                try:
                    title = card.query_selector("h2").inner_text().strip()
                except:
                    title = ""

                try:
                    price = card.query_selector("text=Rp").inner_text().strip()
                except:
                    continue

                location = ambil_lokasi(link)

                baris_data.append([title, price, location, link])
                total_data += 1

            with open(OUTPUT, "a", newline="", encoding="utf-8") as f:
                csv.writer(f).writerows(baris_data)

            print(f"Total data: {total_data}")

            nomor_halaman += 1
            time.sleep(random.uniform(4,7))

        browser.close()
        print("\nScraping selesai.")
        print("Total data:", total_data)

if __name__ == "__main__":
    scraping_rumah()
