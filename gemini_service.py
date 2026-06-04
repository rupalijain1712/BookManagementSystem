"""
Google Gemini Service
"""

from google import genai
import os



client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
    
)

print(client)
print(os.environ["GEMINI_API_KEY"])




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

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )

    return response.text