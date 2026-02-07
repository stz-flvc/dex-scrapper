import requests
import time
import os

# --- CONFIGURATION ---
# Replace these with your actual details from BotFather and @userinfobot
TELEGRAM_TOKEN = "8443595896:AAHe3PDymToHH_HhRvMqgNSD6fV-ojkxJYA"
CHAT_ID = "5859967688"
DB_FILE = "processed_tokens.txt"
SCAN_INTERVAL = 20  # Seconds between scans
# ---------------------

# --- FILTERS ---
MAX_MARKET_CAP = 20000    # Below $20,000
MIN_LIQUIDITY = 100       # Above $100
SCAN_INTERVAL = 30        # Seconds between scans


def load_seen():
    if not os.path.exists(DB_FILE):
        return set()
    with open(DB_FILE, "r") as f:
        return set(line.strip() for line in f if line.strip())


def save_seen(address):
    with open(DB_FILE, "a") as f:
        f.write(f"{address}\n")


def send_tg(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, data=payload)


def get_market_data(chain, address):
    """Fetches real-time MC and Liquidity for a specific token."""
    try:
        url = f"https://api.dexscreener.com/latest/dex/tokens/{address}"
        res = requests.get(url, timeout=10).json()
        pairs = res.get('pairs', [])
        if not pairs:
            return None

        # We take the primary pair (usually the first one)
        main_pair = pairs[0]
        return {
            "liquidity": float(main_pair.get('liquidity', {}).get('usd', 0)),
            # FDV is used as Market Cap for new tokens
            "mcap": float(main_pair.get('fdv', 0)),
            "pair_url": main_pair.get('url')
        }
    except:
        return None


def scan_dex():
    seen = load_seen()
    # Pulling from Token Profiles as the 'discovery' source
    discovery_url = "https://api.dexscreener.com/token-profiles/latest/v1"

    try:
        response = requests.get(discovery_url, timeout=10).json()
        for token in response:
            addr = token.get('tokenAddress')
            chain = token.get('chainId')

            if addr in seen:
                continue

            # Check Socials First
            links = token.get('links', [])
            link_types = [l.get('type', '').lower() for l in links]
            has_x = any(lt in ['twitter', 'x'] for lt in link_types)
            has_tg = 'telegram' in link_types

            if has_x or has_tg:
                # Check Market Data
                stats = get_market_data(chain, addr)
                if stats:
                    liq = stats['liquidity']
                    mcap = stats['mcap']

                    # APPLY YOUR FILTERS
                    if liq >= MIN_LIQUIDITY and mcap <= MAX_MARKET_CAP:
                        msg = (
                            f"🎯 *Target Found (MC < 20k)*\n\n"
                            f"🏷️ *Name:* {token.get('header', 'Unknown')}\n"
                            f"💰 *MCap:* `${mcap:,.2f}`\n"
                            f"💧 *Liq:* `${liq:,.2f}`\n"
                            f"🌐 *Chain:* {chain}\n"
                            f"📍 ` {addr} `\n\n"
                            f"🔗 [DEX Screener]({stats['pair_url']})"
                        )
                        send_tg(msg)
                        save_seen(addr)
                        seen.add(addr)
                        print(f"✅ Notified: {addr} (MC: {mcap})")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    print("🚀 Scraper started with MC < 20k and Liq > $100 filters...")
    while True:
        scan_dex()
        time.sleep(SCAN_INTERVAL)
