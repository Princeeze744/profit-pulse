# Professional Configuration for LegalAI Enterprise
import os

# Enterprise Configuration
ENTERPRISE_CONFIG = {
    'firm_name': 'Global Law Partners LLP',
    'support_email': 'support@legalaipro.com',
    'website': 'https://legalaipro.com',
    'version': '3.0.0',
    
    'supported_jurisdictions': [
        'USA', 'United Kingdom', 'Canada', 'Australia', 'Germany', 'France', 
        'Japan', 'International', 'European Union'
    ],
    
    'practice_areas': [
        'Corporate Law', 'Litigation', 'Real Estate', 'Intellectual Property',
        'Employment Law', 'Family Law', 'Criminal Defense', 'Immigration Law',
        'Tax Law', 'Environmental Law', 'Maritime Law', 'International Arbitration',
        'Constitutional Law', 'Human Rights Law', 'Technology Law'
    ],
    
    'hourly_rates': {
        'Partner': 750,
        'Senior Associate': 450,
        'Associate': 300,
        'Paralegal': 150,
        'Consultant': 600
    },
    
    'billing_methods': [
        'Hourly', 'Fixed Fee', 'Contingency', 'Mixed', 'Retainer', 'Project-based'
    ]
}

# UI Configuration
UI_CONFIG = {
    'colors': {
        'primary': '#1a237e',
        'secondary': '#ff7f0e', 
        'success': '#28a745',
        'warning': '#ffc107',
        'error': '#dc3545',
        'info': '#17a2b8',
        'dark': '#343a40',
        'light': '#f8f9fa'
    },
    
    'status_options': [
        "Intake", "Review", "Accepted", "Active", "Closed", "Declined", "On Hold"
    ],
    
    'urgency_levels': [
        "Low", "Medium", "High", "Critical"
    ],
    
    'case_types': [
        "Corporate", "Litigation", "Real Estate", "Intellectual Property",
        "Employment", "Family", "Criminal", "Personal Injury", "Bankruptcy",
        "Immigration", "Tax", "Estate Planning", "Contract Dispute", "Other"
    ]
}

# Feature Flags
FEATURE_FLAGS = {
    'ai_analysis': True,
    'time_tracking': True,
    'billing_integration': True,
    'document_management': False,
    'email_integration': False,
    'advanced_analytics': True,
    'multi_user': True,
    'dark_mode': True,
    'mobile_optimized': True
}

# Environment Configuration
class Config:
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    SECRET_KEY = os.getenv('SECRET_KEY', 'legalai-enterprise-secret-2024')
    DATABASE_PATH = os.getenv('DATABASE_PATH', './data/')
    
    # AI Configuration
    AI_MODEL = os.getenv('AI_MODEL', 'gpt-4-legal')
    MAX_ANALYSIS_TIME = 30  # seconds
    
    # Performance
    CACHE_TIMEOUT = 300  # 5 minutes
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

# Instantiate config
config = Config()