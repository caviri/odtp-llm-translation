import argparse
import os
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider


def translate_file(input_file, output_file, model_name, language, endpoint, api_key):
    system_prompt = f"""
    Please translate this into the following language {language}
    """

    with open(input_file, 'r') as file:
        data = file.read()

    openaimodel_model = OpenAIModel(
        model_name=model_name, 
        provider=OpenAIProvider(base_url=endpoint, api_key=api_key)
    )

    agent = Agent(openaimodel_model, system_prompt=system_prompt)

    result = agent.run_sync(data, system_prompt=system_prompt)

    with open(output_file, 'w') as file:
        file.write(result.output)


def main():
    parser = argparse.ArgumentParser(description="Translate a file using OpenAI models.")
    parser.add_argument('--input', required=True, help="Path to the input file.")
    parser.add_argument('--output', required=True, help="Path to the output file.")
    parser.add_argument('--model', required=True, help="Model name to use for translation.")
    parser.add_argument('--language', required=True, help="Target language for translation.")
    parser.add_argument('--endpoint', required=True, help="OpenAI API endpoint.")
    parser.add_argument('--api_key', required=True, help="API key for authentication.")

    args = parser.parse_args()

    translate_file(
        input_file=args.input,
        output_file=args.output,
        model_name=args.model,
        language=args.language,
        endpoint=args.endpoint,
        api_key=args.api_key
    )


if __name__ == "__main__":
    main()