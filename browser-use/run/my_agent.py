"""
Default browser-use example using ChatBrowserUse

The simplest way to use browser-use - capable of any web task
with minimal configuration.
"""

import asyncio

from dotenv import load_dotenv

from browser_use import (
    Agent,
    Browser,
    ChatBrowserUse,
    ChatGoogle,
    ChatOpenAI,
    ChatOllama,
)
import os

# Read GOOGLE_API_KEY into env
load_dotenv()

# ChatGoogle(model='gemini-3-flash-preview')
#     llm = ChatBrowserUse()
# llm = ChatOllama(model="qwen3:0.6b")


async def main():
    browser = Browser(use_cloud=False)

    llm = ChatOpenAI(
        model="qwen-plus",
        api_key="sk-dummyapikey",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    task = """go to instagram.com, login with sessionid "sk-dummyapikey", and find my saved posts, goto each post, click unsave bookmark button, then click save bookmark button again to re-save, repeat for all saved posts, keep track of how many posts were visited and re-saved and print the total number at the end and each post url visited"""
    agent = Agent(
        browser=browser,
        task=task,
        llm=llm,
    )
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())
