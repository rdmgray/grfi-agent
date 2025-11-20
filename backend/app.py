"""
GRFI Agent Backend - Sustainability and Impact Data Gathering Agent
Uses Google's Agent Development Kit (ADK) and Gemini model
"""

import os
from dotenv import load_dotenv

# Load environment variables FIRST
load_dotenv()

# Configure environment for ADK BEFORE imports
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "false"
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")

# Disable SSL verification for gRPC in development
os.environ["GRPC_DEFAULT_SSL_ROOTS_FILE_PATH"] = ""
os.environ["GRPC_ENABLE_FORK_SUPPORT"] = "0"

# Now import ADK modules
from flask import Flask, request, jsonify
from flask_cors import CORS
from google.adk.agents import LlmAgent
from google.adk.runners import InMemoryRunner
from google.genai import types
from google.adk.tools import google_search, AgentTool
from openfigi_client import OpenFigiClient
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Define system instructions for the agents
SEARCH_AGENT_INSTRUCTION = """You are a search assistant that performs web searches to gather information.
When asked to search for information, use the google_search tool to find relevant results."""

MAIN_AGENT_INSTRUCTION = """You are a specialized AI agent designed to provide information on
investment instruments. You will be asked for information on a particular security.
Give as much information as you can and include an assessment of the *impact* of buying
this security.

You should:
1. Use openfigi_search to find metadata for a particular security, including details like ticker symbols, ISINs, security type, and other identifying information.
2. Use search_web to gather additional information about the security from the web.
"""

# Initialize OpenFIGI client
openfigi_client = OpenFigiClient()


# Define tool functions for the agent
def openfigi_search(query: str) -> dict:
    """
    Search for financial instruments using OpenFIGI API.

    Use this tool to search for securities, stocks, bonds, or other financial instruments.
    The query parameter should be a search term like a company name, ticker symbol, or ISIN.

    Args:
        query: The search term to look up (e.g., company name, ticker, ISIN)

    Returns:
        Dictionary with status and fee information.
        Success: {"status": "success", "search_result": ...}
        Error: {"status": "error", "error_message": ...}

    """
    try:
        request_data = {"query": query}
        # Parse the JSON string returned by the client
        result_json = openfigi_client.search_request(request_data)
        result_data = json.loads(result_json)
        return {
            "status": "success",
            "search_result": result_data
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": str(e)
        }


def openfigi_mapping(id_type: str, id_value: str, exchange_code: str = None) -> dict:
    """
    Map financial instrument identifiers using OpenFIGI API.

    Use this tool to convert between different types of financial identifiers (e.g., ISIN to FIGI,
    ticker to FIGI, CUSIP to FIGI). This is useful for standardizing instrument identification.

    Args:
        id_type: The type of identifier (e.g., "ID_ISIN", "TICKER", "ID_CUSIP", "ID_SEDOL")
        id_value: The actual identifier value
        exchange_code: Optional exchange code to narrow down results (e.g., "US" for US markets)

    Returns:
        Dictionary with status and mapping information.
        Success: {"status": "success", "mapping_result": ...}
        Error: {"status": "error", "error_message": ...}
    """
    try:
        request_data = {"idType": id_type, "idValue": id_value}
        if exchange_code:
            request_data["exchCode"] = exchange_code

        # The mapping endpoint expects a list of requests
        # Parse the JSON string returned by the client
        result_json = openfigi_client.mapping_request([request_data])
        result_data = json.loads(result_json)
        return {
            "status": "success",
            "mapping_result": result_data
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": str(e)
        }


# Initialize LlmAgent and InMemoryRunner
agent = None
runner = None

if GOOGLE_API_KEY:
    # Create a separate search agent with google_search built-in tool
    search_agent = LlmAgent(
        name="search_agent",
        model="gemini-2.5-flash-lite",
        instruction=SEARCH_AGENT_INSTRUCTION,
        tools=[google_search],
    )

    # Wrap the search agent in an AgentTool
    search_agent_tool = AgentTool(
        agent=search_agent
    )

    # Create main agent with custom tools and the search agent tool
    agent = LlmAgent(
        name="grfi_agent",
        model="gemini-2.5-flash-lite",
        instruction=MAIN_AGENT_INSTRUCTION,
        tools=[openfigi_search, openfigi_mapping, search_agent_tool],
    )
    runner = InMemoryRunner(agent=agent, app_name="grfi_app")


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "GRFI Agent Backend"})


@app.route("/api/chat", methods=["POST"])
async def chat():
    """
    Chat endpoint for interacting with the AI agent
    Expects JSON: { "message": "user message" }
    Returns: { "response": "agent response" }
    """
    try:
        data = request.json
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        if not runner:
            return jsonify(
                {
                    "response": "Hello! I'm the GRFI Sustainability Data Agent. (Note: Google API key not configured - running in demo mode)"
                }
            )

        # Run the agent with the user message using InMemoryRunner
        try:
            # Create a session if it doesn't exist
            session_service = runner.session_service
            user_id = "default_user"
            session_id = "default_session"

            try:
                await session_service.create_session(
                    app_name=runner.app_name, user_id=user_id, session_id=session_id
                )
            except Exception:
                # Session might already exist, that's okay
                pass

            # Create Content object for the user message
            user_content = types.Content(
                role="user", parts=[types.Part(text=user_message)]
            )

            # Run the agent and collect the final response
            final_response = None
            async for event in runner.run_async(
                user_id=user_id, session_id=session_id, new_message=user_content
            ):
                if event.is_final_response() and event.content:
                    final_response = event.content.parts[0].text
                    break

            if final_response:
                return jsonify({"response": final_response})
            else:
                return jsonify({"response": "No response generated."})
        except Exception as agent_error:
            return (
                jsonify(
                    {
                        "error": str(agent_error),
                        "response": "Sorry, I encountered an error processing your request.",
                    }
                ),
                500,
            )

    except Exception as e:
        return (
            jsonify(
                {
                    "error": str(e),
                    "response": "Sorry, I encountered an error processing your request.",
                }
            ),
            500,
        )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
