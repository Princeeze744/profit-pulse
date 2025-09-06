# Configuration settings for Profit Pulse
import os

# Airtable Configuration
AIRTABLE_CONFIG = {
    'API_KEY': 'patYRq0oq0LelxE4z.fc095b34992e746ba7ea1c8abada8fea69b42a4b5afa88a1545d7ab65fcf0e68',
    'BASE_ID': 'appCFeDzca0IXftmV',
    'TABLE_ID': 'tbl629FjMopfIHYfK'
}

# File Paths
CSV_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'trades.csv')

# Field Mappings (maps CSV columns to Airtable fields)
FIELD_MAPPING = {
    'Asset': 'Asset',
    'Date': 'Date',
    'Entry_Price': 'Entry Price',
    'Exit_Price': 'Exit Price',
    'Quantity': 'Quantity'
}