import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from llm_service import llm_service
from recommendation import RecommendationEngine

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_BASE_PATH = os.path.join(BASE_DIR, 'knowledge_base.json')

with open(KNOWLEDGE_BASE_PATH, 'r') as f:
    KNOWLEDGE_BASE = json.load(f)

recommendation_engine = RecommendationEngine(KNOWLEDGE_BASE)

SYSTEM_PROMPT = """You are StudyAbroad AI Counselor, a helpful assistant that helps students who want to study abroad. 
Your role is to provide accurate information about universities, admission requirements, visa processes, and scholarships.

When answering questions:
1. Use the provided knowledge base information whenever possible
2. Be specific and cite university names, requirements, deadlines, and fees
3. If you don't have verified information for something, clearly state that
4. Be encouraging and supportive to students
5. Keep responses concise but informative

Remember: You should only provide information that is grounded in the knowledge base provided. 
If a question is outside your knowledge base, say so honestly."""

def search_knowledge_base(query):
    query_lower = query.lower()
    results = []
    
    query_words = set(query_lower.split())
    
    for uni in KNOWLEDGE_BASE.get('universities', []):
        score = 0
        uni_text = f"{uni['university']} {uni['country']} {uni['course']} {uni['ielts']} {uni['gre']} {uni['deadline']} {uni['tuition_fee']}".lower()
        
        for word in query_words:
            if word in uni_text:
                score += 1
            if word in uni['country'].lower():
                score += 3
            if word in uni['course'].lower():
                score += 3
        
        if score > 0:
            results.append((score, uni))
    
    visa_info = KNOWLEDGE_BASE.get('visa_info', {})
    for country, info in visa_info.items():
        if country in query_lower or 'visa' in query_lower:
            results.append((2, {'type': 'visa', 'country': country, 'data': info}))
    
    scholarships = KNOWLEDGE_BASE.get('scholarships', [])
    for schol in scholarships:
        if 'scholarship' in query_lower or schol['name'].lower() in query_lower:
            results.append((1, {'type': 'scholarship', 'data': schol}))
    
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:5]

def format_context(results):
    context_parts = []
    
    for score, item in results:
        if isinstance(item, dict) and 'type' in item:
            if item['type'] == 'visa':
                v = item['data']
                context_parts.append(f"VISA INFO ({item['country'].upper()}): {v['name']}\nRequirements: {', '.join(v['requirements'])}\nProcessing Time: {v['processing_time']}")
            elif item['type'] == 'scholarship':
                s = item['data']
                context_parts.append(f"SCHOLARSHIP: {s['name']} - {s['description']}\nEligibility: {s['eligibility']}\nDeadline: {s['deadline']}")
        else:
            context_parts.append(f"University: {item['university']}, Country: {item['country']}, Course: {item['course']}, IELTS: {item['ielts']}, GRE: {item['gre']}, Deadline: {item['deadline']}, Tuition: {item['tuition_fee']}, GPA: {item['gpa_requirement']}")
    
    return "\n\n".join(context_parts)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400
    
    results = search_knowledge_base(user_message)
    context = format_context(results) if results else ""
    
    if not context:
        response = llm_service.call_llm(
            SYSTEM_PROMPT,
            user_message,
            "No specific information found in the knowledge base. Please provide a general helpful response based on your training, but note that specific details may vary."
        )
    else:
        response = llm_service.call_llm(SYSTEM_PROMPT, user_message, context)
    
    return jsonify({
        'response': response,
        'context_used': bool(context)
    })

@app.route('/recommend-university', methods=['POST'])
def recommend_university():
    data = request.get_json()
    
    profile = {
        'country': data.get('country', ''),
        'budget': data.get('budget', ''),
        'ielts': data.get('ielts', ''),
        'field': data.get('field', ''),
        'gpa': data.get('gpa', '')
    }
    
    if not profile['country'] and not profile['field'] and not profile['budget']:
        return jsonify({'error': 'Please provide at least one criterion for recommendations'}), 400
    
    recommendations = recommendation_engine.recommend(profile)
    
    return jsonify({
        'recommendations': recommendations
    })

@app.route('/knowledge', methods=['GET'])
def get_knowledge():
    country = request.args.get('country', '').lower()
    course = request.args.get('course', '').lower()
    
    universities = KNOWLEDGE_BASE.get('universities', [])
    
    if country:
        universities = [u for u in universities if country in u['country'].lower()]
    if course:
        universities = [u for u in universities if course in u['course'].lower()]
    
    return jsonify({
        'universities': universities[:20]
    })

@app.route('/visa-info/<country>', methods=['GET'])
def get_visa_info(country):
    visa_info = KNOWLEDGE_BASE.get('visa_info', {})
    country_lower = country.lower()
    
    if country_lower in visa_info:
        return jsonify(visa_info[country_lower])
    else:
        return jsonify({'error': 'Visa information not found for this country'}), 404

@app.route('/universities', methods=['GET'])
def get_all_universities():
    return jsonify({
        'universities': recommendation_engine.get_all_universities()
    })

if __name__ == '__main__':
    print("=" * 60)
    print("StudyAbroad AI Counselor - Starting Server...")
    print("=" * 60)
    print("\nAPI Endpoints:")
    print("  POST /chat - Send a message to the chatbot")
    print("  POST /recommend-university - Get university recommendations")
    print("  GET /knowledge - Search universities")
    print("  GET /visa-info/<country> - Get visa information")
    print("  GET /universities - Get all universities")
    print("\nServer running on http://localhost:5002")
    print("=" * 60)
    app.run(debug=False, port=5002, use_reloader=False)
