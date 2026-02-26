# Dex Scraper

## Overview
Dex Scraper is a Python-based web scraping tool designed to extract and process data from various online sources. This project aims to simplify the data collection process, making it easier for users to gather information efficiently.

## Features
- **Data Extraction**: Scrapes data from specified websites.
- **Token Processing**: Processes and stores tokens for further analysis.
- **Social Filter**: Only tokens with Telegram, X (Twitter) or Discord links are considered.
- **Multi‑channel Notifications**: Send alerts via Telegram, Discord (webhook), or X; configurable in the script.
- **Configurable Settings**: Allows users to customize scraping parameters through configuration files.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd dex_scraper
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
To run the scraper, execute the following command:
```bash
python3 scrapping.py
```

## Configuration
Most options live at the top of `scrapping.py` and can be adjusted directly or via environment variables.

- **TELEGRAM_TOKEN / CHAT_ID** – credentials for the Telegram bot.
- **DISCORD_WEBHOOK_URL** – paste your Discord channel webhook if you want Discord alerts.
- **X_API_* and X_ACCESS_*** – Twitter/X API keys & tokens for posting tweets.
- **NOTIFY_CHANNEL** – choose `'telegram'`, `'discord'` or `'x'` to select the delivery platform.

You can export these as env vars or hard‑code them for quick testing.

## Output
The scraped data will be saved in `processed_tokens.txt`, which prevents duplicate notifications by tracking seen token addresses.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Thanks to the open-source community for their contributions and support.

---
# dex-scrapper
🚀 DEX Scraper DEX Scraper is a multi-chain tool that finds early-stage tokens on DEXs in real time, filtering by market cap ≤ $20k, liquidity ≥ $100, and required Telegram or X links. Built for automation, it delivers clean data for bots, alerts, and Web3 systems — surfacing signal before noise. 🚀
