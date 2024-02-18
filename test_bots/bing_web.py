import asyncio
import json
from pathlib import Path
from re_edge_gpt import Chatbot, ConversationStyle

async def ask_bing_web(question: str, cookies: list[dict]) -> dict:
    bot = None
    try:
        bot = await Chatbot.create(cookies=cookies)
        response = await bot.ask(
            prompt=question,
            conversation_style=ConversationStyle.balanced,
            simplify_response=True
        )
        return response
    finally:
        if bot is not None:
            await bot.close()

# Example usage:
async def main():
    try:
        cookies = json.loads(open(
            str(Path(str(Path.cwd()) + "/bing_cookies.json")), encoding="utf-8").read())
        question = "How do I know when my pizza is done?"
        response = await ask_bing_web(question, cookies)
        print(json.dumps(response, indent=2, ensure_ascii=False))
    except Exception as error:
        print("Error:", error)

if __name__ == "__main__":
    asyncio.run(main())
