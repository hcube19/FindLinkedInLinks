
# Handles LLM prompt formatting and API calls
import os
from openai import OpenAI
from dotenv import load_dotenv
import logging


# Load the LLM prompt template from file
PROMPT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../prompts/llm_prompt.txt'))
with open(PROMPT_PATH, 'r') as f:
    PROMPT_TEMPLATE = f.read()


# Import OpenAI API key from config
import config.config as config
client = OpenAI(api_key=config.OPENAI_API_KEY)

# Format the prompt and call the LLM to verify the profile
def verify_with_llm(name, company, main_text, profile_text):
    prompt = PROMPT_TEMPLATE.format(name=name, company=company, main_text=main_text, profile_text=profile_text)
    try:
        response = client.responses.create(
            model="gpt-5",
            input=prompt,
            reasoning={"effort": "high"}
        )
        answer = ""
        for item in getattr(response, 'output', []):
            if hasattr(item, "content") and item.content:
                for content_item in item.content:
                    if hasattr(content_item, "text"):
                        answer = content_item.text.strip()
                        break
                if answer:
                    break
        return answer.upper()
    except Exception as e:
        logging.error(f"LLM API call failed: {e}")
        return ''
