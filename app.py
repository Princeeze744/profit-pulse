import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import json
import requests
from typing import Dict, List, Optional
import plotly.express as px
import plotly.graph_objects as go

# Import from our modules
from database import (
    load_cases, save_cases, update_case_status, get_case_by_id,
    add_time_entry, get_time_entries, add_case_note, get_case_notes,
    delete_case, export_cases_to_csv, get_case_statistics
)
from ai_analysis import (
    simulate_ai_analysis, analyze_case_complexity, 
    constitutional_analysis, legal_precedent_analysis,
    risk_assessment_analysis, generate_legal_strategy
)
from utils import (
    generate_case_id, validate_email, format_phone_number, 
    get_status_color, rerun, format_currency, calculate_days_since
)
from legal_database import LEGAL_DATABASE, COUNTRIES, LEGAL_SYSTEMS
from auth import require_auth, login_form
from config import ENTERPRISE_CONFIG, UI_CONFIG

# Page configuration with professional settings
st.set_page_config(
    page_title="⚖️ LegalAI Enterprise - Professional Case Management",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://legalaipro.com/support',
        'Report a bug': 'https://github.com/legalaipro/issues',
        'About': 'LegalAI Enterprise v3.0 • Professional Legal Case Management'
    }
)

# 🎨 PROFESSIONAL CSS WITH ANIMATIONS
st.markdown(f"""
<style>
    /* Main Theme */
    .main-header {{
        font-size: 3rem;
        background: linear-gradient(135deg, {UI_CONFIG['colors']['primary']}, {UI_CONFIG['colors']['secondary']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 800;
        animation: fadeIn 1s ease-in;
    }}
    
    /* Cards with hover effects */
    .enterprise-card {{
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 2rem;
        border-radius: 20px;
        border-left: 6px solid {UI_CONFIG['colors']['primary']};
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border: 1px solid #e9ecef;
    }}
    
    .enterprise-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }}
    
    .urgent-case {{
        border-left: 6px solid #dc3545;
        background: linear-gradient(135deg, #fff5f5 0%, #ffeaea 100%);
        animation: pulse 2s infinite;
    }}
    
    .success-case {{
        border-left: 6px solid #28a745;
        background: linear-gradient(135deg, #f0fff4 0%, #e6ffe6 100%);
    }}
    
    /* Metrics Cards */
    .metric-card {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }}
    
    .metric-card:hover {{
        transform: scale(1.05);
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }}
    
    /* Animations */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    @keyframes pulse {{
        0% {{ box-shadow: 0 0 0 0 rgba(220, 53, 69, 0.4); }}
        70% {{ box-shadow: 0 0 0 10px rgba(220, 53, 69, 0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(220, 53, 69, 0); }}
    }}
    
    @keyframes slideIn {{
        from {{ transform: translateX(-100%); opacity: 0; }}
        to {{ transform: translateX(0); opacity: 1; }}
    }}
    
    /* Form Styling */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {{
        border-radius: 10px !important;
        border: 2px solid #e9ecef !important;
        transition: all 0.3s ease !important;
    }}
    
    .stTextInput input:focus, .stTextArea textarea:focus, .stSelectbox select:focus {{
        border-color: {UI_CONFIG['colors']['primary']} !important;
        box-shadow: 0 0 0 3px rgba(26, 35, 126, 0.1) !important;
    }}
    
    /* Button Styling */
    .stButton button {{
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
    }}
    
    .stButton button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }}
    
    /* Progress Bars */
    .stProgress > div > div > div > div {{
        background-color: {UI_CONFIG['colors']['primary']};
        border-radius: 10px;
    }}
    
    /* Custom Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 2rem;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        height: 50px;
        white-space: pre-wrap;
        border-radius: 10px 10px 0px 0px;
        gap: 1rem;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: {UI_CONFIG['colors']['primary']} !important;
        color: white !important;
    }}
    
    /* Mobile Responsive */
    @media (max-width: 768px) {{
        .main-header {{
            font-size: 2rem;
        }}
        .enterprise-card {{
            padding: 1rem;
            margin-bottom: 1rem;
        }}
        .metric-card {{
            padding: 1rem;
            margin-bottom: 1rem;
        }}
    }}
    
    /* Error and Success States */
    .error-field {{
        border: 2px solid #dc3545 !important;
        background-color: #fff5f5 !important;
        animation: shake 0.5s ease-in-out;
    }}
    
    @keyframes shake {{
        0%, 100% {{ transform: translateX(0); }}
        25% {{ transform: translateX(-5px); }}
        75% {{ transform: translateX(5px); }}
    }}
    
    .success-message {{
        background: linear-gradient(135deg, #d4edda, #c3e6cb);
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        animation: slideIn 0.5s ease;
    }}
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize professional session state"""
    defaults = {
        'cases': load_cases(),
        'current_case_id': None,
        'user_role': 'Partner',
        'user_name': 'Legal Professional',
        'view_mode': 'professional',
        'jurisdiction': 'USA',
        'legal_system': 'Common Law',
        'research_depth': 'Comprehensive',
        'dark_mode': False,
        'ai_model': 'gpt-4-legal',
        'authenticated': True,  # For demo, set to True
        'field_errors': {},
        'active_tab': 'Dashboard',
        'show_case_detail': False,
        'force_refresh': False
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    
    # Force refresh cases from database if needed
    if st.session_state.get('force_refresh', False):
        st.session_state.cases = load_cases()
        st.session_state.force_refresh = False

def show_professional_dashboard():
    """Professional dashboard with advanced analytics"""
    st.markdown("<div class='main-header'>🌍 LegalAI Enterprise Dashboard</div>", unsafe_allow_html=True)
    
    # Welcome message with user info
    col1, col2 = st.columns([3, 1])
    with col1:
        st.info(f"👋 Welcome back, **{st.session_state.user_name}**! Ready to manage your legal portfolio.")
    with col2:
        st.metric("Last Login", datetime.now().strftime("%H:%M"))
    
    cases = st.session_state.cases
    if not cases:
        show_empty_state()
        return
    
    # 🎯 Professional Metrics Grid
    st.markdown("### 📊 Key Performance Indicators")
    show_metrics_grid(cases)
    
    # 📈 Advanced Analytics
    st.markdown("### 📈 Portfolio Analytics")
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Case Overview", "🌐 Jurisdictional Mix", "⚖️ Practice Areas", "📅 Timeline"])
    
    with tab1:
        show_case_overview_analytics(cases)
    
    with tab2:
        show_jurisdictional_analytics(cases)
    
    with tab3:
        show_practice_area_analytics(cases)
    
    with tab4:
        show_timeline_analytics(cases)
    
    # 🚨 Urgent Actions
    show_urgent_actions(cases)
    
    # 📱 Recent Activity
    show_recent_activity(cases)

def show_metrics_grid(cases):
    """Professional metrics grid with animations"""
    stats = get_case_statistics()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        with st.container():
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Cases", stats['total_cases'], 
                     delta=f"+{len([c for c in cases if calculate_days_since(c['intake_date']) < 7])} this week")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        with st.container():
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            active_cases = len([c for c in cases if c['status'] in ['Active', 'Accepted']])
            st.metric("Active Cases", active_cases, "In Progress")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        with st.container():
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            total_value = stats['total_value']
            st.metric("Portfolio Value", f"${total_value/1000000:.1f}M", "Managed")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        with st.container():
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            high_risk = len([c for c in cases if c.get('complexity_score', 0) > 75])
            st.metric("High Risk", high_risk, delta_color="inverse")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col5:
        with st.container():
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            closed_cases = [c for c in cases if c['status'] == 'Closed']
            if closed_cases:
                favorable = len([c for c in closed_cases if c.get('outcome') == 'Favorable'])
                success_rate = (favorable / len(closed_cases)) * 100
            else:
                success_rate = 0
            st.metric("Success Rate", f"{success_rate:.1f}%", "Tracked")
            st.markdown('</div>', unsafe_allow_html=True)

def show_case_overview_analytics(cases):
    """Interactive case overview analytics"""
    col1, col2 = st.columns(2)
    
    with col1:
        # Status distribution with Plotly
        status_counts = {}
        for case in cases:
            status = case['status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        if status_counts:
            fig = px.pie(
                values=list(status_counts.values()),
                names=list(status_counts.keys()),
                title="Case Status Distribution",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(showlegend=False, height=300)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No case data available for analysis")
    
    with col2:
        # Complexity distribution
        complexity_scores = [c.get('complexity_score', 50) for c in cases]
        if complexity_scores:
            fig = px.histogram(
                x=complexity_scores,
                title="Case Complexity Distribution",
                nbins=10,
                color_discrete_sequence=[UI_CONFIG['colors']['primary']]
            )
            fig.update_layout(showlegend=False, height=300)
            fig.update_xaxes(title="Complexity Score")
            fig.update_yaxes(title="Number of Cases")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No complexity data available")

def show_jurisdictional_analytics(cases):
    """Jurisdictional analytics with maps"""
    jurisdictions = [case.get('jurisdiction', 'USA') for case in cases]
    jurisdiction_counts = pd.Series(jurisdictions).value_counts()
    
    col1, col2 = st.columns(2)
    
    with col1:
        if not jurisdiction_counts.empty:
            fig = px.bar(
                x=jurisdiction_counts.index,
                y=jurisdiction_counts.values,
                title="Cases by Jurisdiction",
                color=jurisdiction_counts.values,
                color_continuous_scale='Viridis'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No jurisdictional data available")
    
    with col2:
        # Success rates by jurisdiction
        st.write("**Success Rates by Jurisdiction**")
        jurisdictions_to_show = jurisdiction_counts.index[:5] if not jurisdiction_counts.empty else []
        
        for jurisdiction in jurisdictions_to_show:
            j_cases = [c for c in cases if c.get('jurisdiction') == jurisdiction and c['status'] == 'Closed']
            if j_cases:
                favorable = len([c for c in j_cases if c.get('outcome') == 'Favorable'])
                success_rate = (favorable / len(j_cases)) * 100
                
                st.progress(success_rate/100, text=f"📍 {jurisdiction}: {success_rate:.1f}%")
            else:
                st.write(f"📍 {jurisdiction}: No closed cases")

def show_practice_area_analytics(cases):
    """Practice area performance analytics"""
    practice_data = []
    for case in cases:
        practice_data.append({
            'Practice Area': case.get('practice_area', 'Other'),
            'Value': case.get('matter_value', 0),
            'Complexity': case.get('complexity_score', 50)
        })
    
    if practice_data:
        df = pd.DataFrame(practice_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Value by practice area
            value_by_practice = df.groupby('Practice Area')['Value'].sum().sort_values(ascending=False)
            fig = px.treemap(
                names=value_by_practice.index,
                parents=[''] * len(value_by_practice),
                values=value_by_practice.values,
                title="Portfolio Value by Practice Area"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Complexity heatmap
            complexity_by_practice = df.groupby('Practice Area')['Complexity'].mean().sort_values(ascending=False)
            fig = px.bar(
                x=complexity_by_practice.index,
                y=complexity_by_practice.values,
                title="Average Complexity by Practice Area",
                color=complexity_by_practice.values,
                color_continuous_scale='Reds'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No practice area data available")

def show_timeline_analytics(cases):
    """Timeline and trend analytics"""
    # Convert intake dates to datetime
    intake_dates = []
    for case in cases:
        try:
            date_obj = datetime.fromisoformat(case['intake_date']).date()
            intake_dates.append(date_obj)
        except:
            continue
    
    if intake_dates:
        date_counts = pd.Series(intake_dates).value_counts().sort_index()
        
        fig = px.line(
            x=date_counts.index,
            y=date_counts.values,
            title="Case Intake Timeline",
            labels={'x': 'Date', 'y': 'New Cases'}
        )
        fig.update_traces(line=dict(color=UI_CONFIG['colors']['primary'], width=3))
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No timeline data available")

def show_urgent_actions(cases):
    """Show urgent actions needed"""
    urgent_cases = [c for c in cases if c.get('urgency') in ['High', 'Critical'] and c['status'] != 'Closed']
    
    if urgent_cases:
        st.markdown("### 🚨 Urgent Attention Required")
        
        for case in urgent_cases[:3]:
            with st.container():
                st.markdown('<div class="urgent-case">', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([3, 2, 1])
                
                with col1:
                    st.write(f"**{case['case_id']}** - {case['client_name']}")
                    st.write(f"*{case['case_type']}* • {case.get('description', '')[:100]}...")
                
                with col2:
                    st.write(f"**Status:** {case['status']}")
                    st.write(f"**Urgency:** 🔥 {case.get('urgency', 'Medium')}")
                    st.write(f"**Complexity:** {case.get('complexity_score', 0)}/100")
                
                with col3:
                    if st.button("Review", key=f"review_{case['case_id']}", type="primary"):
                        st.session_state.current_case_id = case['case_id']
                        st.session_state.show_case_detail = True
                        st.session_state.active_tab = "Case Management"
                        rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)

def show_recent_activity(cases):
    """Show recent activity feed with robust error handling"""
    st.markdown("### 📋 Recent Activity")
    
    if not cases:
        st.info("No recent activity to display")
        return
    
    # Sort cases by last_updated, handle missing dates
    recent_cases = sorted(
        cases, 
        key=lambda x: x.get('last_updated', x.get('intake_date', datetime.now().isoformat())), 
        reverse=True
    )[:5]
    
    for case in recent_cases:
        # Safe date calculation with fallbacks
        last_updated = case.get('last_updated') or case.get('intake_date', datetime.now().isoformat())
        days_ago = calculate_days_since(last_updated)
        
        # Safe field access with fallbacks
        case_id = case.get('case_id', 'Unknown Case')
        client_name = case.get('client_name', 'Unknown Client')
        practice_area = case.get('practice_area', 'General Practice')
        status = case.get('status', 'Unknown')
        complexity_score = case.get('complexity_score', 50)
        
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**{case_id}** - {client_name}")
                st.write(f"*{practice_area}* • Updated {days_ago} days ago")
            
            with col2:
                status_color = get_status_color(status)
                st.markdown(f"<span style='color:{status_color}; font-weight:bold'>{status}</span>", 
                           unsafe_allow_html=True)
            
            # Safe progress calculation
            progress_value = min(complexity_score / 100, 1.0)
            st.progress(progress_value)
            st.markdown("---")

def show_professional_client_intake():
    """Professional client intake with enhanced UX"""
    st.markdown("<div class='main-header'>👥 Professional Client Intake</div>", unsafe_allow_html=True)
    
    # Progress tracker
    progress_steps = ["Client Profile", "Case Details", "Jurisdiction", "AI Analysis"]
    current_step = 0
    
    if 'client_profile' in st.session_state:
        current_step = 1
    if 'case_details' in st.session_state:
        current_step = 2
    if 'jurisdictional_data' in st.session_state:
        current_step = 3
    
    # Progress bar
    progress = current_step / (len(progress_steps) - 1) if len(progress_steps) > 1 else 0
    st.progress(progress, text=f"Step {current_step + 1} of {len(progress_steps)}: {progress_steps[current_step]}")
    
    # Tab-based interface
    tab1, tab2, tab3, tab4 = st.tabs(["🏢 Client Profile", "⚖️ Case Details", "🌐 Jurisdiction", "🤖 AI Analysis"])
    
    with tab1:
        show_enhanced_client_profile()
    
    with tab2:
        show_enhanced_case_details()
    
    with tab3:
        show_jurisdictional_intake()
    
    with tab4:
        show_ai_analysis_step()

def show_enhanced_client_profile():
    """Enhanced client profile with better validation"""
    st.subheader("🏢 Client Information")
    
    # Initialize error tracking
    if 'field_errors' not in st.session_state:
        st.session_state.field_errors = {}
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**👤 Primary Contact**")
        first_name = st.text_input("First Name *", placeholder="John", key="first_name_pro")
        last_name = st.text_input("Last Name *", placeholder="Doe", key="last_name_pro")
        email = st.text_input("Email *", placeholder="john.doe@corporation.com", key="email_pro")
        phone = st.text_input("Phone", placeholder="+1 (555) 123-4567", key="phone_pro")
        
        # Show field-specific errors
        if st.session_state.field_errors.get('first_name'):
            st.error(st.session_state.field_errors['first_name'])
        if st.session_state.field_errors.get('last_name'):
            st.error(st.session_state.field_errors['last_name'])
        if st.session_state.field_errors.get('email'):
            st.error(st.session_state.field_errors['email'])
    
    with col2:
        st.markdown("**🏢 Company Information**")
        company_name = st.text_input("Company Name *", placeholder="Global Corporation Inc.", key="company_pro")
        industry = st.selectbox("Industry", ["Technology", "Finance", "Healthcare", "Manufacturing", "Energy", "Other"], key="industry_pro")
        revenue = st.selectbox("Annual Revenue", ["Under $1M", "$1M-$10M", "$10M-$100M", "$100M-$1B", "Over $1B"], key="revenue_pro")
        
        st.markdown("**⚖️ Legal Representation**")
        conflict_check = st.checkbox("✅ I have performed comprehensive conflict check", value=False, key="conflict_pro")
        
        if st.session_state.field_errors.get('company_name'):
            st.error(st.session_state.field_errors['company_name'])
        if st.session_state.field_errors.get('conflict_check'):
            st.error(st.session_state.field_errors['conflict_check'])
    
    # Action buttons
    col1, col2 = st.columns([3, 1])
    
    with col2:
        if st.button("💾 Save & Continue →", type="primary", key="save_client_pro", use_container_width=True):
            validate_and_save_client_profile(first_name, last_name, email, company_name, conflict_check, phone, industry, revenue)

def validate_and_save_client_profile(first_name, last_name, email, company_name, conflict_check, phone, industry, revenue):
    """Validate and save client profile with detailed error reporting"""
    st.session_state.field_errors = {}
    
    errors = []
    
    # Validate required fields
    if not first_name.strip():
        st.session_state.field_errors['first_name'] = "First name is required"
        errors.append("First Name")
    
    if not last_name.strip():
        st.session_state.field_errors['last_name'] = "Last name is required"
        errors.append("Last Name")
    
    if not email.strip():
        st.session_state.field_errors['email'] = "Email is required"
        errors.append("Email")
    elif not validate_email(email):
        st.session_state.field_errors['email'] = "Please enter a valid email address"
        errors.append("Email")
    
    if not company_name.strip():
        st.session_state.field_errors['company_name'] = "Company name is required"
        errors.append("Company Name")
    
    if not conflict_check:
        st.session_state.field_errors['conflict_check'] = "Conflict check must be completed before proceeding"
        errors.append("Conflict Check")
    
    if errors:
        # Show comprehensive error message
        error_html = """
        <div style='background: linear-gradient(135deg, #ffe6e6, #ffcccc); 
                    padding: 1rem; border-radius: 10px; border-left: 4px solid #dc3545;
                    margin: 1rem 0; animation: fadeIn 0.5s ease;'>
            <h4 style='color: #dc3545; margin: 0;'>❌ Please fix the following issues:</h4>
            <ul style='margin: 0.5rem 0 0 1rem;'>
        """
        for error in errors:
            error_html += f"<li>{error}</li>"
        error_html += "</ul></div>"
        
        st.markdown(error_html, unsafe_allow_html=True)
    else:
        # Save successful data
        st.session_state.client_profile = {
            'first_name': first_name, 'last_name': last_name, 'email': email,
            'phone': phone, 'company_name': company_name, 'industry': industry,
            'revenue': revenue, 'conflict_check': conflict_check
        }
        st.session_state.field_errors = {}
        
        # Success animation
        st.markdown("""
        <div class='success-message'>
            <h4 style='margin: 0;'>✅ Client profile saved successfully!</h4>
            <p style='margin: 0.5rem 0 0 0;'>Proceeding to case details...</p>
        </div>
        """, unsafe_allow_html=True)
        
        time.sleep(1.5)
        rerun()

def show_enhanced_case_details():
    """Enhanced case details for enterprise"""
    st.subheader("⚖️ Case Details")
    
    if 'client_profile' not in st.session_state:
        st.info("Please complete the Client Profile first")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Case Classification**")
        practice_area = st.selectbox("Primary Practice Area *", ENTERPRISE_CONFIG['practice_areas'], key="practice_area_ent")
        case_type = st.text_input("Specific Case Type *", placeholder="e.g., Mergers & Acquisition, IP Litigation", key="case_type_ent")
        matter_value = st.number_input("Estimated Matter Value ($) *", min_value=0, value=1000000, step=100000, key="matter_value_ent")
        
        st.write("**Urgency & Complexity**")
        urgency = st.selectbox("Urgency Level *", ["Standard", "High", "Critical", "Emergency"], key="urgency_ent")
        complexity = st.slider("Perceived Complexity (1-10)", 1, 10, 5, key="complexity_ent")
    
    with col2:
        st.write("**Legal Team**")
        lead_partner = st.selectbox("Lead Partner", ["John Smith", "Maria Garcia", "Robert Chen", "Sarah Johnson"], key="partner_ent")
        associate = st.selectbox("Assigned Associate", ["David Wilson", "Emily Brown", "Michael Davis"], key="associate_ent")
        paralegal = st.selectbox("Support Paralegal", ["Jennifer Miller", "Christopher Moore"], key="paralegal_ent")
        
        st.write("**Budget & Billing**")
        billing_method = st.selectbox("Billing Method", ["Hourly", "Fixed Fee", "Contingency", "Mixed"], key="billing_ent")
        budget_cap = st.number_input("Budget Cap ($)", min_value=0, value=0, key="budget_ent")
        matter_code = st.text_input("Matter Code", placeholder="GLP-2024-CORP-001", key="matter_code_ent")
    
    description = st.text_area("Detailed Case Description *", 
                             placeholder="Comprehensive description of legal matter, key issues, stakeholders, and objectives...",
                             height=150, key="description_ent")
    
    if st.button("💼 Save Case Details →", type="primary", key="save_case_ent"):
        if all([practice_area, case_type, description]):
            st.session_state.case_details = {
                'practice_area': practice_area, 'case_type': case_type, 'matter_value': matter_value,
                'urgency': urgency, 'complexity': complexity, 'lead_partner': lead_partner,
                'associate': associate, 'paralegal': paralegal, 'billing_method': billing_method,
                'budget_cap': budget_cap, 'matter_code': matter_code, 'description': description
            }
            st.success("✅ Case details saved! Proceed to Jurisdictional Analysis.")
            time.sleep(1.5)
            rerun()
        else:
            st.error("Please complete all required fields")

def show_jurisdictional_intake():
    """Jurisdictional analysis intake"""
    st.subheader("🌐 Jurisdictional Analysis")
    
    if 'case_details' not in st.session_state:
        st.info("Please complete Case Details first")
        return
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Primary Jurisdiction**")
        jurisdiction = st.selectbox("Country/Jurisdiction *", COUNTRIES, key="jurisdiction_ent")
        state_province = st.text_input("State/Province", placeholder="California, England, Ontario", key="state_ent")
        court_system = st.selectbox("Court System", ["Federal", "State", "Provincial", "International"], key="court_ent")
    
    with col2:
        st.write("**Legal System**")
        legal_system = st.selectbox("Legal System *", LEGAL_SYSTEMS, key="legal_system_ent")
        applicable_law = st.text_input("Governing Law", placeholder="New York law, English law", key="law_ent")
        international_elements = st.checkbox("International elements present", key="international_ent")
    
    with col3:
        st.write("**Previous Proceedings**")
        prior_proceedings = st.radio("Prior legal proceedings?", ["None", "Trial Court", "Appellate", "Multiple"], key="proceedings_ent")
        related_cases = st.text_area("Related Case Numbers", placeholder="Case numbers of related proceedings", key="related_ent")
    
    if st.button("🌍 Save Jurisdictional Data →", type="primary", key="save_jurisdiction_ent"):
        st.session_state.jurisdictional_data = {
            'jurisdiction': jurisdiction, 'state_province': state_province,
            'court_system': court_system, 'legal_system': legal_system,
            'applicable_law': applicable_law, 'international_elements': international_elements,
            'prior_proceedings': prior_proceedings, 'related_cases': related_cases
        }
        st.success("✅ Jurisdictional data saved! Proceed to AI Legal Analysis.")
        time.sleep(1.5)
        rerun()

def show_ai_analysis_step():
    """AI analysis step"""
    st.subheader("🤖 AI Legal Analysis")
    
    if 'jurisdictional_data' not in st.session_state:
        st.info("Please complete Jurisdictional Analysis first")
        return
    
    if st.button("🚀 Run Comprehensive AI Analysis", type="primary", key="run_ai_analysis"):
        with st.spinner("🤖 AI is analyzing your case..."):
            # Combine all data
            client_data = {**st.session_state.client_profile, 
                          **st.session_state.case_details, 
                          **st.session_state.jurisdictional_data}
            
            # Run AI analysis
            ai_analysis = simulate_ai_analysis(client_data)
            complexity_score = analyze_case_complexity(client_data)
            
            st.session_state.ai_analysis = ai_analysis
            st.session_state.complexity_score = complexity_score
            
            st.success("✅ AI Analysis Complete!")
            
            # Display results
            st.subheader("AI Analysis Results")
            st.write(ai_analysis)
            
            if st.button("✅ Create Case", type="primary", key="create_case_final"):
                create_new_case()

def create_new_case():
    """Create a new case from the intake data"""
    try:
        client_data = st.session_state.client_profile
        case_data = st.session_state.case_details
        jurisdictional_data = st.session_state.jurisdictional_data
        
        # Generate case ID
        case_id = generate_case_id()
        
        new_case = {
            "case_id": case_id,
            "client_name": f"{client_data['first_name']} {client_data['last_name']}",
            "email": client_data['email'],
            "phone": client_data.get('phone', ''),
            "company_name": client_data['company_name'],
            "practice_area": case_data['practice_area'],
            "case_type": case_data['case_type'],
            "matter_value": case_data['matter_value'],
            "urgency": case_data['urgency'],
            "complexity_score": case_data['complexity'] * 10,
            "description": case_data['description'],
            "jurisdiction": jurisdictional_data['jurisdiction'],
            "legal_system": jurisdictional_data['legal_system'],
            "status": "Intake",
            "intake_date": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "lead_partner": case_data.get('lead_partner', ''),
            "associate": case_data.get('associate', ''),
            "billing_method": case_data.get('billing_method', ''),
            "budget_cap": case_data.get('budget_cap', 0)
        }
        
        # Save case
        cases = load_cases()
        cases.append(new_case)
        save_cases(cases)
        
        # Update session state
        st.session_state.cases = cases
        st.session_state.force_refresh = True
        
        st.balloons()
        st.success(f"✅ Case {case_id} created successfully!")
        
        # Clear session state
        for key in ['client_profile', 'case_details', 'jurisdictional_data', 'ai_analysis']:
            if key in st.session_state:
                del st.session_state[key]
        
        time.sleep(2)
        rerun()
        
    except Exception as e:
        st.error(f"Error creating case: {str(e)}")

def show_enhanced_case_management():
    """Enhanced case management with professional features"""
    st.markdown("<div class='main-header'>📋 Professional Case Management</div>", unsafe_allow_html=True)
    
    # Check if we should show case detail view
    if st.session_state.get('show_case_detail', False) and st.session_state.current_case_id:
        show_case_detail_view()
        return
    
    cases = st.session_state.cases
    if not cases:
        st.info("No cases found. Start by adding a new client intake.")
        return
    
    # Quick actions
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📥 Export Cases", use_container_width=True):
            csv_data = export_cases_to_csv()
            if csv_data:
                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name="cases_export.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    with col2:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.session_state.cases = load_cases()
            st.session_state.force_refresh = True
            st.success("Data refreshed!")
            time.sleep(1)
            rerun()
    with col3:
        if st.button("📊 View Statistics", use_container_width=True):
            show_case_statistics()
    with col4:
        if st.button("➕ New Case", type="primary", use_container_width=True):
            st.session_state.active_tab = "Client Intake"
            rerun()
    
    st.markdown("---")
    
    # Display cases
    for case in cases:
        with st.container():
            st.markdown('<div class="enterprise-card">', unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
            
            with col1:
                st.write(f"**{case.get('case_id', 'Unknown')}** - {case.get('client_name', 'Unknown Client')}")
                st.write(f"*{case.get('practice_area', 'General Practice')}* • {case.get('case_type', '')}")
                st.write(f"{case.get('description', '')[:100]}...")
            
            with col2:
                status_color = get_status_color(case.get('status', 'Unknown'))
                st.markdown(f"**Status:** <span style='color:{status_color}'>{case.get('status', 'Unknown')}</span>", unsafe_allow_html=True)
                st.write(f"**Urgency:** {case.get('urgency', 'Medium')}")
                st.write(f"**Value:** {format_currency(case.get('matter_value', 0))}")
            
            with col3:
                days_since = calculate_days_since(case.get('intake_date', datetime.now().isoformat()))
                st.write(f"**Age:** {days_since}d")
            
            with col4:
                col4a, col4b = st.columns(2)
                with col4a:
                    if st.button("👁️", key=f"view_{case.get('case_id', '')}", help="View Details"):
                        st.session_state.current_case_id = case.get('case_id', '')
                        st.session_state.show_case_detail = True
                        rerun()
                with col4b:
                    if st.button("⚙️", key=f"manage_{case.get('case_id', '')}", help="Manage Case"):
                        st.session_state.current_case_id = case.get('case_id', '')
                        st.session_state.show_case_detail = True
                        rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

def show_case_detail_view():
    """Show detailed view of a specific case"""
    case_id = st.session_state.current_case_id
    cases = st.session_state.cases
    case = next((c for c in cases if c.get('case_id') == case_id), None)
    
    if not case:
        st.error("Case not found")
        st.session_state.show_case_detail = False
        st.session_state.current_case_id = None
        return
    
    # Back button
    if st.button("← Back to Case List"):
        st.session_state.show_case_detail = False
        st.session_state.current_case_id = None
        rerun()
    
    st.markdown(f"## 📋 Case Details: {case_id}")
    
    # Case overview
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👤 Client Information")
        st.write(f"**Client:** {case.get('client_name', 'N/A')}")
        st.write(f"**Company:** {case.get('company_name', 'N/A')}")
        st.write(f"**Email:** {case.get('email', 'N/A')}")
        st.write(f"**Phone:** {case.get('phone', 'N/A')}")
        
        st.subheader("⚖️ Case Information")
        st.write(f"**Practice Area:** {case.get('practice_area', 'N/A')}")
        st.write(f"**Case Type:** {case.get('case_type', 'N/A')}")
        st.write(f"**Description:** {case.get('description', 'N/A')}")
    
    with col2:
        st.subheader("📊 Case Status")
        status = case.get('status', 'Unknown')
        status_color = get_status_color(status)
        st.markdown(f"**Status:** <span style='color:{status_color}; font-size: 1.2em;'>{status}</span>", unsafe_allow_html=True)
        
        st.write(f"**Urgency:** {case.get('urgency', 'Medium')}")
        st.write(f"**Complexity Score:** {case.get('complexity_score', 0)}/100")
        st.write(f"**Matter Value:** {format_currency(case.get('matter_value', 0))}")
        st.write(f"**Jurisdiction:** {case.get('jurisdiction', 'N/A')}")
        st.write(f"**Legal System:** {case.get('legal_system', 'N/A')}")
        st.write(f"**Intake Date:** {case.get('intake_date', 'N/A')}")
    
    # Case management actions
    st.markdown("---")
    st.subheader("🛠️ Case Management")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        new_status = st.selectbox("Update Status", 
                                 ["Intake", "Review", "Accepted", "Active", "Closed", "Declined"],
                                 index=["Intake", "Review", "Accepted", "Active", "Closed", "Declined"].index(status) if status in ["Intake", "Review", "Accepted", "Active", "Closed", "Declined"] else 0)
        
        if st.button("Update Status", use_container_width=True) and new_status != status:
            if update_case_status(case_id, new_status):
                st.success(f"Status updated to {new_status}")
                st.session_state.cases = load_cases()
                st.session_state.force_refresh = True
                time.sleep(1)
                rerun()
            else:
                st.error("Failed to update status")
    
    with col2:
        st.text_area("Add Note", key=f"note_{case_id}", placeholder="Add case notes...")
        if st.button("Save Note", use_container_width=True):
            note = st.session_state.get(f"note_{case_id}", "")
            if note and add_case_note(case_id, note):
                st.success("Note added successfully")
                st.session_state[f"note_{case_id}"] = ""
                time.sleep(1)
                rerun()
    
    with col3:
        if st.button("🗑️ Delete Case", type="secondary", use_container_width=True):
            if delete_case(case_id):
                st.success("Case deleted successfully")
                st.session_state.show_case_detail = False
                st.session_state.current_case_id = None
                st.session_state.cases = load_cases()
                st.session_state.force_refresh = True
                time.sleep(1)
                rerun()
            else:
                st.error("Failed to delete case")

def show_case_statistics():
    """Display case statistics"""
    stats = get_case_statistics()
    
    st.subheader("📊 Case Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Cases", stats['total_cases'])
    with col2:
        st.metric("Active Cases", stats['active_cases'])
    with col3:
        st.metric("Total Value", format_currency(stats['total_value']))
    with col4:
        st.metric("High Risk Cases", stats['high_risk_cases'])

def show_empty_state():
    """Show empty state for dashboard"""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 3rem;'>
            <h3>🌟 Welcome to LegalAI Enterprise!</h3>
            <p>Get started by creating your first case.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Create First Case", type="primary", use_container_width=True):
            st.session_state.active_tab = "Client Intake"
            rerun()

def main():
    """Main application entry point"""
    initialize_session_state()
    
    # Authentication check
    if not st.session_state.get('authenticated', False):
        login_form()
        return
    
    # Professional Sidebar
    with st.sidebar:
        st.markdown(f"<h1 style='color: {UI_CONFIG['colors']['primary']}; text-align: center;'>⚖️ LegalAI Pro</h1>", 
                   unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #666;'>{ENTERPRISE_CONFIG['firm_name']}</p>", 
                   unsafe_allow_html=True)
        st.markdown("---")
        
        # User Profile
        st.subheader("👤 Professional Profile")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image("https://via.placeholder.com/50x50/1a237e/ffffff?text=LP", width=50)
        with col2:
            st.write(f"**{st.session_state.user_name}**")
            st.caption(f"{st.session_state.user_role}")
        
        st.markdown("---")
        
        # Navigation
        st.subheader("🧭 Navigation")
        app_mode = st.radio(
            "Select Module",
            ["🌍 Dashboard", "👥 Client Intake", "📋 Case Management", "⏱️ Time Tracking", 
             "📊 Analytics", "⚙️ Settings"],
            key="professional_navigation",
            label_visibility="collapsed"
        )
        
        # Quick Stats
        st.markdown("---")
        st.subheader("📈 Quick Stats")
        cases = st.session_state.cases
        if cases:
            active_cases = len([c for c in cases if c['status'] in ['Active', 'Accepted']])
            total_value = sum([c.get('matter_value', 0) for c in cases])
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Active", active_cases)
            with col2:
                st.metric("Value", f"${total_value/1000000:.1f}M")
        else:
            st.write("No cases yet")
        
        # System Status
        st.markdown("---")
        st.subheader("🟢 System Status")
        st.caption("All systems operational")
        st.progress(0.95, text="Storage: 95%")
    
    # Main Content Router
    if "Dashboard" in app_mode:
        show_professional_dashboard()
    elif "Client Intake" in app_mode:
        show_professional_client_intake()
    elif "Case Management" in app_mode:
        show_enhanced_case_management()
    else:
        st.info("🚧 Module under development - Check back soon!")

if __name__ == "__main__":
    main()