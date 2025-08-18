from get_data import (
  fetch_questions
)

import asyncio


async def main():
    q = await fetch_questions()
    print(q)

asyncio.run(main())