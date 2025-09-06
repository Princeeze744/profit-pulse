import streamlit as st
import pandas as pd
from pyairtable import Api
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Profit Pulse - Trading Performance Tracker",
    page_icon="📊",
    layout="wide"
)

# Initialize Airtable API
def init_airtable():
    try:
        api = Api(st.secrets["AIRTABLE_API_KEY"])
        return api.table(st.secrets["AIRTABLE_BASE_ID"], st.secrets["TABLE_ID"])
    except Exception as e:
        st.error(f"Failed to connect to Airtable: {e}")
        return None

# Calculate metrics function
def calculate_metrics(records):
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

# Main app
def main():
    st.title("📊 Profit Pulse")
    st.markdown("### Trading Performance Tracker")
    
    # Initialize Airtable
    table = init_airtable()
    if table is None:
        return
    
    # File upload section
    st.header("📤 Upload Your Trades")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            # Check required columns
            required_columns = ['Asset', 'Date', 'Entry_Price', 'Exit_Price', 'Quantity']
            if not all(col in df.columns for col in required_columns):
                st.error("CSV file must contain: Asset, Date, Entry_Price, Exit_Price, Quantity")
                return
            
            # Show preview
            st.subheader("Data Preview")
            st.dataframe(df.head())
            
            if st.button("Upload to Airtable"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                trades_imported = 0
                total_rows = len(df)
                
                for i, row in df.iterrows():
                    trade_data = {
                        "Asset": row["Asset"],
                        "Date": row["Date"],
                        "Entry Price": float(row["Entry_Price"]),
                        "Exit Price": float(row["Exit_Price"]),
                        "Quantity": float(row["Quantity"]),
                    }
                    
                    if "Type" in df.columns:
                        trade_data["Type"] = row["Type"]
                    
                    table.create(trade_data)
                    trades_imported += 1
                    progress_bar.progress((i + 1) / total_rows)
                    status_text.text(f"Imported {trades_imported} of {total_rows} trades...")
                
                st.success(f"Successfully imported {trades_imported} trades!")
                
        except Exception as e:
            st.error(f"Error processing file: {e}")
    
    # Analysis section
    st.header("📈 Performance Analysis")
    
    if st.button("Analyze Trades"):
        try:
            records = table.all()
            metrics = calculate_metrics(records)
            
            if metrics:
                st.subheader("Performance Report")
                st.write(f"**Analysis Date:** {metrics['analysis_date']}")
                
                # Create metrics columns
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Trades", metrics['total_trades'])
                    st.metric("Winning Trades", metrics['winning_trades'])
                    st.metric("Losing Trades", metrics['losing_trades'])
                
                with col2:
                    st.metric("Win Rate", f"{metrics['win_rate']}%")
                    st.metric("Total Profit", f"${metrics['total_profit']}")
                    st.metric("Average Profit", f"${metrics['average_profit']}")
                
                with col3:
                    st.metric("Profit Factor", metrics['profit_factor'])
                    st.metric("Total Wins", f"${metrics['total_win']}")
                    st.metric("Total Losses", f"${metrics['total_loss']}")
                
                st.success("Analysis completed successfully!")
            else:
                st.warning("No trades found in the database")
                
        except Exception as e:
            st.error(f"Error analyzing data: {e}")
    
    # Sample file section
    st.header("📝 Sample CSV File")
    sample_data = """Asset,Date,Entry_Price,Exit_Price,Quantity,Type
EUR/USD,2023-10-01,1.1580,1.1620,10000,Long
GBP/USD,2023-10-02,1.3150,1.3100,15000,Short
USD/JPY,2023-10-03,110.50,111.20,20000,Long"""
    
    st.download_button(
        label="Download Sample CSV",
        data=sample_data,
        file_name="profit_pulse_sample.csv",
        mime="text/csv"
    )

if __name__ == "__main__":
    main()