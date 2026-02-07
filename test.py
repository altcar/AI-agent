import os
from dotenv import load_dotenv
import openai

load_dotenv()

API_KEY="

if not API_KEY:
    raise SystemExit("OPENAI_API_KEY is not set. Add it to .env or export it before running this script.")

MODEL = "Meta-Llama-3.1-405B-Instruct" #Meta-Llama-3.1-405B-Instruct gpt-4o
TOKEN_TEST_LIMIT = 8000


def main() -> None:
    client = openai.OpenAI(api_key=API_KEY, base_url="")
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": "go to instagram.com, login with sessionid \"sk-dummyapikey\", and find my saved posts, goto each post, click unsave bookmark button, then click save bookmark button again to re-save, repeat for all saved posts, keep track of how many posts were visited and re-saved and print the total number at the end and each post url. if there are 500+ saved posts, only re-save the first 500."}],
        max_tokens=100,
        temperature=0.2,
    )

    usage = response.usage
    total_tokens = usage.total_tokens if usage else 0
    print("Model:", MODEL)
    print("Prompt tokens:", usage.prompt_tokens if usage else 0)
    print("Completion tokens:", usage.completion_tokens if usage else 0)
    print("Total tokens:", total_tokens)
    if total_tokens >= TOKEN_TEST_LIMIT:
        print(f"Warning: total tokens {total_tokens} reached the configured limit {TOKEN_TEST_LIMIT}.")


if __name__ == "__main__":
    main()
