import requests
from bs4 import BeautifulSoup
import pandas as pd

with open("data/nonfatals.txt", "r") as f:
    urls = [line.strip() for line in f if line.strip()]

all_data = []

for url in urls:
    print(f"Scraping: {url}")
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        crash_details = soup.find("div", class_="crash-details")
        if not crash_details:
            print(f"⚠️ Skipping (no crash-details): {url}")
            continue

        data = {"URL": url}
        for div in crash_details.find_all("div", recursive=False):
            label_span = div.find("span", class_="crash-label")
            if label_span:
                label = label_span.text.strip().replace(":", "")
                value = div.get_text().replace(label_span.text, "").strip()
                data[label] = value

        all_data.append(data)

    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        
df = pd.DataFrame(all_data)
df.to_csv("data/nonfatalsdata.csv", index=False)
print("Scraping completed and saved to data/output.csv")
