# app/services/ai_enhancer.py
import openai

class AIEnhancer:
    def __init__(self, api_key: str):
        openai.api_key = api_key

    def enhance_resume(self, resume_text: str) -> str:
        prompt = (
            "You are a professional resume writer. Improve the following resume "
            "by fixing grammar, making the language more professional, and "
            "ensuring it's suitable for job applications:\n\n"
            f"{resume_text}\n\n"
            "Return only the enhanced resume."
        )

        try:
            response = openai.Completion.create(
                engine="text-davinci-003",  # Replace with your preferred model
                prompt=prompt,
                max_tokens=2000,
                temperature=0.7,
            )
            return response.choices[0].text.strip()
        except Exception as e:
            raise ValueError(f"Error interacting with OpenAI: {e}")
