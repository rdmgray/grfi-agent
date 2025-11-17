"""
GRFI Agent Backend - Sustainability and Impact Data Gathering Agent
Uses Google's Agent Development Kit (ADK) and Gemini model
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Disable SSL verification for gRPC in development
os.environ['GRPC_DEFAULT_SSL_ROOTS_FILE_PATH'] = ''
os.environ['GRPC_ENABLE_FORK_SUPPORT'] = '0'

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

        # Try to generate response using Gemini
        try:
            response = model.generate_content(full_prompt)
            return jsonify({
                'response': response.text
            })
        except Exception as gemini_error:
            # If Gemini fails (e.g., SSL issues), provide a helpful demo response
            error_msg = str(gemini_error)
            if 'SSL' in error_msg or 'certificate' in error_msg.lower():
                demo_responses = {
                    'sustainability': 'Sustainability investing (also known as sustainable, socially responsible, or ESG investing) refers to investment strategies that consider environmental, social, and governance factors alongside financial returns. Key aspects include: carbon footprint analysis, renewable energy investments, social impact metrics, and corporate governance standards.',
                    'esg': 'ESG stands for Environmental, Social, and Governance - three key factors used to measure the sustainability and ethical impact of investments. Environmental criteria examine how a company performs as a steward of nature. Social criteria examine how it manages relationships with employees, suppliers, customers, and communities. Governance deals with leadership, audits, internal controls, and shareholder rights.',
                    'impact': 'Impact investing refers to investments made with the intention to generate positive, measurable social and environmental impact alongside a financial return. This differs from traditional investing by explicitly seeking to create beneficial outcomes, such as affordable housing, clean energy, or sustainable agriculture.',
                    'default': f'I apologize, but I\'m currently running in demo mode due to SSL configuration issues in this environment. In production, I would use Google\'s Gemini AI to provide detailed insights about sustainability data for your query: "{user_message}". To enable full functionality, please configure SSL certificates properly or deploy in a production environment with valid certificates.'
                }

                # Simple keyword matching for demo responses
                message_lower = user_message.lower()
                if any(word in message_lower for word in ['sustainability', 'sustainable']):
                    response_text = demo_responses['sustainability']
                elif any(word in message_lower for word in ['esg', 'governance']):
                    response_text = demo_responses['esg']
                elif any(word in message_lower for word in ['impact', 'investing']):
                    response_text = demo_responses['impact']
                else:
                    response_text = demo_responses['default']

                return jsonify({
                    'response': response_text,
                    'mode': 'demo',
                    'note': 'Running in demo mode due to SSL certificate issues. Deploy with valid SSL certificates for full AI capabilities.'
                })
            else:
                raise gemini_error

    except Exception as e:
        return jsonify({
            'error': str(e),
            'response': 'Sorry, I encountered an error processing your request.'
        }), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
