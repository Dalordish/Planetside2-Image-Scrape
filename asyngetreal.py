#Wierd semi-asynchronous thing just to get the item images required - first time using python async
# Does two requests async (each item), but everything else sync.  POS crappy code, but a learning experience. Python async is still really weird to me, even with async/await
# Written by Dalordish for Mono
import aiohttp
import asyncio
import async_timeout

import requests #first time using aiohttp so i'm just using requests for the initial data load
import json

datalink = "http://psarchives.com/v1/update/items"
data = json.loads(str(requests.get(datalink).content,'utf-8'))

print(len(data))
async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.read()

async def fetchHead(session, url):
    with async_timeout.timeout(10):
        async with session.head(url) as response:
            return response.status

censusLink = "https://census.daybreakgames.com/files/ps2/images/static/" #the urls for each
psarchivesLink = "https://storage.googleapis.com/planetside/static/"

censusTemp = []
psarchivesTemp = []
required = []

async def main(loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        count = 0
        for item in data:
            #try:
            censusURL = censusLink + str(item['image_id']) #creating our request URLs
            psarchivesURL = psarchivesLink + str(item['image_id']) + ".png"
            censusImage = await fetchHead(session,censusURL)
            psarchivesImage = await fetchHead(session,psarchivesURL)
            if censusImage != 200 and psarchivesImage != 200:
                #required.append( [ item['name'] , item['image_id'] , item['item_id'] ])
                required.append({
                    'name': item['name'],
                    'image_id' : item['image_id'],
                    'item_id' : item['item_id'],
                    'faction_id' : item['faction_id']
                    })
                print(required)
            count = count + 1
            print(count)
            censusTemp.append(censusImage)
            psarchivesTemp.append(psarchivesImage)

#            except ClientResponseError:
#                continue
        

        #for url in censusurls:
        #    list.append(await fetchHead(session, url))
        #    print(list)

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))

print(censusTemp)
print(psarchivesTemp)


with open('neededData.json','w') as out: #writing it to a file
    out.write(json.dumps(required))