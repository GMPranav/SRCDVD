import os
import requests

if os.path.exists("missinglinks.txt"):
    os.remove("missinglinks.txt")

game_abbr = input("Enter the game's abbreviation in speedrun.com (eg. \"smb1\" for Super Mario Bros.): ")

url = "https://www.speedrun.com/" + game_abbr + "/gamestats"
response = requests.get(url)
data = response.text
Links = []
word = str()
done = bool()
counter = int()
link = str()

for i in range(len(data)):
    if data[i] == 'N':
        word = str(data[i])
        for j in range(13):
            word += str(data[i+j+1])
        if word == "Number of runs":
            done = False
            counter = 66
            link = str()
            while not done:
                link += str(data[i+counter])
                if data[i+counter+1] == '\n':
                    done = True
                counter += 1
            runs_count = int(link.replace(',',''))

url = "https://www.speedrun.com/api/v1/games/" + game_abbr
response = requests.get(url)
game_id = response.url[38:]
data = response.text
word = str()
game_name = str()
for i in range(len(data)):
     if data[i] == 'i':
        word = str(data[i])
     for j in range(12):
        word += str(data[i+j+1])
     if word == "international":
        done = False
        counter = 16
        while not done:
            game_name += str(data[i+counter])
            if data[i+counter+1] == '\"':
                done = True
            counter += 1
        break
if game_name == str():
    print("\n\nGame does not exist, please check again.")
else:
    print("\n\nGame detected: "+game_name)
    print("\nConnecting with speedrun.com API to gather run data......")      
        
if os.path.exists("data.txt"):
    os.remove("data.txt")

f = open("data.txt", "a")

if os.path.exists("links.txt"):
    os.remove("links.txt")

g = open("links.txt", "a")

for i in range(0, runs_count, 200):
    url = "https://www.speedrun.com/api/v1/runs?max=200&offset=" + str(i) + "&status=verified&game=" + game_id
    response = requests.get(url)
    f.write(response.text)
    data = response.text
    Links = []
    for k in range(len(data)):
        if data[k] == 'v' and data[k+1] == 'i':
            word = str(data[k])
            for j in range(22):
                word += str(data[k+j+1])
            if word == "videos\":{\"links\":[{\"uri":
                done = False
                counter = 26
                link = str()
                while not done:
                    link += str(data[k+counter])
                    if data[k+counter+1] == '"':
                        done = True
                    counter += 1
                Links += [link]
    for k in range(len(Links)):
        g.write(Links[k])
        g.write('\n')
    
g.close()

print("Done....Data of "+str(runs_count)+" runs stored in data.txt and their links in links.txt")
print("\nConnecting to Google API to get info about the youtube VODs.......type 'skip' instead of entering your API key to skip this step")
api_key = input("\nEnter your Google API Key: ")

if(api_key != "skip"):
    print("\nAuthenticating with Google API......")
    print("(This may take a while especially for games with a lot of runs)")
    f = open("links.txt", "r")

    data = str(f.read())
    YTLinks = []
    word = str()
    done = bool()
    counter = int()
    link = str()

    for i in range(len(data)):
        if (data[i] == 'y' and data[i+1] == 'o'):
            word = str(data[i])
            for j in range(8):
                word += str(data[i+j+1])
            if word == "youtube.c":
                done = False
                counter = 20
                link = str()
                while not done:
                    link += str(data[i+counter])
                    if counter == 30:
                        done = True
                    counter += 1
                YTLinks += [link]
            if word == "youtu.be/":
                done = False
                counter = 9
                link = str()
                while not done:
                    link += str(data[i+counter])
                    if counter == 19:
                        done = True
                    counter += 1
                YTLinks += [link]

    if os.path.exists("ytdata.txt"):
        os.remove("ytdata.txt")

    f = open("ytdata.txt", "a")

    counter = 0
    batch = str()

    for i in range(len(YTLinks)):
        batch = batch + YTLinks[i]
        counter += 1
        if counter != 50:
            batch = batch + ","
        if counter == 50:
            counter = 0
            response = requests.get("https://www.googleapis.com/youtube/v3/videos?id="+batch+"&part=status&key="+api_key)
            f.write(response.text)
            batch = ""
    if counter != 50:
        response = requests.get("https://www.googleapis.com/youtube/v3/videos?id="+batch[:-1]+"&part=status&key="+api_key)
        f.write(response.text)

    f = open("ytdata.txt", "r")

    data = str(f.read())
    FilteredLinks = []
    word = str()
    done = bool()
    counter = int()
    link = str()

    for i in range(len(data)):
        if data[i] == 'i':
            word = str(data[i])
            for j in range(3):
                word += str(data[i+j+1])
            if word == "id\":":
                done = False
                counter = 6
                link = str()
                while not done:
                    link += str(data[i+counter])
                    if counter == 16:
                        done = True
                    counter += 1
                FilteredLinks += [link]

    f = open("missinglinks.txt", "a")
    g = open("data.txt", "r")
    data = str(g.read())
    word = str()
    offset = 0
    f.write("\nRuns with unplayable YouTube VODs:\n\n")
    for i in range(len(FilteredLinks)):
        if(FilteredLinks[i] != YTLinks[i+offset]):
            run_id = str()
            for j in range(len(data)-len(YTLinks[i+offset])):
                word = str()
                for k in range(len(YTLinks[i+offset])):
                    word += str(data[j+k])
                if word == YTLinks[i+offset]:
                    k=0
                    while not(str(data[j-k])=="i" and str(data[j-k+1])=="d" and str(data[j-k+2])=="\""):
                        k+=1
                    k-=5
                    while not(str(data[j-k])=="\""):
                        run_id += str(data[j-k])
                        k-=1
                    run_url = "https://www.speedrun.com/"+game_abbr+"/run/"+run_id
                    f.write(run_url)
                    f.write("\n")
                    offset += 1
                    break 
    print("Done......Links to all runs with missing youtube VODs stored to missinglinks.txt")

print("\nConnecting to Twitch API to get info about the twitch VODs.......type 'skip' instead of entering your Client-ID to skip this step")
twitch_cid = input("\nEnter your Twitch dev Client-ID: ")
if(twitch_cid != "skip"):
    twitch_auth = input("Enter your Twitch API Auth Key (include the type of key as well ('Bearer', etc.): ")
    print("\nAuthenticating with Twitch API......")
    print("(This may take a while especially for games with a lot of runs)")
    f = open("links.txt", "r")

    data = str(f.read())
    TwiLinks = []
    word = str()
    done = bool()
    counter = int()
    link = str()

    for i in range(len(data)):
        if data[i] == 't':
            word = str(data[i])
            for j in range(16):
                word += str(data[i+j+1])
            if word == "twitch.tv/videos/":
                done = False
                counter = 17
                link = str()
                while not done:
                    link += str(data[i+counter])
                    if data[i+counter+1] == '\n' or data[i+counter+1] == '?':
                        done = True
                    counter += 1
                TwiLinks += [link]

    if os.path.exists("twitchdata.txt"):
        os.remove("twitchdata.txt")

    f = open("twitchdata.txt", "a", encoding='utf-8')

    counter = 0
    batch = str()

    headersdef = {
        'Client-ID': twitch_cid,'Authorization': twitch_auth}

    for i in range(len(TwiLinks)):
        batch = batch + TwiLinks[i]
        counter += 1
        if counter != 100:
            batch = batch + ","
        if counter == 100:
            counter = 0
            response = requests.get("https://api.twitch.tv/helix/videos?id="+batch,headers=headersdef)
            f.write(response.text)
            batch = ""
    
    if counter != 100:
        response = requests.get("https://api.twitch.tv/helix/videos?id="+batch[:-1],headers=headersdef)
        f.write(response.text)
    
    f = open("twitchdata.txt", "r", encoding='utf-8')

    data = str(f.read())
    FilteredLinks = []
    word = str()
    done = bool()
    counter = int()
    link = str()

    for i in range(len(data)):
        if data[i] == '"' and data[i+1] == 'i':
            word = str(data[i])
            for j in range(5):
                word += str(data[i+j+1])
            if word == "\"id\":\"":
                done = False
                counter = 6
                link = str()
                while not done:
                    link += str(data[i+counter])
                    if data[i+counter+1] == '"':
                        done = True
                    counter += 1
                FilteredLinks += [link]
                
    f = open("missinglinks.txt", "a")
    g = open("data.txt", "r")
    f.write("\nRuns with unplayable Twitch VODs:\n\n")
    data = str(g.read())
    word = str()
    offset = 0
    FilteredLinks.sort()
    TwiLinks.sort()
    for i in range(len(FilteredLinks)):
        if(FilteredLinks[i] != TwiLinks[i+offset]):
            run_id = str()
            for j in range(len(data)-len(TwiLinks[i+offset])):
                word = str()
                for k in range(len(TwiLinks[i+offset])):
                    word += str(data[j+k])
                if word == TwiLinks[i+offset]:
                    k=0
                    while not(str(data[j-k])=="i" and str(data[j-k+1])=="d" and str(data[j-k+2])=="\""):
                        k+=1
                    k-=5
                    while not(str(data[j-k])=="\""):
                        run_id += str(data[j-k])
                        k-=1
                    run_url = "https://www.speedrun.com/"+game_abbr+"/run/"+run_id
                    f.write(run_url)
                    f.write("\n")
                    offset += 1
                    break
    print("Done......Links to all runs with missing twich VODs stored to missinglinks.txt")
print("Program has finished Running")
dummy = input("Press any key to exit")