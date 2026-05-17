from pytrends.request import TrendReq
import requests
from datetime import datetime

PHONE = "4693389280"

SEED_KEYWORDS = [
    "JDM parts",
    "car accessories",
    "auto parts",
    "performance parts",
    "car mods",
    "drift parts",
    "JDM cars",
]

def get_trends():
    pytrends = TrendReq(hl="en-US", tz=360)
    seen = set()
    results = []

    for kw in SEED_KEYWORDS:
        try:
            pytrends.build_payload([kw], timeframe="now 7-d", geo="US")
            data = pytrends.related_queries()
            top = data.get(kw, {}).get("top")
            if top is not None:
                for _, row in top.head(5).iterrows():
                    q = row["query"].lower().strip()
                    if q not in seen:
                        seen.add(q)
                        results.append({
                            "query": row["query"],
                            "value": int(row["value"])
                        })
        except Exception:
            continue

    results.sort(key=lambda x: x["value"], reverse=True)
    return results[:10]

def send_sms(message):
    resp = requests.post("https://textbelt.com/text", {
        "phone": PHONE,
        "message": message,
        "key": "textbelt",
    })
    print(resp.json())

def main():
    trends = get_trends()
    date_str = datetime.now().strftime("%m/%d")
    lines = [f"Auto Trends {date_str}:"]
    for i, item in enumerate(trends, 1):
        lines.append(f"{i}. {item['query']}")
    lines.append("-- via Google Trends")
    send_sms("\n".join(lines))

if __name__ == "__main__":
    main()
