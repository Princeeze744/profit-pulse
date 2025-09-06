# Profit Pulse - Trading Performance Tracker

A Python application that tracks trading performance by importing trades from CSV to Airtable and generating detailed performance reports.

## Features

- 📊 Import trades from CSV to Airtable
- 📈 Calculate performance metrics (win rate, profit factor, etc.)
- 💰 Generate beautiful performance reports
- 🔄 Easy configuration for different Airtable bases

## Setup

1. Clone or download this project
2. Install requirements: `pip install -r requirements.txt`
3. Configure your Airtable details in `config/settings.py`
4. Place your trades CSV file in the `data` folder
5. Run the application: `python src/main.py`

## CSV Format

Your CSV file should have these columns:
- Asset (e.g., AAPL, TSLA)
- Date (YYYY-MM-DD)
- Entry_Price (number)
- Exit_Price (number)
- Quantity (number)

## Support

For issues or questions, please check the configuration settings or create an issue in the GitHub repository.