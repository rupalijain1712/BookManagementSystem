"""
Google Gemini Service
"""

from google import genai
from google.genai import errors #For overload error hanfling
import os



client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
    
)

# print(client)
# print(os.environ["GEMINI_API_KEY"])




def get_book_recommendation(
        user_interest):
    """
    Generate AI Recommendations
    """

    prompt = f"""
    You are an expert librarian.

    User Interest:
    {user_interest}

    Recommend 5 books.

    For each provide:

    1. Book Name
    2. Author
    3. Difficulty Level
    4. Why Recommended
    """

    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",  
            contents=prompt
        )
        return response.text

    except errors.APIError as e:
        # Catches server overloads (503), rate limits (429), or internal errors (500)
        print(f"Gemini API Error occurred: {e}")
        return (
            "⚠️ The AI Library Service is currently busy or overloaded. "
            "Please wait a few moments and click 'Get Recommendations' again!"
        )
        
    except Exception as e:
        # Catch-all fallback for other sudden issues (e.g., local network loss)
        print(f"Unexpected system error: {e}")
        return "⚠️ A system connection issue occurred. Please check your internet connection and retry."