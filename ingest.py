import requests
import os
from datetime import datetime

def get_facts(n=10):
    facts = []
    for i in range(n):
        try:
            response = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random?language=en")
            response.raise_for_status()
            data = response.json()
            facts.append(data)
        except requests.RequestException as e:
            print(f"Error fetching fact {i + 1}: {e}")
    return facts

def save_facts_as_txt(facts):
    if not facts:
        print("No data to save.")
        return

    os.makedirs("data/raw", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"data/raw/facts_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        for i, fact in enumerate(facts, 1):
            f.write(f"Fact {i}:\n")
            f.write(f"ID: {fact['id']}\n")
            f.write(f"Text: {fact['text']}\n")
            f.write(f"Source: {fact['source']}\n")
            f.write(f"Source URL: {fact['source_url']}\n")
            f.write(f"Permalink: {fact['permalink']}\n")
            f.write("-" * 60 + "\n")

    print(f"{len(facts)} facts saved to {filename}")

if __name__ == '__main__':
    facts_data = get_facts(10)
    save_facts_as_txt(facts_data)
