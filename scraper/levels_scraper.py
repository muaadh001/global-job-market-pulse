# scraper/levels_scraper.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

# Define headers with a user-agent string
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# Target URL (this page lists companies and salaries)
url = "https://www.levels.fyi/salaries/"

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

# Data storage
data = []

# Loop through job listings in the table
for row in soup.select("table tr")[1:]:  # Skip the header row
    cells = row.find_all("td")
    if len(cells) < 5:
        continue

    company = cells[0].text.strip()
    title = cells[1].text.strip()
    location = cells[2].text.strip()
    total_pay = cells[3].text.strip()
    updated = cells[4].text.strip()

    data.append({
        "Company": company,
        "Title": title,
        "Location": location,
        "Total Compensation": total_pay,
        "Last Updated": updated
    })

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv("data/levels_fyi_salaries.csv", index=False)

print(f"✅ Scraped {len(df)} job listings and saved to /data/levels_fyi_salaries.csv")


