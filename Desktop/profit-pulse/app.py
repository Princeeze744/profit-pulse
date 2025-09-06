from flask import Flask, render_template, request, flash, redirect, url_for
import pandas as pd
from pyairtable import Api
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'profit_pulse_secret_key_2023'

# Airtable Configuration
AIRTABLE_API_KEY = "patYRq0oq0LelxE4z.fc095b34992e746ba7ea1c8abada8fea69b42a4b5afa88a1545d7ab65fcf0e68"
AIRTABLE_BASE_ID = "appCFeDzca0IXftmV"
TABLE_ID = "tbl629FjMopfIHYfK"

# Initialize Airtable API
api = Api(AIRTABLE_API_KEY)
table = api.table(AIRTABLE_BASE_ID, TABLE_ID)

def calculate_metrics(records):
    """Calculate performance metrics from Airtable records"""
    if not records:
        return None
    
    total_trades = len(records)
    total_profit = 0
    winning_trades = 0
    losing_trades = 0
    total_win = 0
    total_loss = 0
    
    for record in records:
        pnl = record['fields'].get('Pnl 2', 0)
        # Skip records with formula errors
        if isinstance(pnl, str) and pnl.startswith('#ERROR!'):
            continue
            
        total_profit += pnl
        
        if pnl > 0:
            winning_trades += 1
            total_win += pnl
        elif pnl < 0:
            losing_trades += 1
            total_loss += abs(pnl)
    
    # Calculate metrics
    win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
    average_profit = total_profit / total_trades if total_trades > 0 else 0
    profit_factor = total_win / total_loss if total_loss > 0 else "N/A (No losses)"
    
    return {
        "total_trades": total_trades,
        "winning_trades": winning_trades,
        "losing_trades": losing_trades,
        "win_rate": round(win_rate, 2),
        "total_profit": round(total_profit, 2),
        "average_profit": round(average_profit, 2),
        "profit_factor": profit_factor,
        "total_win": round(total_win, 2),
        "total_loss": round(total_loss, 2),
        "analysis_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle CSV file upload and process trades"""
    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(request.url)
    
    if file and file.filename.endswith('.csv'):
        try:
            # Read the CSV file
            df = pd.read_csv(file)
            
            # Check required columns
            required_columns = ['Asset', 'Date', 'Entry_Price', 'Exit_Price', 'Quantity']
            if not all(col in df.columns for col in required_columns):
                flash('CSV file must contain columns: Asset, Date, Entry_Price, Exit_Price, Quantity', 'error')
                return redirect(request.url)
            
            # Import trades to Airtable
            trades_imported = 0
            for _, row in df.iterrows():
                # Prepare the data for Airtable
                trade_data = {
                    "Asset": row["Asset"],
                    "Date": row["Date"],
                    "Entry Price": float(row["Entry_Price"]),
                    "Exit Price": float(row["Exit_Price"]),
                    "Quantity": float(row["Quantity"]),
                }
                
                # Add Type if available in CSV
                if "Type" in df.columns:
                    trade_data["Type"] = row["Type"]
                
                table.create(trade_data)
                trades_imported += 1
            
            flash(f'Successfully imported {trades_imported} trades!', 'success')
            
            # Calculate and display metrics
            records = table.all()
            metrics = calculate_metrics(records)
            
            return render_template('index.html', metrics=metrics)
            
        except Exception as e:
            flash(f'Error processing file: {str(e)}', 'error')
            return redirect(request.url)
    
    else:
        flash('Please upload a CSV file', 'error')
        return redirect(request.url)

@app.route('/analyze')
def analyze():
    """Analyze existing trades in Airtable"""
    try:
        records = table.all()
        metrics = calculate_metrics(records)
        
        if metrics:
            flash('Analysis completed successfully!', 'success')
            return render_template('index.html', metrics=metrics)
        else:
            flash('No trades found in the database', 'error')
            return redirect(url_for('index'))
            
    except Exception as e:
        flash(f'Error analyzing data: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/sample')
def download_sample():
    """Provide a sample CSV file for download"""
    sample_data = """Asset,Date,Entry_Price,Exit_Price,Quantity,Type
EUR/USD,2023-10-01,1.1580,1.1620,10000,Long
GBP/USD,2023-10-02,1.3150,1.3100,15000,Short
USD/JPY,2023-10-03,110.50,111.20,20000,Long
AUD/USD,2023-10-04,0.7250,0.7300,12000,Long
USD/CAD,2023-10-05,1.2650,1.2600,18000,Short"""
    
    return sample_data, 200, {
        'Content-Type': 'text/csv',
        'Content-Disposition': 'attachment; filename=profit_pulse_sample.csv'
    }

if __name__ == '__main__':
    app.run(debug=True)