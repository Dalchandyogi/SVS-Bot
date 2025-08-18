from get_data import (
  fetch_answer
)

import asyncio


async def main():
    q = await fetch_answer("19")
    print(q)

asyncio.run(main())