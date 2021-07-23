# SRCDVD
SRCDVD (**s**peed**r**un.**c**om **D**eleted **V**ideo **D**etector) is a tool to detect runs with unviewable (deleted/private/expired) YouTube and Twitch VODs for a given game in speedrun.com
## Important Notice
We are in the process of refactoring the code, which has introduced some bugs as expected. For urgent use, check out the old branch with the code before the refactoring process - https://github.com/GMPranav/SRCDVD/tree/old
## What this tool does exactly:
This tool makes use of speedrun.com's [REST API](https://github.com/speedruncomorg/api) to gather the data of all the **verified** runs of a given game and stores it in a file named "data.txt", but the most important detail we would be needing is the video links of each run, which is isolated from "data.txt" and stored in "links.txt". It then checks for all the youtube links and twitch links in "links.txt" and gets the IDs of each VOD and checks its availability using [Google API v3](https://developers.google.com/youtube/v3) and [Twitch API](https://dev.twitch.tv/docs/api/) respectively. It then compares the IDs returned by the API to the original list to get the list of missing runs. It search for the ID in data.txt to find the src links to the appropriate runs, which is stored in "missinglinks.txt". You can skip either of YouTube or Twitch checks by tying skip instead of rhe respective authentication details.
## Prerequisites:
The program requires python app to run. Do not worry, you dont require python programming skills, this is just needed to run the .py files. The google and twitch APIs require authentication to use, so you will have to get your authentication details first. I will try to explain the process of doing so briefly. It might look complicated, but do not worry.
### Setting up Python
- Get python from https://www.python.org/

- Open command prompt, type "pip install requests" and run enter. The "requests" module for python is required for this program.

- If you get "pip is not recognised as an internal or external command", go to the python install folder, default is %UserProfile%\AppData\Local\Programs\Python\Python39

- Go to the scripts folder. Copy the folder path from the address bar.

- Open cmd and type "cd", give a space and paste the folder path and hit enter. For me it will look like this:<br>
![image](https://user-images.githubusercontent.com/54983451/126489381-b68d759d-72af-4e15-b902-ebe552d80090.png)

- Now try running "pip install requests" and it should work.
### Google API v3
- First, you have to create a project in google dev console. Here is a handy link - https://console.cloud.google.com/projectcreate

- I will name it "Example" for demo purposes. Also, you don't need to select any organisation<br>
![image](https://user-images.githubusercontent.com/54983451/126477099-a7d7ead0-ef0e-4b6a-8f13-1d86c97090fd.png)

- Now in the sidebar, go to APIs & Services > Library<br>
![image](https://user-images.githubusercontent.com/54983451/126478089-c224deca-4d4a-44d5-ad0e-1a3123534fce.png)

- In the library, seach "youtube" and click on "YouTube Data API v3"<br>
![image](https://user-images.githubusercontent.com/54983451/126478387-81416e81-7b23-4b72-bc8d-187eb4f08d28.png)

- Click "Enable"<br>
![image](https://user-images.githubusercontent.com/54983451/126478601-18c39bff-9eee-424c-a307-3b7868ef0ade.png)

- You will be redirected to a page about the overview of YouTube API usage by your project. Click on "Create Credentials"<br>
![image](https://user-images.githubusercontent.com/54983451/126478994-33a8b451-7a06-47ad-96ec-1838147b7ae2.png)

- In the next screen, select "YouTube Data API v3" as the Credential Type and select "Public Data" under "What data will you be accessing?" and click "Next"<br>
![image](https://user-images.githubusercontent.com/54983451/126479306-9c834ba9-dfe1-4bf0-a94b-f9b72ffa7e00.png)

- You will get your API Key, copy it and paste it somewhere like notepad, and click "Done"<br>
![image](https://user-images.githubusercontent.com/54983451/126479602-05d8f8fa-c34f-4d9f-8e5e-eea40deea099.png)

- Now you can close your project page and never worry about it again. There are some limtations like quota, etc. to prevent abuse but it's high enough that you won't feel it for any practical uses. If your game only has YouTube links, you can skip the next section about Twitch API and go ahead to use the tool.

### Twitch API
- First, you have to create an application in twitch dev console. Here is a handy link - https://dev.twitch.tv/console/apps/create

- I will name it "SRCDVD" for demo purposes. Set the OAuth Redirect URL to "http://localhost", Category as "Analytics Tool" and click "Create"<br>
![image](https://user-images.githubusercontent.com/54983451/126481501-1272f8b3-3ef8-47ff-ac45-c75b8ac6c3f4.png)

- Click on "Manage" beside your application in the next page<br>
![image](https://user-images.githubusercontent.com/54983451/126481763-133adb04-7843-4391-bcf1-370bc0dcbd4e.png)

- You will see a field called "Client ID" and also an option to create a "New Secret". Click on it. Now you will have both an ID and a secret, you can close your twitch dev console page for good. If you need later, you know where to find your ID and secret<br>
![image](https://user-images.githubusercontent.com/54983451/126482065-f7475550-c462-491b-b757-152e54d50409.png)

## How to use the program:
- Visit https://codeload.github.com/GMPranav/SRCDVD/zip/refs/heads/main and extract the ZIP file.
  
- I would advise keeping the contents of the program in a seperate folder.
  
- Run the program. Enter the your Twitch Client ID and secret and then your Google API key

- Enter the game's abbreviation in speedrun.com. For example, for Prince of Persia, it is "pop1".<br>
  ![image](https://user-images.githubusercontent.com/54983451/126490521-751df7cf-9e0a-4a18-b2be-1c563b830e32.png)<br>
![image](https://user-images.githubusercontent.com/54983451/126490671-3d582cbd-6a0a-401b-9242-d00ce238cb7a.png)

- After entering it will take a while especially for games with a lot of runs, so please be patient.

- Once the program has finished running, all the links of affected runs should be stored in a file called "missinglinks.txt".
  
## Purpose of this tool and disclaimers:
The primary purpose of this tool is for the moderators of the game to keep track of the runs without viewable VODs. A lot of games have a "video must" rule so this might be helpful for potentially rejecting the runs. Before doing so, please manually check if the video is indeed unplayable. This tool or its creator is not responsible for falsely rejected runs. One more thing - If a youtube video is private rather than deleted (you can tell if you open the embed in a new tab), try contacting the owner to make it unlisted/public first, they can do so in a single click and probably better than rejecting the run. At the end of the day its your decision and I just want to say I am not responsible for it.
