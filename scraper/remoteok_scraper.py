# scraper/remoteok_scraper.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

def scrape_remoteok():
    """
    Scrapes developer/data job listings from RemoteOK and saves them to a CSV file.
    """

    print("🔍 Starting scrape...")

    url = "https://remoteok.com/remote-dev+data-jobs"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []
    rows = soup.select("tr.job")

    print(f"✅ Found {len(rows)} job listings")

    for row in rows:
        try:
            title = row.select_one("h2").text.strip()
            company = row.select_one("h3").text.strip()
            location = row.select_one(".location")
            location_text = location.text.strip() if location else "Remote"
            tags = [tag.text for tag in row.select(".tag")]
            link = "https://remoteok.com" + row["data-href"]

            jobs.append({
                "title": title,
                "company": company,
                "location": location_text,
                "tags": ", ".join(tags),
                "link": link,
                "scraped_on": datetime.date.today().isoformat()
            })

        except Exception as e:
            print("⚠️ Skipping a job due to error:", e)

    df = pd.DataFrame(jobs)
    df.to_csv("data/remoteok_jobs.csv", index=False)
    print(f"📁 Saved {len(df)} job listings to data/remoteok_jobs.csv")

if __name__ == "__main__":
    scrape_remoteok()

