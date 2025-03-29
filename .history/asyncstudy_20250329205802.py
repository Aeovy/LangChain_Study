import asyncio
import time
async def jishu():
    for i in range(10):
        if i % 2 == 1:
            print("jishu")
            return i
            time.sleep(1)
async def oushu():
    for i in range(10):
        if i % 2 == 0:
            print("oushu")
            return i
            time.sleep(1)

async def main():
    task1 = asyncio.create_task(jishu())
    task2 = asyncio.create_task(oushu())
    await task1
    await task2
    print("All tasks completed")

if __name__ == "__main__":
    asyncio.run(main())
    