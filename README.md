# 🏠 Homeus - Georgian Real Estate Scraper

A production-ready real estate scraper for Georgian property websites (SS.ge and MyHome.ge) with Google Sheets integration and intelligent monitoring.

## ✨ Features

- **Multi-site scraping**: SS.ge and MyHome.ge support
- **Smart duplicate detection**: Hash-based property comparison
- **Google Sheets integration**: Automatic export of new properties
- **Precise data extraction**: Square meters, rooms, prices with currency detection
- **Intelligent scheduling**: Configurable scraping intervals
- **Production ready**: Docker support, logging, error handling
- **Respectful scraping**: Rate limiting and proper headers

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

```bash
git clone https://github.com/yourusername/homeus.git
cd homeus

# Run setup script
python setup.py
```

### Option 2: Manual Setup

```bash
git clone https://github.com/yourusername/homeus.git
cd homeus

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy example config
cp config/config.example.yaml config/config.yaml

# Edit configuration
nano config/config.yaml
```

### 3. Run

```bash
# Single scraping cycle
python src/main.py --once

# Continuous monitoring (every 5 minutes)
python src/main.py
```

## 📋 Configuration

The `config/config.yaml` file controls all aspects of the scraper:

### Basic Settings

```yaml
scraping:
  interval_minutes: 5 # How often to scrape
  max_pages: 10 # Maximum pages per search
  delay_between_requests: 2 # Seconds between requests
```

### Website Configuration

```yaml
websites:
  ss:
    enabled: true
    search_urls:
      - url: "https://home.ss.ge/ka/udzravi-qoneba/iyideba-bina?price_to=90000"
        name: "Apartments Under 90k USD"
```

### Google Sheets Integration

```yaml
google_sheets:
  enabled: true
  sheet_id: "your-google-sheet-id"
  service_account_file: "config/google_credentials.json"
```

## 🔧 Google Sheets Setup

1. **Create a Google Sheet** and note the Sheet ID from the URL
2. **Enable Google Sheets API** in Google Cloud Console
3. **Create Service Account** and download credentials JSON
4. **Share your sheet** with the service account email
5. **Place credentials** in `config/google_credentials.json`

Detailed setup guide: [GOOGLE_SHEETS_SETUP.md](GOOGLE_SHEETS_SETUP.md)

## 🐳 Docker Deployment

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f homeus

# Stop
docker-compose down
```

## 📊 Data Structure

Properties are extracted with the following fields:

| Field           | Description                 | Example                   |
| --------------- | --------------------------- | ------------------------- |
| `property_id`   | Unique identifier           | `ss_12345678`             |
| `title`         | Property title              | `იყიდება 3 ოთახიანი ბინა` |
| `price`         | Price in specified currency | `75000`                   |
| `currency`      | Currency code               | `USD`                     |
| `location`      | Property location           | `დიდი დიღომი`             |
| `size`          | Size in square meters       | `61.5`                    |
| `rooms`         | Number of rooms             | `3`                       |
| `property_type` | Type of property            | `apartment`               |

## 🔍 Supported Websites

### SS.ge

- ✅ Property listings
- ✅ Detailed property pages
- ✅ Price extraction (USD/GEL)
- ✅ Size extraction (m²)
- ✅ Room count
- ✅ Images

### MyHome.ge

- ✅ Property listings
- ✅ Basic property data
- ⚠️ Limited detail extraction (encoding issues)

## 📈 Monitoring

The scraper provides comprehensive logging:

```bash
# View logs
tail -f data/logs/homeus.log

# Database statistics
sqlite3 data/homeus.db "SELECT COUNT(*) as total_properties FROM properties;"
```

## 🛠️ Development

### Project Structure

```
homeus/
├── src/
│   ├── models/          # Data models
│   ├── scraper/         # Website scrapers
│   ├── storage/         # Database & Sheets
│   ├── utils/           # Utilities
│   └── main.py          # Entry point
├── config/
│   ├── config.example.yaml
│   └── google_credentials.json
├── data/
│   ├── homeus.db        # SQLite database
│   └── logs/            # Log files
└── docker-compose.yml
```

### Adding New Websites

1. Create scraper class inheriting from `BaseScraper`
2. Implement `scrape_listings()` and `scrape_property_details()`
3. Add website configuration to `config.yaml`
4. Register scraper in `main.py`

### Running Tests

```bash
# Test individual scrapers
python -c "from src.scraper.ss_scraper import SSScraper; print('SS scraper imported successfully')"

# Test database
python -c "from src.storage.database import Database; db = Database('test.db'); print('Database working')"
```

## 🚨 Rate Limiting & Ethics

This scraper is designed to be respectful:

- **2-second delays** between requests
- **Proper User-Agent** headers
- **Error handling** to avoid overwhelming servers
- **Configurable limits** on pages and requests

Please use responsibly and respect the websites' terms of service.

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/homeus/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/homeus/discussions)

## 🎯 Roadmap

- [ ] Additional Georgian real estate websites
- [ ] Price change notifications
- [ ] Web dashboard
- [ ] Property image downloading
- [ ] Advanced filtering options
- [ ] Telegram bot integration
- [ ] Email notifications

---

**Made with ❤️ for the Georgian real estate market**
