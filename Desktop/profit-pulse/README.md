# Profit Pulse - Trading Performance Tracker

A web application that tracks trading performance by importing trades from CSV to Airtable and generating detailed performance reports.

## Features

- 📊 Import trades from CSV to Airtable
- 📈 Calculate performance metrics (win rate, profit factor, etc.)
- 💰 Generate beautiful performance reports
- 🌐 Web-based interface (no installation required)

## Live Demo

Try the live app: [https://your-app-name.streamlit.app/](https://your-app-name.streamlit.app/)

## How to Use

1. Prepare a CSV file with your trading data
2. Upload the CSV file to the web app
3. Click "Upload to Airtable" to import your trades
4. Click "Analyze Trades" to generate a performance report

## CSV Format

Your CSV file should have these columns:
- Asset (e.g., AAPL, EUR/USD)
- Date (YYYY-MM-DD)
- Entry_Price (number)
- Exit_Price (number)
- Quantity (number)
- Type (Long or Short, optional)

## Technology Stack

- Python
- Streamlit
- Airtable API
- Pandas

## License

MIT License - feel free to use this project for your own purposes!