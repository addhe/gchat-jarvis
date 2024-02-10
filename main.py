from typing import Any, Mapping

import flask
import functions_framework
import google.generativeai as genai
import os

# Google Cloud Function that responds to messages sent in Google Chat.
#
# @param {Object} req Request sent from Google Chat.
# @param {Object} res Response to send back.

GEMINI_MODEL_ID = "gemini-pro"

@functions_framework.http
def hello_jarvis(req: flask.Request) -> Mapping[str, Any]:
  if req.method == "GET":
    return "Hello! This function must be called from Google Chat."

  request_json = req.get_json(silent=True)
  prompt = request_json["message"]["text"]

  response = generate_content(prompt)
  return {"text": response}

def generate_content(prompt):
  try:
    # Retrieve API key securely from environment variables or a secrets manager
    api_key = os.environ.get("GOOGLE_GEMINI_API_KEY")
    if not api_key:
      raise ValueError("Missing GOOGLE Gemini API Key.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(GEMINI_MODEL_ID)
    response = model.generate_content(prompt)
    return response.text
  except Exception as e:
    return f"An error occurred: {e}"
