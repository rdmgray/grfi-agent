"""
GRFI Agent Backend - Sustainability and Impact Data Gathering Agent
Uses Google's Agent Development Kit (ADK) and Gemini model
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-pro')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'GRFI Agent Backend'
    })


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Chat endpoint for interacting with the AI agent
    Expects JSON: { "message": "user message" }
    Returns: { "response": "agent response" }
    """
    try:
        data = request.json
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({'error': 'Message is required'}), 400

        if not GEMINI_API_KEY:
            return jsonify({
                'response': 'Hello! I\'m the GRFI Sustainability Data Agent. (Note: Gemini API key not configured - running in demo mode)'
            })

        # Create a prompt with context about the agent's purpose
        system_context = """You are a specialized AI agent designed to help gather and analyze
sustainability and impact data on investment products. Your focus is on environmental,
social, and governance (ESG) factors, impact investing metrics, and sustainable finance data.

You can help users understand sustainability data sources and investment product information.
"""

        full_prompt = f"{system_context}\n\nUser: {user_message}\n\nAssistant:"

        # Generate response using Gemini
        response = model.generate_content(full_prompt)

        return jsonify({
            'response': response.text
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'response': 'Sorry, I encountered an error processing your request.'
        }), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
