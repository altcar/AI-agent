# main.py

import argparse
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from windows_use.agent import Agent

load_dotenv()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Windows-Use agent")
    parser.add_argument(
        "--model",
        default=os.getenv("OPENAI_MODEL", "qwen-plus"),
        help="Model ID (or OPENAI_MODEL)",
    )
    parser.add_argument(
        "--api_key",
        default=os.getenv("OPENAI_API_KEY", ""),
        help="OpenAI-compatible API key (or OPENAI_API_KEY)",
    )
    parser.add_argument(
        "--api_base",
        default=os.getenv("OPENAI_API_BASE", ""),
        help="OpenAI-compatible API base URL (or OPENAI_API_BASE)",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Sampling temperature",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    llm = ChatOpenAI(
        model=args.model,
        temperature=args.temperature,
        api_key=args.api_key,
        base_url=args.api_base or None,
    )
    agent = Agent(llm=llm, use_vision=False, max_steps=50)
    agent.invoke(query=input("Enter a query: "))


main()
