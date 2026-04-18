import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_functions import available_functions
from prompts import system_prompt


def generate_content(client, prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if response.usage_metadata is None:
        raise RuntimeError("Unable to complete request")
    return response


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    if api_key is None:
        raise RuntimeError("Unable to locate api key. Verify veriable set properly.")
    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    response = generate_content(client, messages)
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    if response.function_calls is not None:
        for text in response.function_calls:
            print(f"Calling function: {text.name}({text.args})")
    else:
        print(response.text)


if __name__ == "__main__":
    main()
