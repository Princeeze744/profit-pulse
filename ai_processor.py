import re
import json
from datetime import datetime, timedelta
from typing import Dict, List

class LegalAIAnalyzer:
    def __init__(self):
        self.practice_keywords = {
            'contract': ['contract', 'agreement', 'breach', 'terms', 'obligation', 'enforce'],
            'employment': ['employee', 'employer', 'discrimination', 'harassment', 'wage', 'termination'],
            'intellectual_property': ['trademark', 'copyright', 'patent', 'intellectual property', 'ip'],
            'litigation': ['lawsuit', 'sue', 'court', 'dispute', 'claim', 'settlement'],
            'real_estate': ['property', 'lease', 'landlord', 'tenant', 'mortgage', 'zoning'],
            'business_formation': ['llc', 'corporation', 'incorporate', 'business formation', 'startup'],
            'compliance': ['compliance', 'regulation', 'legal requirement', 'audit', 'government']
        }
        
        self.attorney_specialties = {
            'contract': 'Attorney Johnson (Commercial Law)',
            'employment': 'Attorney Smith (Labor & Employment)',
            'intellectual_property': 'Attorney Davis (IP Law)',
            'litigation': 'Attorney Brown (Civil Litigation)',
            'real_estate': 'Attorney Wilson (Property Law)',
            'business_formation': 'Attorney Taylor (Business Law)',
            'compliance': 'Attorney Martinez (Regulatory Law)'
        }

    def analyze_matter(self, description: str, matter_type: str, urgency: str) -> Dict:
        """Comprehensive AI analysis of legal matter"""
        
        description_lower = description.lower()
        
        return {
            'classification': self._classify_matter(description_lower, matter_type),
            'priority': self._determine_priority(urgency, description_lower),
            'complexity': self._assess_complexity(description),
            'practice_area': self._recommend_practice_area(description_lower),
            'recommended_attorney': self._recommend_attorney(description_lower),
            'key_issues': self._extract_legal_issues(description_lower),
            'estimated_duration': self._estimate_duration(description_lower, urgency),
            'similar_cases': self._find_similar_cases_count(description_lower),
            'next_steps': self._generate_next_steps(description_lower, urgency),
            'risk_factors': self._identify_risk_factors(description_lower),
            'confidence': self._calculate_confidence(description),
            'analysis_timestamp': datetime.now().isoformat()
        }

    def _classify_matter(self, description: str, matter_type: str) -> str:
        """Classify the legal matter with high accuracy"""
        if matter_type and matter_type != "Other":
            return matter_type
        
        scores = {}
        for practice, keywords in self.practice_keywords.items():
            score = sum(1 for keyword in keywords if keyword in description)
            if score > 0:
                scores[practice] = score
        
        if scores:
            best_match = max(scores.items(), key=lambda x: x[1])
            return best_match[0].replace('_', ' ').title()
        
        return "General Legal Matter"

    def _determine_priority(self, urgency: str, description: str) -> str:
        """Determine priority with contextual analysis"""
        urgency_map = {
            "Not Urgent": "Low",
            "Somewhat Urgent": "Medium", 
            "Urgent": "High",
            "Very Urgent": "Critical",
            "Emergency": "Critical"
        }
        
        base_priority = urgency_map.get(urgency, "Medium")
        
        # Contextual priority elevation
        urgent_indicators = [
            'deadline', 'court date', 'filing deadline', 'expire', 'immediately',
            'emergency', 'urgent', 'asap', 'time-sensitive', 'lawsuit filed'
        ]
        
        urgent_count = sum(1 for indicator in urgent_indicators if indicator in description)
        
        if urgent_count >= 2 and base_priority in ["Low", "Medium"]:
            return "High"
        elif urgent_count >= 3:
            return "Critical"
        
        return base_priority

    def _assess_complexity(self, description: str) -> str:
        """Assess matter complexity based on multiple factors"""
        word_count = len(description.split())
        sentence_count = len(re.split(r'[.!?]+', description))
        
        # Complexity factors
        factors = {
            'legal_terms': len(re.findall(r'\b(wherein|hereinafter|pursuant|whereas)\b', description, re.IGNORECASE)),
            'parties': len(re.findall(r'\b(party|parties|defendant|plaintiff)\b', description, re.IGNORECASE)),
            'monetary': bool(re.search(r'\$[\d,]+|\d+ dollars?', description)),
            'multiple_issues': len(self._extract_legal_issues(description)) > 1
        }
        
        complexity_score = (
            min(word_count / 100, 1) +
            min(sentence_count / 5, 1) +
            sum(factors.values())
        )
        
        if complexity_score > 3:
            return "High"
        elif complexity_score > 1.5:
            return "Medium"
        else:
            return "Low"

    def _extract_legal_issues(self, description: str) -> List[str]:
        """Extract specific legal issues from description"""
        issues = []
        issue_patterns = {
            'Contract Breach': r'breach|violat|fail to perform|non.?performance',
            'Payment Dispute': r'payment|money owed|unpaid|fee dispute',
            'Intellectual Property': r'infringement|unauthorized use|copy right|trade secret',
            'Employment Issue': r'discriminat|harassment|wrongful termination|wage claim',
            'Regulatory Compliance': r'compliance|regulation|violation|penalty|fine',
            'Liability': r'liable|liability|negligence|damages',
            'Contract Interpretation': r'interpret|meaning|ambiguous|unclear terms'
        }
        
        for issue, pattern in issue_patterns.items():
            if re.search(pattern, description, re.IGNORECASE):
                issues.append(issue)
        
        return issues if issues else ["General Legal Consultation"]

    def _recommend_practice_area(self, description: str) -> str:
        """Recommend specific practice area"""
        classification = self._classify_matter(description, "")
        area_map = {
            "contract": "Commercial Law",
            "employment": "Labor & Employment",
            "intellectual property": "Intellectual Property Law",
            "litigation": "Civil Litigation",
            "real estate": "Real Estate Law",
            "business formation": "Business Law",
            "compliance": "Regulatory Compliance"
        }
        return area_map.get(classification.lower(), "General Practice")

    def _recommend_attorney(self, description: str) -> str:
        """Recommend the most appropriate attorney"""
        classification = self._classify_matter(description, "").lower()
        return self.attorney_specialties.get(classification, "Senior Counsel (General Practice)")

    def _estimate_duration(self, description: str, urgency: str) -> str:
        """Estimate matter duration"""
        complexity = self._assess_complexity(description)
        
        duration_map = {
            ("Low", "Low"): "1-2 weeks",
            ("Low", "Medium"): "2-4 weeks", 
            ("Low", "High"): "3-6 weeks",
            ("Medium", "Low"): "3-6 weeks",
            ("Medium", "Medium"): "1-3 months",
            ("Medium", "High"): "2-4 months",
            ("High", "Low"): "2-4 months",
            ("High", "Medium"): "3-6 months",
            ("High", "High"): "4-8 months"
        }
        
        urgency_level = "High" if urgency in ["Urgent", "Very Urgent", "Emergency"] else "Medium" if urgency == "Somewhat Urgent" else "Low"
        
        return duration_map.get((complexity, urgency_level), "2-4 weeks")

    def _find_similar_cases_count(self, description: str) -> int:
        """Simulate finding similar historical cases"""
        keywords = re.findall(r'\b[a-z]{4,}\b', description.lower())
        unique_keywords = set(keywords)
        return min(len(unique_keywords) * 2, 25)  # Simulated count

    def _generate_next_steps(self, description: str, urgency: str) -> List[str]:
        """Generate intelligent next steps"""
        steps = [
            "Initial conflict check and case opening",
            "Client engagement agreement preparation",
            "First attorney review and strategy session"
        ]
        
        if urgency in ["Urgent", "Very Urgent", "Emergency"]:
            steps.insert(0, "Immediate senior attorney review")
            steps.append("Expedited document collection")
        
        if "contract" in description.lower():
            steps.append("Contract analysis and gap identification")
            steps.append("Remedy assessment and strategy development")
        
        if "dispute" in description.lower() or "conflict" in description.lower():
            steps.append("Dispute resolution strategy session")
            steps.append("Settlement opportunity assessment")
        
        return steps

    def _identify_risk_factors(self, description: str) -> List[str]:
        """Identify potential risk factors"""
        risks = []
        
        if re.search(r'\$[0-9,]{5,}|[0-9]{6,} dollars?', description):
            risks.append("High financial exposure")
        
        if re.search(r'\b(court|judge|lawsuit|litigation)\b', description, re.IGNORECASE):
            risks.append("Active litigation involvement")
        
        if len(self._extract_legal_issues(description)) > 2:
            risks.append("Multiple complex legal issues")
        
        return risks if risks else ["Standard risk profile"]

    def _calculate_confidence(self, description: str) -> int:
        """Calculate AI confidence score"""
        word_count = len(description.split())
        legal_term_count = len(re.findall(r'\b(contract|agreement|liable|breach|dispute|claim)\b', description, re.IGNORECASE))
        
        base_confidence = min(80 + (word_count // 10) + (legal_term_count * 5), 95)
        return base_confidence

# Global instance
analyzer = LegalAIAnalyzer()

def analyze_matter(description: str, matter_type: str, urgency: str) -> Dict:
    """Main analysis function"""
    return analyzer.analyze_matter(description, matter_type, urgency)