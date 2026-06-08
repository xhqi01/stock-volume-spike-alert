import os
import time
import smtplib
import yfinance as yf
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

# ── CONFIG ────────────────────────────────────────────────────────────────────
EMAIL_SENDER   = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# Stocks to monitor (add/remove as you like)
WATCHLIST = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA",
    "META", "TSLA", "AMD", "NFLX", "BABA"
]

# Alert if today's volume is this many times higher than the 20-day average
VOLUME_THRESHOLD = float(os.getenv("VOLUME_THRESHOLD", "3.0"))

# How often to check (seconds). Default: every 30 minutes.
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "1800"))

# ── EMAIL ─────────────────────────────────────────────────────────────────────
def send_email(subject, body):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = EMAIL_SENDER
    msg["To"]      = EMAIL_RECEIVER
    msg.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        print(f"  ✓ Email sent: {subject}")
    except Exception as e:
        print(f"  ✗ Email failed: {e}")

# ── DETECTION ─────────────────────────────────────────────────────────────────
def check_volume_spike(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist  = stock.history(period="25d", interval="1d")

        if len(hist) < 5:
            return None

        avg_volume     = hist["Volume"].iloc[:-1].mean()  # 20-day avg (excl. today)
        today_volume   = hist["Volume"].iloc[-1]
        today_close    = hist["Close"].iloc[-1]
        prev_close     = hist["Close"].iloc[-2]
        price_change   = ((today_close - prev_close) / prev_close) * 100
        volume_ratio   = today_volume / avg_volume if avg_volume > 0 else 0

        if volume_ratio >= VOLUME_THRESHOLD:
            return {
                "ticker":       ticker,
                "today_volume": int(today_volume),
                "avg_volume":   int(avg_volume),
                "ratio":        round(volume_ratio, 2),
                "price":        round(today_close, 2),
                "change_pct":   round(price_change, 2),
            }
    except Exception as e:
        print(f"  ✗ Error fetching {ticker}: {e}")
    return None

# ── EMAIL BODY ────────────────────────────────────────────────────────────────
def build_email(alerts):
    rows = ""
    for a in alerts:
        color  = "#2ecc71" if a["change_pct"] >= 0 else "#e74c3c"
        arrow  = "▲" if a["change_pct"] >= 0 else "▼"
        rows += f"""
        <tr>
          <td style="padding:10px 14px;font-weight:600">{a["ticker"]}</td>
          <td style="padding:10px 14px">${a["price"]}</td>
          <td style="padding:10px 14px;color:{color}">{arrow} {abs(a["change_pct"])}%</td>
          <td style="padding:10px 14px">{a["today_volume"]:,}</td>
          <td style="padding:10px 14px;color:#e67e22;font-weight:600">{a["ratio"]}x avg</td>
        </tr>"""

    return f"""
    <html><body style="font-family:monospace;background:#f7f6f3;padding:32px">
    <div style="max-width:600px;margin:0 auto;background:#fff;border:1px solid #ddd;padding:28px">
      <h2 style="margin:0 0 4px;font-size:16px">📈 Volume Spike Alert</h2>
      <p style="margin:0 0 20px;color:#888;font-size:13px">
        {len(alerts)} stock{"s" if len(alerts) > 1 else ""} detected · {VOLUME_THRESHOLD}x average volume threshold
      </p>
      <table style="width:100%;border-collapse:collapse;font-size:13px">
        <thead>
          <tr style="border-bottom:2px solid #eee;color:#aaa;text-transform:uppercase;font-size:11px">
            <th style="padding:8px 14px;text-align:left">Ticker</th>
            <th style="padding:8px 14px;text-align:left">Price</th>
            <th style="padding:8px 14px;text-align:left">Change</th>
            <th style="padding:8px 14px;text-align:left">Volume</th>
            <th style="padding:8px 14px;text-align:left">vs Avg</th>
          </tr>
        </thead>
        <tbody>{rows}</tbody>
      </table>
      <p style="margin:20px 0 0;font-size:11px;color:#bbb">
        Data from Yahoo Finance (15min delay) · stock-volume-monitor
      </p>
    </div>
    </body></html>"""

# ── MAIN LOOP ─────────────────────────────────────────────────────────────────
def main():
    print(f"Stock Volume Monitor started")
    print(f"  Watchlist  : {', '.join(WATCHLIST)}")
    print(f"  Threshold  : {VOLUME_THRESHOLD}x average volume")
    print(f"  Interval   : {CHECK_INTERVAL}s ({CHECK_INTERVAL // 60} min)")
    print(f"  Sending to : {EMAIL_RECEIVER}")
    print()

    while True:
        print(f"[scan] Checking {len(WATCHLIST)} stocks…")
        alerts = []

        for ticker in WATCHLIST:
            result = check_volume_spike(ticker)
            if result:
                print(f"  ⚡ {ticker}: {result['ratio']}x volume spike")
                alerts.append(result)
            else:
                print(f"  · {ticker}: normal")

        if alerts:
            subject = f"⚡ Volume Spike: {', '.join(a['ticker'] for a in alerts)}"
            body    = build_email(alerts)
            send_email(subject, body)
        else:
            print("  No spikes detected.")

        print(f"  Next check in {CHECK_INTERVAL // 60} minutes.\n")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
