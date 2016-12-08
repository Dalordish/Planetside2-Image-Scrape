from bs4 import BeautifulSoup
import requests 

def getImage(item_name,image_id): #Not a pure function, don't kill me pleaseeeeeeeeeeee it's just a shitty script aieeeeeeeee
    item_name = item_name.strip()
    item_name_list = item_name.split(" ") #temp var
    if item_name_list[-1].isdigit():
        print("Last is digit, removing : " + str(item_name_list[-1]))
        item_name_list.pop(-1)
        item_name = " ".join(item_name_list)
    #print(item_name)
    wiki_url = "http://planetside.wikia.com/wiki/"
    request_clean = item_name.replace("AE","")
    request_clean = request_clean.replace("GG","")
    request_clean.replace("  "," ")
    request_clean = request_clean.strip()
    request_url = wiki_url + request_clean.replace(" ","_")
    print("Requesting : " + request_url)
    result = requests.get(request_url)
    if result.status_code == 200:
        #print("YEEE BOOOOOOOIIIIIIIIIIS")
        data = result.content
        soup = BeautifulSoup(data, 'html.parser')
        try:
            image_link = soup.find("a","mw-redirect",title = item_name,).parent.parent.find_next_sibling("tr").find("img",height = "110").get("data-src")
            print(image_link)
            image = requests.get(image_link)
            with open("images/" + str(image_id) + ".png", 'wb') as imageFile:
                imageFile.write(image.content)
            print("Success!")
            return 1
        except (TypeError,AttributeError):
            print("does not exist - DOM traversal error")
            return 0
    else:
        print(result.status_code)
        print("does not exist")
        return 0

def makeSQL(item_name,image_id): #Here! this one's a pure function

    #base command ( not the right one but anyway)
    #UPDATE items SET image_id=-84637 WHERE item_id=802875; # GatekeeperH
    base_command = "UPDATE items SET"
    command = base_command + " image_id" + "=" + "-" + str(image_id) 
    command = command + " WHERE" + " image_id=" + str(image_id)
    command = command + "; #" + str(item_name)
    return command

requestItems = {
    'Aspis Anti-Aircraft Tower' : '85839',
    'Rampart Wall' : '85830',
    'Sunderer Garage' : '86100',
    'AE Medical Applicator 1' : '84808',
    'NS-15MP' : '9348',
    'NS-15M AE' : '81565'

}

failures = {}
for item_name in requestItems.keys():
    image_id = requestItems[item_name]
    if getImage(item_name,image_id) == 1:
        print(makeSQL(item_name,image_id))
        with open("SQL_Commands.txt",'a') as text: # a mode is append
            text.write(makeSQL(item_name,image_id) + "\n")
    else:
        print("Failed on item")
        failures[item_name] = image_id
    print("_________________")
print("Failed on : ")
print(failures)

with open('failures.txt','a') as failText:
    for key in failures.keys():
        failText.write(str(key) + " : " + str(failures[key]) + "\n")
print("Please note that txt files generated aren't cleared (by design), so you might get duplicate commands if you run it on the same set")
        
    #print(
    #   soup.find("a","mw-redirect",title = item_name,).parent.parent.find_next_sibling("tr").find("img",height = "110").get("data-src")
#       )

    #example output

    #<img alt="HIVE" class="lzy lzyPlcHld " data-image-key="HIVE.png" data-image-name="HIVE.png" data-src="http://vignette2.wikia.nocookie.net/planetside2/images/7/7a/HIVE.png/revision/latest/scale-to-width-down/220?cb=20160504133441" height="110" onload="if(typeof ImgLzy==='object'){ImgLzy.load(this)}" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" width="220">
    #<noscript>
    #   <img alt="HIVE" class="" data-image-key="HIVE.png" data-image-name="HIVE.png" height="110" src="http://vignette2.wikia.nocookie.net/planetside2/images/7/7a/HIVE.png/revision/latest/scale-to-width-down/220?cb=20160504133441" width="220"/>
    #</noscript>
    #</img>

    #for link in soup.find_all('img',height = "110"):
    #   print(link.get('src'))
    #print(soup.prettify().encode('UTF-8'))