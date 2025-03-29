import asyncio
import time
async def jishu():
    for i in range(10):
        if i % 2 == 1:
            time.sleep(1)
async def oushu():
    for i in range(10):
        if i % 2 == 0:
            time.sleep(1)
            return i  
            

async def main():
    task1 = asyncio.create_task(jishu())
    task2 = asyncio.create_task(oushu())
    await task1
    await task2
    print("All tasks completed")

if __name__ == "__main__":
    starttime=time.perf_counter()
    asyncio.run(main())
    endtime=time.perf_counter()
    print(f"Time taken: {endtime - starttime} seconds")
