import asyncio
from gemini import GeminiClient


async def ask_gemini_web(question, cookies):
    # Extract required cookies
    Secure_1PSID, Secure_1PSIDTS = extract_required_cookies(cookies)

    # Initialize Gemini client
    client = GeminiClient(Secure_1PSID, Secure_1PSIDTS, proxy=None)
    await client.init(timeout=30)

    # Generate content based on the question
    response = await client.generate_content(question)

    return response.text


def extract_required_cookies(cookies):
    # Extract necessary cookies from the provided list
    Secure_1PSID = None
    Secure_1PSIDTS = None
    for cookie in cookies:
        if cookie['name'] == '__Secure-1PSID':
            Secure_1PSID = cookie['value']
        elif cookie['name'] == '__Secure-1PSIDTS':
            Secure_1PSIDTS = cookie['value']

    return Secure_1PSID, Secure_1PSIDTS
