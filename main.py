import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_functions import available_functions
from functions.call_function import call_function
from prompts import system_prompt


def generate_content(client, prompt, verbose):
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if response.usage_metadata is None:
        raise RuntimeError("Unable to complete request")
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    if response.candidates:
        for candidate in response.candidates:
            if candidate.content:
                prompt.append(candidate.content)
    if not response.function_calls:
        return response.text
    function_response_list = []
    for text in response.function_calls:
        function_call_response = call_function(text, verbose)
        function_call_result = function_call_response.parts[0]
        if function_call_response.parts is None:
            raise Exception("Error: function parts is none")
        if function_call_result.function_response is None:
            raise Exception("Error: function_response is none")
        if function_call_result.function_response.response is None:
            raise Exception("Error: function result is none")
        function_response_list.append(function_call_result)
        if verbose:
            print(f"-> {function_call_result.function_response.response['result']}")
    prompt.append(types.Content(role="user", parts=function_response_list))


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
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
    for _ in range(20):
        try:
            response = generate_content(client, messages, args.verbose)
            if response:
                print("Final response:")
                print(response)
                return
        except Exception as e:
            print(f"Error in generate_content: {e}")
    print("Max iterations reached")
    sys.exit(1)


if __name__ == "__main__":
    main()
