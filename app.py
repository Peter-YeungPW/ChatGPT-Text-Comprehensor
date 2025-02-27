from flask import Flask, render_template, request, jsonify
from openai import OpenAI, AzureOpenAI
from openai import AuthenticationError, NotFoundError
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Set up OpenAI API credentials, DOTENV is used
# Include your api key inside a .env file with API_KEY=YOURAPIKEY 
if (api_key := os.getenv('API_KEY')) is None:
    raise KeyError('No API key provided!')

# Optionally accept Azure OpenAI API
if (azure_endpoint := os.getenv('AZURE_ENDPOINT')) is not None:
    if (api_version := os.getenv('API_VERSION')) is None:
        raise KeyError('Specify API Version when using Azure OpenAI API!')
    
    client = AzureOpenAI(
        api_key=api_key,
        api_version=api_version,
        azure_endpoint=azure_endpoint
        )

else:
    client = OpenAI(api_key=api_key)
    

# Define the default route to return the index.html file
@app.route("/")
def index():
    return render_template("index.html")

# Define the /api route to handle POST requests
@app.route("/api", methods=["POST"])
def api():
    # Get the message, chat history and function index from the POST request
    message = request.json.get("message")
    chat_history = request.json.get("chat_history",[])
    function_index = request.json.get("function_index", 0)

    # Append the new user message to the chat history
    chat_history.append({"role": "user", "content": message})
    
    # Define system roles and models based on the function index
    system_roles = [
        {"role": "system", "content": "Ignore previous instructions and history. You are a helpful assistant that performs keyword extraction. Identify and extract the most important keywords or phrases from the text provided by the user."},
        {"role": "system", "content": "Ignore previous instructions and history. You are a helpful assistant that performs text summarization. Generate a concise summary of a longer text provided by the user."},
        {"role": "system", "content": "Ignore previous instructions and history. You are a helpful assistant that performs topic classification. Categorize the text provided by the user into predefined topics (including, but not limited to sports, politics, technology, entertainment etc.)"}
    ]

    models = [
        "gpt-3.5-turbo",  # Model for keyword extraction
        "gpt-3.5-turbo",  # Model for text summarization
        "gpt-3.5-turbo"   # Model for topic classification
    ]

    # Add the system role to the chat history based on the selected function
    chat_history.append(system_roles[function_index])

    # Send the entire chat history to OpenAI's API and receive the response
    try:
        completion = client.chat.completions.create(
            messages=chat_history,
            model=models[function_index] # Use the corresponding model for each function
        )
    except AuthenticationError:
        return jsonify({"response": "Authentication Error! Make sure your API key is correct."}), 401
    except NotFoundError as e:
        return jsonify({"response": "Internal Server Error! Report this message to the administrator."}, str(e)), 500

    if completion.choices and completion.choices[0].message:
        bot_response = completion.choices[0].message.content
        # Append the bot response to the chat history
        chat_history.append({"role": "assistant", "content": bot_response})

        return jsonify({"response": bot_response, "chat_history": chat_history})  # Return both response and updated history
    else:
        return jsonify({"response": 'Failed to Generate response!'})

if __name__=='__main__':
    app.run()
