import json
import re

class RecommendationEngine:
    def __init__(self, knowledge_base):
        self.universities = knowledge_base.get('universities', [])
        
    def parse_budget(self, budget_str):
        if not budget_str:
            return 0
        budget_str = budget_str.upper().replace(',', '').replace('$', '').replace('USD', '')
        numbers = re.findall(r'[\d]+', budget_str)
        if numbers:
            return int(numbers[0])
        return 0
    
    def parse_ielts(self, score_str):
        if not score_str:
            return 0
        numbers = re.findall(r'[\d.]+', score_str)
        if numbers:
            return float(numbers[0])
        return 0
    
    def parse_gpa(self, gpa_str):
        if not gpa_str:
            return 0
        numbers = re.findall(r'[\d.]+', gpa_str)
        if numbers:
            return float(numbers[0])
        return 0
    
    def recommend(self, profile):
        country = profile.get('country', '').strip().lower()
        budget = self.parse_budget(profile.get('budget', ''))
        ielts = self.parse_ielts(profile.get('ielts', ''))
        field = profile.get('field', '').strip().lower()
        gpa = self.parse_gpa(profile.get('gpa', ''))
        
        recommendations = []
        
        for uni in self.universities:
            score = 0
            reasons = []
            
            if country and uni['country'].lower() == country:
                score += 30
                reasons.append(f"Matches your preferred country: {uni['country']}")
            
            if field and field in uni['course'].lower():
                score += 25
                reasons.append(f"Offers {field} program")
            
            uni_ielts = self.parse_ielts(uni.get('ielts', ''))
            if ielts >= uni_ielts:
                score += 20
                reasons.append(f"Your IELTS {ielts} meets requirement of {uni['ielts']}")
            elif ielts > 0:
                score -= 10
            
            uni_gpa = self.parse_gpa(uni.get('gpa_requirement', ''))
            if gpa >= uni_gpa:
                score += 15
                reasons.append(f"Your GPA {gpa} meets requirement of {uni_gpa}")
            elif gpa > 0:
                score -= 10
            
            tuition_str = uni.get('tuition_fee', '')
            tuition = self.parse_budget(tuition_str)
            if budget and tuition:
                if budget >= tuition:
                    score += 20
                    reasons.append(f"Fits within your budget of {budget}")
            
            if score > 0:
                recommendations.append({
                    'university': uni['university'],
                    'country': uni['country'],
                    'course': uni['course'],
                    'ielts': uni['ielts'],
                    'gre': uni['gre'],
                    'deadline': uni['deadline'],
                    'tuition_fee': uni['tuition_fee'],
                    'gpa_requirement': uni['gpa_requirement'],
                    'score': score,
                    'reasons': reasons[:3]
                })
        
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:10]
    
    def get_all_universities(self):
        return [{
            'university': u['university'],
            'country': u['country'],
            'course': u['course'],
            'ielts': u['ielts'],
            'gre': u['gre'],
            'deadline': u['deadline'],
            'tuition_fee': u['tuition_fee'],
            'gpa_requirement': u['gpa_requirement']
        } for u in self.universities]
