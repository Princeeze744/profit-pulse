import streamlit as st
import hashlib
from datetime import datetime

def init_authentication():
    """Initialize authentication system"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_role' not in st.session_state:
        st.session_state.user_role = 'guest'
    if 'user_name' not in st.session_state:
        st.session_state.user_name = 'Guest User'

def hash_password(password):
    """Hash password for security"""
    return hashlib.sha256(password.encode()).hexdigest()

def check_credentials(username, password):
    """Check user credentials with professional roles"""
    users = {
        'admin': {
            'password_hash': hash_password('admin123'),
            'role': 'Administrator',
            'name': 'System Admin',
            'permissions': ['all']
        },
        'partner': {
            'password_hash': hash_password('partner123'),
            'role': 'Senior Partner', 
            'name': 'Legal Partner',
            'permissions': ['cases', 'clients', 'billing', 'reports']
        },
        'associate': {
            'password_hash': hash_password('associate123'),
            'role': 'Legal Associate',
            'name': 'Junior Associate',
            'permissions': ['cases', 'clients']
        },
        'demo': {
            'password_hash': hash_password('demo123'),
            'role': 'Demo User',
            'name': 'Demo Account',
            'permissions': ['cases', 'clients', 'reports']
        }
    }
    
    if username in users and users[username]['password_hash'] == hash_password(password):
        return users[username]
    return None

def login_form():
    """Professional login form with animations"""
    st.markdown("""
    <style>
    .login-container {
        max-width: 400px;
        margin: 2rem auto;
        padding: 2rem;
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        animation: slideIn 0.5s ease;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    
    # Logo and Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://via.placeholder.com/100x100/1a237e/ffffff?text=⚖️", width=100)
    
    st.markdown("<h1 style='text-align: center; color: #1a237e;'>LegalAI Enterprise</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>Professional Legal Case Management</p>", unsafe_allow_html=True)
    
    # Login Form
    with st.form("professional_login"):
        st.subheader("🔐 Secure Login")
        
        username = st.text_input("👤 Username", placeholder="Enter your username")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
        remember_me = st.checkbox("Remember me for 30 days")
        
        submitted = st.form_submit_button("Login to System", type="primary", use_container_width=True)
        
        if submitted:
            user_data = check_credentials(username, password)
            if user_data:
                st.session_state.authenticated = True
                st.session_state.user_role = user_data['role']
                st.session_state.user_name = user_data['name']
                st.session_state.login_time = datetime.now()
                
                # Success message
                st.success(f"🎉 Welcome back, {user_data['name']}!")
                st.balloons()
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Please try again.")
    
    # Demo credentials
    st.markdown("---")
    st.markdown("### 🚀 Demo Access")
    st.code("Username: demo\nPassword: demo123", language="text")
    
    st.markdown("</div>", unsafe_allow_html=True)

def require_auth():
    """Decorator to require authentication"""
    if not st.session_state.get('authenticated', False):
        login_form()
        st.stop()
    return True