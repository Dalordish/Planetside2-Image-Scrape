#Made by Dalordish for PsArchives (M0N0)


import requests
import json

datalink = "http://psarchives.com/v1/update/items"
data = json.loads(str(requests.get(datalink).content,'utf-8'))



output = []

censusLink = "https://census.daybreakgames.com/files/ps2/images/static/" #the urls for each
psarchivesLink = "https://storage.googleapis.com/planetside/static/"
for item in data: # we're iterating over each item/weapon inside mono's global list


	try:
		censusImage = requests.get(censusLink + str(item['image_id']),stream=True) #constructing our request - stream=True defers downloading the actual image 
		psarchivesImage = requests.get(psarchivesLink + str(item['image_id']) + ".png",stream=True) #so we can speed up dramatically by not downloading gigs of images
	except ConnectionError:
		continue
	censusHas = None #If there's None in the output something's gone wrong - just declaring the variables here
	psarchivesHas = None

	if censusImage.status_code == 200: #HTTP 200 is successful request - anything else means there was an issue
		censusHas = True
	else:
		censusHas = False

	if psarchivesImage.status_code == 200: # 
		psarchivesHas = True
	else:
		psarchivesHas = False
	print(item['name']) # Logging info, nothign to see here
	print("Census: " + str(censusHas) + " psarchives : " + str(psarchivesHas))

	output.append({ #Let's remake our json with most of the same data, just the censusHas and psarchivesHas are added in too
		"name":item['name'],
		"item_id" : item['item_id'],
		"image_id" : item['image_id'],
		"censusHas": censusHas,
		"psarchivesHas": psarchivesHas,
		"faction_id" : item['faction_id']
		})

with open('neededData.json','w') as out: #writing it to a file
	out.write(json.dumps(output))