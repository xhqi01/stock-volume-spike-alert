# Stock Volume Monitor

Monitors a watchlist of US stocks and sends an email alert when trading volume spikes significantly above the 20-day average — a common signal of unusual buying or selling activity.

## How it works

Every 30 minutes, the script fetches the latest daily data from Yahoo Finance (15-minute delay) and compares today's volume against the 20-day average. If a stock's volume exceeds the threshold (default: 3x average), an email alert is sent with the ticker, price, price change, and volume ratio.

## Setup

**1. Clone the repo**

```bash
git clone https://github.com/xhqi01/stock-volume-monitor.git
cd stock-volume-monitor
pip install -r requirements.txt
```

**2. Create your `.env` file**

```bash
cp .env.example .env
```

Then edit `.env` with your details:

```
EMAIL_SENDER=you@gmail.com
EMAIL_PASSWORD=xxxx xxxx xxxx xxxx
EMAIL_RECEIVER=you@gmail.com
VOLUME_THRESHOLD=3.0
CHECK_INTERVAL=1800
```

> Gmail App Password: go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords) and generate one. This is different from your login password.

**3. Edit your watchlist**

Open `monitor.py` and edit the `WATCHLIST` at the top:

```python
WATCHLIST = ["AAPL", "MSFT", "NVDA", "TSLA", ...]
```

**4. Run locally**

```bash
python monitor.py
```

## Deploy to Render (runs 24/7 for free)

1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → New → **Background Worker**
3. Connect your GitHub repo
4. Set **Build Command**: `pip install -r requirements.txt`
5. Set **Start Command**: `python monitor.py`
6. Under **Environment**, add your variables from `.env`
7. Click Deploy

## Configuration

| Variable | Default | Description |
|---|---|---|
| `EMAIL_SENDER` | — | Your Gmail address |
| `EMAIL_PASSWORD` | — | Gmail App Password |
| `EMAIL_RECEIVER` | — | Where to send alerts |
| `VOLUME_THRESHOLD` | `3.0` | Alert if volume exceeds this multiple of 20-day avg |
| `CHECK_INTERVAL` | `1800` | Scan interval in seconds (1800 = 30 min) |

## Notes

- Data is from Yahoo Finance with a 15-minute delay — not suitable for real-time trading
- Never commit your `.env` file (already in `.gitignore`)

---

# Stock Volume Monitor（日本語）

米国株のウォッチリストを監視し、出来高が20日平均を大幅に上回った場合にメールで通知するツールです。

## 仕組み

30分ごとにYahoo Financeからデータを取得し、当日の出来高を20日平均と比較します。設定した閾値（デフォルト：3倍）を超えた場合、ティッカー・価格・価格変動率・出来高比率をメールで通知します。

## セットアップ

**1. クローン**

```bash
git clone https://github.com/xhqi01/stock-volume-monitor.git
cd stock-volume-monitor
pip install -r requirements.txt
```

**2. `.env` ファイルを作成**

```bash
cp .env.example .env
```

`.env` を編集：

```
EMAIL_SENDER=you@gmail.com
EMAIL_PASSWORD=xxxx xxxx xxxx xxxx
EMAIL_RECEIVER=you@gmail.com
VOLUME_THRESHOLD=3.0
CHECK_INTERVAL=1800
```

> GmailのアプリパスワードはGoogleアカウントの [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords) で生成してください。

**3. ウォッチリストを編集**

`monitor.py` の先頭にある `WATCHLIST` を編集：

```python
WATCHLIST = ["AAPL", "MSFT", "NVDA", "TSLA", ...]
```

**4. ローカルで実行**

```bash
python monitor.py
```

## Renderへのデプロイ（24時間稼働・無料）

1. このリポジトリをGitHubにプッシュ
2. [render.com](https://render.com) → New → **Background Worker**
3. GitHubリポジトリを接続
4. **Build Command**：`pip install -r requirements.txt`
5. **Start Command**：`python monitor.py`
6. **Environment** に `.env` の変数を追加
7. Deployをクリック

## 注意事項

- データはYahoo Financeから取得（15分遅延）。リアルタイムトレードには不向きです
- `.env` ファイルは絶対にコミットしないでください（`.gitignore` 設定済み）
