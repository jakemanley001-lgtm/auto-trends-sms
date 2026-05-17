from pytrends.request import TrendReq
import smtplib
import os
from datetime import datetime

PHONE        = "4693389280"
CARRIER_GATE = "tmomail.net"
TO_EMAIL     = f"{PHONE}@{CARRIER_GATE}"
GMAIL_USER   = os.environ["GMAIL_USER"]
GMAIL_PASS   = os.environ["GMAIL_APP_PASSWORD"]

# Grouped by category — pytrends compares within each group
KEYWORD_GROUPS = [
    # Lighting
    ["Honda Civic LED tail lights", "Toyota Camry LED tail lights", "Honda Accord LED tail lights"],
    # Body kits & exterior
    ["Honda Civic body kit", "Toyota Camry body kit", "Honda Civic front lip"],
    # Carbon fiber & interior styling
    ["carbon fiber shift knob", "carbon fiber steering wheel", "carbon fiber mirror covers"],
    # Mods by model
    ["Honda Civic 11th gen mods", "Toyota Camry mods", "Honda Accord mods"],
    # Broad styling intent
    ["LED headlights upgrade", "power folding mirrors", "custom tail lights"],
]

def get_trends():
    pytrends = TrendReq(hl="en-US", tz=360)
    results = {}

    for group in KEYWORD_GROUPS:
        try:
            pytrends.build_payload(group, timeframe="now 7-d", geo="US")
            data = pytrends.interest_over_time()
            if data.empty:
                continue
            for kw in group:
                if kw in data.columns:
                    avg = int(data[kw].mean())
                    if kw not in results or avg > results[kw]:
                        results[kw] = avg
        except Exception:
            continue

    ranked = sorted(results.items(), key=lambda x: x[1], reverse=True)
    return ranked[:10]

def send_sms(message):
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_USER, GMAIL_PASS)
        server.sendmail(GMAIL_USER, TO_EMAIL, message)
    print("SMS sent.")

def main():
    trends = get_trends()
    date_str = datetime.now().strftime("%m/%d")
    lines = [f"HRS Trends {date_str}:"]
    for i, (kw, score) in enumerate(trends, 1):
        lines.append(f"{i}. {kw} ({score})")
    send_sms("\n".join(lines))

if __name__ == "__main__":
    main()
