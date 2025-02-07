from dotenv import load_dotenv
import os
import json
import openai

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with custom base URL
client = openai.OpenAI(
    api_key=os.getenv("OPENAI_CUSTOM_API_KEY"),
    base_url=os.getenv("OPENAI_CUSTOM_API_BASE")
)

# DEFAULT_MODEL = "google/gemini-2.0-flash-001"
DEFAULT_MODEL = "gpt-4-32k"

def answer(
    user_message: str | list,
    system_prompt: str = "You are a helpful assistant.",
    temperature: float = 0.7,
    model: str = DEFAULT_MODEL
) -> str:
    """
    Get a basic response from the OpenAI API.
    
    Args:
        user_message (str | list): The user's input message (text or multimodal content)
        system_prompt (str): The system prompt to guide the model's behavior
        temperature (float): Controls randomness (0.0 to 1.0)
        model (str): The model to use for generation
    
    Returns:
        str: The model's response
    """
    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
    )
    return response.choices[0].message.content

def answer_json(
    user_message: str,
    system_prompt: str = "You are a helpful assistant. Always respond with valid JSON.",
    temperature: float = 0.7,
    model: str = DEFAULT_MODEL,
    max_tokens: int = 4096
) -> dict:
    """
    Get a JSON response from the OpenAI API.
    
    Args:
        user_message (str): The user's input message
        system_prompt (str): The system prompt to guide the model's behavior
        temperature (float): Controls randomness (0.0 to 1.0)
        model (str): The model to use for generation
        max_tokens (int): Maximum number of tokens in the response
    
    Returns:
        dict: The model's response parsed as JSON
    """
    # Create a more structured prompt to ensure valid JSON
    json_prompt = (
        "You are a JSON-only response bot. Important rules:\n"
        "1. Respond ONLY with valid JSON\n"
        "2. No markdown formatting, no extra text\n"
        "3. No explanation or conversation\n"
        "4. The JSON should be properly formatted and parseable\n"
        "5. Use double quotes for keys and string values\n\n"
        f"{system_prompt}"
    )
    
    # Enhance the user message to be more explicit about JSON requirements
    formatted_user_message = (
        f"Provide a JSON response for: {user_message}\n"
        "Remember: Return ONLY valid JSON, nothing else."
    )
    
    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": json_prompt},
            {"role": "user", "content": formatted_user_message}
        ]
    )
    
    # Parse the response as JSON - now with cleanup for common formatting issues
    try:
        response_text = response.choices[0].message.content.strip()
        # Remove any markdown code block indicators
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        return json.loads(response_text.strip())
    except json.JSONDecodeError as e:
        raise ValueError(f"The API response was not valid JSON. Error: {str(e)}\nResponse: {response.choices[0].message.content}")
