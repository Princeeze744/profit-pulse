import json
import os
import uuid
import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional

def load_cases() -> List[Dict]:
    """Load cases with enhanced error handling and data validation"""
    try:
        if os.path.exists("cases.json"):
            with open("cases.json", "r", encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    cases = json.loads(content)
                    # Validate case structure
                    return [validate_case(case) for case in cases]
        return []
    except Exception as e:
        print(f"❌ Error loading cases: {e}")
        return []

def validate_case(case: Dict) -> Dict:
    """Ensure case has all required fields with defaults"""
    required_fields = {
        'case_id': lambda: generate_case_id(),
        'client_name': lambda: 'Unknown Client',
        'email': lambda: '',
        'status': lambda: 'Intake',
        'intake_date': lambda: datetime.now().isoformat(),
        'last_updated': lambda: datetime.now().isoformat()
    }
    
    for field, default_func in required_fields.items():
        if field not in case or not case[field]:
            case[field] = default_func()
    
    return case

def save_cases(cases: List[Dict]) -> bool:
    """Save cases with backup and compression"""
    try:
        # Create backup
        if os.path.exists("cases.json"):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"backups/cases_backup_{timestamp}.json"
            os.makedirs("backups", exist_ok=True)
            os.rename("cases.json", backup_name)
        
        # Save with pretty printing
        with open("cases.json", "w", encoding='utf-8') as f:
            json.dump(cases, f, indent=2, ensure_ascii=False, default=str)
        
        # Clean up old backups (keep last 5)
        cleanup_old_backups()
        return True
    except Exception as e:
        print(f"❌ Error saving cases: {e}")
        return False

def cleanup_old_backups(max_backups: int = 5):
    """Keep only the most recent backups"""
    try:
        if os.path.exists("backups"):
            backups = [f for f in os.listdir("backups") if f.startswith("cases_backup_")]
            backups.sort(reverse=True)
            
            for old_backup in backups[max_backups:]:
                os.remove(os.path.join("backups", old_backup))
    except Exception as e:
        print(f"Warning: Could not clean up backups: {e}")

def update_case_status(case_id: str, new_status: str, notes: str = None) -> bool:
    """Update case status with comprehensive tracking"""
    try:
        cases = load_cases()
        case_updated = False
        
        for case in cases:
            if case['case_id'] == case_id:
                old_status = case.get('status', 'Unknown')
                case['status'] = new_status
                case['last_updated'] = datetime.now().isoformat()
                case['status_history'] = case.get('status_history', [])
                case['status_history'].append({
                    'from_status': old_status,
                    'to_status': new_status,
                    'timestamp': datetime.now().isoformat(),
                    'notes': notes
                })
                case_updated = True
                break
        
        if case_updated:
            if save_cases(cases):
                # Add a note about the status change
                if notes:
                    add_case_note(case_id, f"Status changed from {old_status} to {new_status}: {notes}", "System")
                else:
                    add_case_note(case_id, f"Status changed from {old_status} to {new_status}", "System")
                return True
        return False
    except Exception as e:
        print(f"❌ Error updating case status: {e}")
        return False

def get_case_by_id(case_id: str) -> Optional[Dict]:
    """Get a specific case by ID with enhanced data"""
    try:
        cases = load_cases()
        for case in cases:
            if case['case_id'] == case_id:
                # Enrich case data
                case['time_entries'] = get_time_entries_for_case(case_id)
                case['total_time'] = sum(entry['hours'] for entry in case['time_entries'])
                case['total_billed'] = sum(entry['amount'] for entry in case['time_entries'])
                case['notes'] = get_case_notes(case_id)
                return case
        return None
    except Exception as e:
        print(f"❌ Error getting case by ID: {e}")
        return None

def add_time_entry(case_id: str, task_description: str, hours: float, date: str = None, rate: float = 250, user: str = "System") -> bool:
    """Add a time entry for a case with comprehensive tracking"""
    try:
        entries = load_time_entries()
        
        new_entry = {
            'id': str(uuid.uuid4()),
            'case_id': case_id,
            'date': date or datetime.now().isoformat(),
            'task_description': task_description,
            'hours': hours,
            'rate': rate,
            'amount': hours * rate,
            'user': user,
            'billed': False,
            'created_at': datetime.now().isoformat()
        }
        
        entries.append(new_entry)
        
        if save_time_entries(entries):
            # Update case total time and amount
            cases = load_cases()
            for case in cases:
                if case['case_id'] == case_id:
                    case['time_spent'] = case.get('time_spent', 0) + hours
                    case['billed_amount'] = case.get('billed_amount', 0) + (hours * rate)
                    case['last_updated'] = datetime.now().isoformat()
                    break
            
            save_cases(cases)
            return True
        return False
    except Exception as e:
        print(f"❌ Error adding time entry: {e}")
        return False

def get_time_entries_for_case(case_id: str) -> List[Dict]:
    """Get all time entries for a specific case"""
    try:
        entries = load_time_entries()
        return [entry for entry in entries if entry['case_id'] == case_id]
    except Exception as e:
        print(f"❌ Error getting time entries for case: {e}")
        return []

def get_time_entries(date_from: str = None, date_to: str = None) -> List[Dict]:
    """Get time entries with optional date filtering"""
    try:
        entries = load_time_entries()
        
        if date_from and date_to:
            filtered_entries = []
            for entry in entries:
                entry_date = datetime.fromisoformat(entry['date']).date()
                from_date = datetime.fromisoformat(date_from).date()
                to_date = datetime.fromisoformat(date_to).date()
                if from_date <= entry_date <= to_date:
                    filtered_entries.append(entry)
            return filtered_entries
        
        return entries
    except Exception as e:
        print(f"❌ Error getting time entries: {e}")
        return []

def add_case_note(case_id: str, note_content: str, author: str = "System", note_type: str = "general") -> bool:
    """Add a note to a case with comprehensive metadata"""
    try:
        notes = load_notes()
        
        new_note = {
            'id': str(uuid.uuid4()),
            'case_id': case_id,
            'timestamp': datetime.now().isoformat(),
            'author': author,
            'content': note_content,
            'type': note_type,
            'case_status_at_time': get_case_by_id(case_id).get('status', 'Unknown') if get_case_by_id(case_id) else 'Unknown'
        }
        
        notes.append(new_note)
        return save_notes(notes)
    except Exception as e:
        print(f"❌ Error adding case note: {e}")
        return False

def get_case_notes(case_id: str) -> List[Dict]:
    """Get all notes for a specific case"""
    try:
        notes = load_notes()
        case_notes = [note for note in notes if note['case_id'] == case_id]
        return sorted(case_notes, key=lambda x: x['timestamp'], reverse=True)
    except Exception as e:
        print(f"❌ Error getting case notes: {e}")
        return []

def delete_case(case_id: str) -> bool:
    """Delete a case and all associated data"""
    try:
        cases = load_cases()
        initial_count = len(cases)
        
        # Filter out the case to delete
        updated_cases = [case for case in cases if case['case_id'] != case_id]
        
        if len(updated_cases) < initial_count:
            # Case was found and removed
            if save_cases(updated_cases):
                # Also remove related time entries and notes
                cleanup_case_data(case_id)
                return True
        return False
    except Exception as e:
        print(f"❌ Error deleting case: {e}")
        return False

def cleanup_case_data(case_id: str) -> bool:
    """Clean up related data when a case is deleted"""
    try:
        # Clean up time entries
        entries = load_time_entries()
        updated_entries = [entry for entry in entries if entry['case_id'] != case_id]
        save_time_entries(updated_entries)
        
        # Clean up notes
        notes = load_notes()
        updated_notes = [note for note in notes if note['case_id'] != case_id]
        save_notes(updated_notes)
        
        return True
    except Exception as e:
        print(f"❌ Error cleaning up case data: {e}")
        return False

def export_cases_to_csv() -> str:
    """Export all cases to CSV format"""
    try:
        cases = load_cases()
        if not cases:
            return None
            
        # Convert to DataFrame
        df = pd.DataFrame(cases)
        
        # Select and order columns for better readability
        display_columns = [
            'case_id', 'client_name', 'company_name', 'email', 'practice_area',
            'case_type', 'matter_value', 'jurisdiction', 'status', 'urgency',
            'complexity_score', 'lead_partner', 'intake_date', 'last_updated'
        ]
        
        # Filter to only include columns that exist
        available_columns = [col for col in display_columns if col in df.columns]
        df = df[available_columns]
        
        # Format dates
        if 'intake_date' in df.columns:
            df['intake_date'] = pd.to_datetime(df['intake_date']).dt.strftime('%Y-%m-%d')
        if 'last_updated' in df.columns:
            df['last_updated'] = pd.to_datetime(df['last_updated']).dt.strftime('%Y-%m-%d')
        
        # Format currency
        if 'matter_value' in df.columns:
            df['matter_value'] = df['matter_value'].apply(lambda x: f"${x:,.2f}")
        
        return df.to_csv(index=False)
    except Exception as e:
        print(f"❌ Error exporting cases: {e}")
        return None

def get_case_statistics() -> Dict:
    """Get comprehensive case statistics"""
    try:
        cases = load_cases()
        
        stats = {
            'total_cases': len(cases),
            'cases_by_status': {},
            'cases_by_practice_area': {},
            'cases_by_jurisdiction': {},
            'total_value': 0,
            'active_cases': 0,
            'high_risk_cases': 0,
            'average_complexity': 0,
            'total_time_spent': 0
        }
        
        complexity_scores = []
        
        for case in cases:
            # Count by status
            status = case.get('status', 'Unknown')
            stats['cases_by_status'][status] = stats['cases_by_status'].get(status, 0) + 1
            
            # Count by practice area
            practice_area = case.get('practice_area', 'Unknown')
            stats['cases_by_practice_area'][practice_area] = stats['cases_by_practice_area'].get(practice_area, 0) + 1
            
            # Count by jurisdiction
            jurisdiction = case.get('jurisdiction', 'Unknown')
            stats['cases_by_jurisdiction'][jurisdiction] = stats['cases_by_jurisdiction'].get(jurisdiction, 0) + 1
            
            # Total value
            stats['total_value'] += case.get('matter_value', 0)
            
            # Active cases
            if case.get('status') in ['Active', 'Accepted', 'Review']:
                stats['active_cases'] += 1
            
            # High risk cases
            if case.get('complexity_score', 0) > 75:
                stats['high_risk_cases'] += 1
            
            # Complexity scores for average
            complexity_scores.append(case.get('complexity_score', 50))
            
            # Total time spent
            stats['total_time_spent'] += case.get('time_spent', 0)
        
        # Calculate averages
        if complexity_scores:
            stats['average_complexity'] = sum(complexity_scores) / len(complexity_scores)
        
        return stats
    except Exception as e:
        print(f"❌ Error getting case statistics: {e}")
        return {}

def load_time_entries() -> List[Dict]:
    """Load time entries from JSON file"""
    try:
        if os.path.exists("time_entries.json"):
            with open("time_entries.json", "r", encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    return json.loads(content)
        return []
    except Exception as e:
        print(f"❌ Error loading time entries: {e}")
        return []

def save_time_entries(entries: List[Dict]) -> bool:
    """Save time entries to JSON file"""
    try:
        with open("time_entries.json", "w", encoding='utf-8') as f:
            json.dump(entries, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"❌ Error saving time entries: {e}")
        return False

def load_notes() -> List[Dict]:
    """Load case notes from JSON file"""
    try:
        if os.path.exists("case_notes.json"):
            with open("case_notes.json", "r", encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    return json.loads(content)
        return []
    except Exception as e:
        print(f"❌ Error loading notes: {e}")
        return []

def save_notes(notes: List[Dict]) -> bool:
    """Save case notes to JSON file"""
    try:
        with open("case_notes.json", "w", encoding='utf-8') as f:
            json.dump(notes, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"❌ Error saving notes: {e}")
        return False

def search_cases_by_keyword(keyword: str, field: str = "all") -> List[Dict]:
    """Search cases by keyword in specified fields"""
    try:
        cases = load_cases()
        matching_cases = []
        
        keyword_lower = keyword.lower()
        
        for case in cases:
            if field == "all" or field == "client_name":
                if keyword_lower in case.get('client_name', '').lower():
                    matching_cases.append(case)
                    continue
            if field == "all" or field == "case_type":
                if keyword_lower in case.get('case_type', '').lower():
                    matching_cases.append(case)
                    continue
            if field == "all" or field == "description":
                if keyword_lower in case.get('description', '').lower():
                    matching_cases.append(case)
                    continue
            if field == "all" or field == "practice_area":
                if keyword_lower in case.get('practice_area', '').lower():
                    matching_cases.append(case)
                    continue
            if field == "all" or field == "company_name":
                if keyword_lower in case.get('company_name', '').lower():
                    matching_cases.append(case)
                    continue
        
        return matching_cases
    except Exception as e:
        print(f"❌ Error searching cases: {e}")
        return []

def generate_case_id() -> str:
    """Generate a unique case ID"""
    import time
    import random
    import string
    
    timestamp = int(time.time())
    random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"LAW-{timestamp}-{random_suffix}"

# Initialize data files if they don't exist
def initialize_data_files():
    """Initialize required data files if they don't exist"""
    try:
        if not os.path.exists("cases.json"):
            save_cases([])
        if not os.path.exists("time_entries.json"):
            save_time_entries([])
        if not os.path.exists("case_notes.json"):
            save_notes([])
        os.makedirs("backups", exist_ok=True)
        print("✅ Data files initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing data files: {e}")

# Initialize on import
initialize_data_files()