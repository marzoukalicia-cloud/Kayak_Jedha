import pandas as pd
from playwright.sync_api import sync_playwright

# ---------------------------------------------------------
# 1) Fonction Playwright robuste pour scraper une ville
# ---------------------------------------------------------

def scrape_booking_city(city, city_id):
    city_clean = city.replace(" ", "+")
    url = f"https://www.booking.com/searchresults.html?ss={city_clean}"

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        )

        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/123.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 800},
            locale="fr-FR"
        )

        page = context.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_selector("div[data-testid='property-card']", timeout=60000)
        cards = page.query_selector_all("div[data-testid='property-card']")

        hotels = []

        for card in cards[:10]:
            # Nom
            name = card.query_selector("div[data-testid='title']").inner_text()

            # URL
            link = card.query_selector("a[data-testid='title-link']").get_attribute("href")
            hotel_url = link if link.startswith("http") else "https://www.booking.com" + link

            # Score
            score_tag = card.query_selector("div[data-testid='review-score'] div:nth-child(1)")
            score = score_tag.inner_text().strip() if score_tag else None

            # --- Récupération des coordonnées sur la page de l'hôtel ---
            lat, lon = None, None
            detail_page = context.new_page()
            detail_page.goto(hotel_url, timeout=60000)

            try:
                detail_page.wait_for_selector("a[data-atlas-latlng]", timeout=30000)
                map_link = detail_page.query_selector("a[data-atlas-latlng]")
                if map_link:
                    coords = map_link.get_attribute("data-atlas-latlng")
                    if coords:
                        lat, lon = coords.split(",")
            except:
                pass
            finally:
                detail_page.close()
            # ------------------------------------------------------------

            hotels.append({
                "city_id": city_id,
                "city_name": city,
                "hotel_name": name,
                "url": hotel_url,
                "score": score,
                "latitude": lat,
                "longitude": lon
            })

        browser.close()
        return hotels


# ---------------------------------------------------------
# 2) Boucle Top‑5 + DataFrame final
# ---------------------------------------------------------
def scrape_top5_hotels():
    # Charger ton fichier des villes scorées
    df = pd.read_csv("city_scores_20january2026.csv")

    # Harmoniser les colonnes
    df = df.rename(columns={"city_id_x": "city_id"})
    df = df[["city_id", "city_name", "score"]]

    # Sélectionner le Top‑5
    top5 = df.sort_values("score", ascending=False).head(5)

    hotels_list = []

    for _, row in top5.iterrows():
        print(f"Scraping {row['city_name']}...")
        hotels = scrape_booking_city(row["city_name"], row["city_id"])
        hotels_list.extend(hotels)

    # DataFrame final
    df_hotels = pd.DataFrame(hotels_list)
    df_hotels.to_csv("hotels_top5.csv", index=False)

    print("\nScraping terminé ! Fichier généré : hotels_top5.csv")
    return df_hotels


# ---------------------------------------------------------
# 3) Exécution principale
# ---------------------------------------------------------
if __name__ == "__main__":
    df_hotels = scrape_top5_hotels()
    print(df_hotels.head())
