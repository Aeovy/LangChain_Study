import asyncio
import time
async def jishu():
    result=[]
    for i in range(10):
        
        if i % 2 == 1:
            result.append(i)
            awasyncio.sleep(1)         
    return result
async def oushu():
    result=[]
    for i in range(10):
        
        if i % 2 == 0:
            result.append(i)
            await asyncio.sleep(1)        
    return result

            

async def main():
    task1 = asyncio.create_task(jishu())
    task2 = asyncio.create_task(oushu())
    result1=await task1
    result2=await task2
    print(result1,result2)

if __name__ == "__main__":
    starttime=time.perf_counter()
    asyncio.run(main())
    endtime=time.perf_counter()
    print(f"Time taken: {endtime - starttime} seconds")
