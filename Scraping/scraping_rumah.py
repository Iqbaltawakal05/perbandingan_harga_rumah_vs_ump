import csv, os, time, random, re
from playwright.sync_api import sync_playwright

BASE_URL = "https://www.rumah123.com/jual/rumah/?page={}"
MAKS_DATA = 3000
OUTPUT = "../Data/Raw/rumah123_raw.csv"
os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

def ambil_lokasi(link):
    cocok = re.search(r'/properti/([^/]+)/', link)
    return cocok.group(1).replace('-', ' ').title() if cocok else ""

def scraping_rumah():
    total_data, nomor_halaman = 0, 1
    sudah_ada = set()

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            halaman = browser.new_page()

            halaman.route("**/*", lambda r, req:
                r.abort() if req.resource_type in ["image","font","media","stylesheet"]
                else r.continue_()
            )

            print("\nMulai scraping data rumah...\n")

            while total_data < MAKS_DATA:
                print(f"Mengambil halaman {nomor_halaman}")

                try:
                    halaman.goto(BASE_URL.format(nomor_halaman), timeout=60000)
                except:
                    print("Gagal membuka halaman, lanjut ke halaman berikutnya")
                    nomor_halaman += 1
                    time.sleep(random.uniform(2,5))
                    continue

                daftar_link = halaman.query_selector_all("a[href*='/properti/']")
                daftar_judul = halaman.query_selector_all("h2")
                daftar_harga = halaman.query_selector_all("text=Rp")

                if not daftar_link:
                    break

                baris_data = []
                for i, a in enumerate(daftar_link):
                    if total_data >= MAKS_DATA:
                        break

                    link = a.get_attribute("href")
                    if not link:
                        continue

                    link = link if link.startswith("http") else "https://www.rumah123.com" + link
                    if link in sudah_ada:
                        continue
                    sudah_ada.add(link)

                    judul = daftar_judul[i].inner_text() if i < len(daftar_judul) else ""
                    harga = daftar_harga[i].inner_text() if i < len(daftar_harga) else ""
                    lokasi = ambil_lokasi(link)

                    baris_data.append([judul.strip(), harga.strip(), lokasi, link])
                    total_data += 1


                with open(OUTPUT, "a", newline="", encoding="utf-8") as f:
                    csv.writer(f).writerows(baris_data)

                print("Data terkumpul:", total_data)
                nomor_halaman += 1
                time.sleep(random.uniform(2,4))

    except KeyboardInterrupt:
        print("\nScraping dihentikan")
        print("Data tersimpan")

    except Exception as e:
        print("\nTerjadi kesalahan:", e)

    finally:
        print("\nProgram selesai")
        print("Total data akhir:", total_data)

if __name__ == "__main__":
    scraping_rumah()
