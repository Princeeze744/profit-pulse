import streamlit as st
import time
import random
import string
from datetime import datetime
import re

def rerun():
    """Universal rerun with professional handling"""
    # Check which rerun method is available
    if hasattr(st, 'rerun'):
        st.rerun()
    elif hasattr(st, 'experimental_rerun'):
        st.experimental_rerun()
    else:
        # Ultimate fallback - use session state to force refresh
        st.session_state.force_refresh = True
        time.sleep(1)
        st.experimental_rerun()

def generate_case_id() -> str:
    """Generate professional case ID"""
    timestamp = int(time.time())
    random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"LAW-{timestamp}-{random_suffix}"

def validate_email(email: str) -> bool:
    """Professional email validation"""
    if not email or len(email) > 254:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def format_phone_number(phone: str) -> str:
    """International phone formatting"""
    if not phone:
        return ""
    
    clean_phone = re.sub(r'\D', '', phone)
    
    if len(clean_phone) == 10:
        return f"+1 ({clean_phone[:3]}) {clean_phone[3:6]}-{clean_phone[6:]}"
    elif len(clean_phone) == 11 and clean_phone[0] == '1':
        return f"+1 ({clean_phone[1:4]}) {clean_phone[4:7]}-{clean_phone[7:]}"
    elif len(clean_phone) > 7:
        return f"+{clean_phone}"
    
    return phone

def get_status_color(status: str) -> str:
    """Professional status color scheme"""
    color_map = {
        "Intake": "#3B82F6",      # Blue
        "Review": "#F59E0B",      # Amber  
        "Accepted": "#10B981",    # Emerald
        "Active": "#8B5CF6",      # Violet
        "Closed": "#6B7280",      # Gray
        "Declined": "#EF4444"     # Red
    }
    return color_map.get(status, "#3B82F6")

def format_currency(amount: float) -> str:
    """Professional currency formatting"""
    if amount >= 1000000:
        return f"${amount/1000000:.2f}M"
    elif amount >= 1000:
        return f"${amount/1000:.1f}K"
    else:
        return f"${amount:,.2f}"

def calculate_days_since(date_string: str) -> int:
    """Calculate days since with error handling"""
    try:
        date_obj = datetime.fromisoformat(date_string)
        now = datetime.now()
        return (now - date_obj).days
    except:
        return 0

def create_success_message(title: str, message: str) -> str:
    """Create professional success message"""
    return f"""
    <div style='background: linear-gradient(135deg, #d4edda, #c3e6cb);
                padding: 1rem; border-radius: 10px; border-left: 4px solid #28a745;
                margin: 1rem 0; animation: slideIn 0.5s ease;'>
        <h4 style='color: #155724; margin: 0;'>✅ {title}</h4>
        <p style='color: #155724; margin: 0.5rem 0 0 0;'>{message}</p>
    </div>
    """