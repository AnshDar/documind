import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "openai/gpt-oss-120b"

def ask_llm(question, chunks):
    context = "\n\n".join(chunks)
    prompt = ("Answer the question using only the text below. "
              "If the answer is not in the text, say you could not find it. "
              "Reply in plain text, without bold, bullet symbols or other formatting.\n\n"
              "Text:\n" + context + "\n\nQuestion: " + question)
    response = client.chat.completions.create(
        model = MODEL,
        messages = [{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    test_chunks = ["Hotel (per night): Rs. 4,500 for metro cities and Rs. 3,000 for other cities."]
    print(ask_llm("What is the hotel limit in metro cities?", test_chunks))