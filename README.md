# GRFI Agent - Sustainability & Impact Data Intelligence

An AI agent tool for gathering and analyzing sustainability and impact data on investment products. Built with Python (Flask + Google Gemini) backend and React frontend.

## 🌱 Overview

GRFI Agent is a prototype AI agent designed to help gather data from diverse sources on investment products, with a focus on sustainability and impact metrics. It uses Google's Agent Development Kit (ADK) and Gemini model family to provide intelligent responses about ESG factors, impact investing, and sustainable finance data.

## 🏗️ Project Structure

```
grfi-agent/
├── backend/               # Python Flask backend
│   ├── app.py            # Main Flask application
│   ├── requirements.txt  # Python dependencies
│   └── .env.example      # Environment variables template
│
└── frontend/             # React frontend
    ├── public/           # Static files
    ├── src/
    │   ├── components/   # React components
    │   │   ├── Header.js
    │   │   ├── ChatInterface.js
    │   │   ├── Message.js
    │   │   └── MessageInput.js
    │   ├── App.js
    │   └── index.js
    └── package.json      # Node dependencies
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn
- Google Gemini API key (get one at: https://makersuite.google.com/app/apikey)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

5. Run the backend:
   ```bash
   python app.py
   ```
   The backend will start on `http://localhost:5000`

### Frontend Setup

1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```
   The frontend will start on `http://localhost:3000`

## 💬 Usage

1. Open your browser to `http://localhost:3000`
2. You'll see a clean, modern chat interface
3. Type a message about sustainability data, ESG metrics, or impact investing
4. The AI agent will respond with relevant information

### Example Queries

- "What are the key ESG metrics for evaluating investment products?"
- "Tell me about sustainability data sources"
- "What is impact investing?"
- "How do I measure the environmental impact of a portfolio?"

## 🎨 Features

### Current Features (v0.1)
- ✅ Clean and attractive React UI with gradient design
- ✅ Real-time chat interface
- ✅ Integration with Google Gemini Pro model
- ✅ Responsive design for mobile and desktop
- ✅ Typing indicators and smooth animations
- ✅ Error handling and loading states

### Planned Features
- 🔄 Multi-source data gathering capabilities
- 🔄 Integration with financial data APIs
- 🔄 ESG rating analysis
- 🔄 Investment product comparison
- 🔄 Data visualization dashboards
- 🔄 Advanced agentic workflows using Google ADK

## 🛠️ Technology Stack

**Backend:**
- Flask (Python web framework)
- Google Generative AI (Gemini Pro model)
- Flask-CORS (Cross-origin requests)
- python-dotenv (Environment management)

**Frontend:**
- React 18
- Axios (HTTP client)
- CSS3 with modern gradients and animations
- Responsive design

## 📝 Development Notes

This is a prototype focused on demonstrating agentic capabilities rather than production-ready investment tools. The architecture is designed to be extensible for adding multiple data sources and advanced agent behaviors.

## 🔐 API Key Security

- Never commit your `.env` file or actual API keys to version control
- The `.env.example` file is provided as a template
- Keep your Gemini API key secure and rotate it regularly

## 🤝 Contributing

This is a prototype project. Feel free to extend it with:
- Additional data source integrations
- Enhanced agentic capabilities
- More sophisticated UI components
- Data visualization features

## 📄 License

This project is for educational and prototyping purposes.

## 🐛 Troubleshooting

**Backend won't start:**
- Make sure you've activated the virtual environment
- Check that all dependencies are installed
- Verify your Python version is 3.8+

**Frontend won't connect to backend:**
- Ensure the backend is running on port 5000
- Check that CORS is enabled
- Verify the proxy setting in `package.json`

**Gemini API errors:**
- Verify your API key is correct in `.env`
- Check your API quota and limits
- Ensure you have internet connectivity

## 📧 Support

For issues and questions, please refer to the documentation or create an issue in the repository.
