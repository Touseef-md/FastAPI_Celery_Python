import google.generativeai as genai
import json
import re
import typing_extensions as typing

#Add your Gemini API_KEY
genai.configure(api_key="YOUR_GEMINI_API_KEY")


class GeminiResponse(typing.TypedDict):
    tone: str
    sentiment: str

def analyze_tone_and_sentiment(review_text, stars):
    prompt = f"""Analyze the following review:\n\nReview: \"{review_text}\"\nStars: {stars}\n\nProvide the tone and sentiment of the review. \n Use this JSON schema to answer:\n
    {{
    "tone": "",
    "sentiment": ""
    }}"""

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    # Use a regular expression to extract the JSON content
    match = re.search(r'```json\n({.*})\n```', response.text, re.DOTALL)
    if match:
        json_str = match.group(1)
        try:
            response_dict = json.loads(json_str)
            return {"tone": response_dict['tone'], "sentiment": response_dict['sentiment']}
        except json.JSONDecodeError:
            print("Error: Extracted text is not valid JSON.")
    else:
        print("Error: No JSON content found in the response.")