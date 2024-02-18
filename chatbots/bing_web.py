
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
        return response['text']
    finally:
        if bot is not None:
            await bot.close()
