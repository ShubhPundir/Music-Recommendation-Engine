import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)

def get_lyrics_meaning(lyrics):
    try:
        model = genai.GenerativeModel("gemini-pro")
        prompt = (
            "You are a music expert. Analyze the following song lyrics and provide a contextual meaning, "
            "including emotional tone, themes, and possible interpretations:\n\n"
            f"Lyrics:\n{lyrics}\n\n"
            "Explain the meaning in simple language for a general audience."
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error analyzing lyrics: {str(e)}"

# Example usage
# lyrics = "Look at the stars, look how they shine for you..."
# print(get_lyrics_meaning(lyrics))
