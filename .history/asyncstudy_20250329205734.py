import asyncio
import time
async def jishu():
    for i in range(10):
        if i % 2 == 1:
            print("jishu")
            return i
            time.sleep(1)
async def oushu