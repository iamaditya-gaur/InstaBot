#TODO complete the objectives for get another user's post sec.
#TODO add a parameter in get_posts to check for menu call or funcn call
# -*- coding: UTF-8 -*-
import requests
import urllib
from nltk.corpus import wordnet
# A global variable for storing an access token.
APP_ACCESS_TOKEN = '648921853.d9f41e8.a9e9b36da55647b1ac5841df098222b5'
# Global variable for storing the base url
BASE_URL = 'https://api.instagram.com/v1/'

# Method to get the User ID with the help of it's username
def get_user_id(user_name):
    request_url = BASE_URL + "users/search?q=%s&access_token=%s" %(user_name , APP_ACCESS_TOKEN)
    user_id = requests.get(request_url).json()
    if user_id["meta"]["code"] is 200:
        if len(user_id["data"]):
            return int((user_id["data"][0]["id"]))
        else:
            return None

    else:
        print("Response code other than 200 received!!")
        print("Error type : %s") %(user_id["meta"]["error_type"])

# Method to Display the user info, let's you choose b/w self info and info using User ID
def get_info(user_name):
    ans = raw_input("1. Carry the operation for yourself.\n2. Carry the operation for some other user .")
    if ans == '1':
        request_url = BASE_URL + "users/self/?access_token=%s" %(APP_ACCESS_TOKEN)
        user_info = requests.get(request_url).json()
        if user_info["meta"]["code"] is 200:
            if len(user_info["data"]):
                print("Username : %s") %(user_info["data"]["username"])
                print("Full Name : %s") % (user_info["data"]["full_name"])
                print("Bio : %s") % (user_info["data"]["bio"])
                print("Followers : %s") % (user_info["data"]["counts"]["followed_by"])
                print("Follows : %s") % (user_info["data"]["counts"]["follows"])
                print("Number of posts : %s") % (user_info["data"]["counts"]["media"])
            else:
                exit()
        else:
            print("Response code other than 200 received!!")
            print("Error type : %s") % (user_info["meta"]["error_type"])
    elif ans == '2' :
        user_name = raw_input("Enter the username of the user : ")
        get_id = str(get_user_id(user_name))
        if get_id is None:
            print("User not found !!")
        else:
            request_url = BASE_URL + "users/%s/?access_token=%s" %(get_id,APP_ACCESS_TOKEN)
            user_info = requests.get(request_url).json()
            if user_info["meta"]["code"] is 200:
                if user_info["data"]:
                    print("Username : %s") % (user_info["data"]["username"])
                    print("Full Name : %s") % (user_info["data"]["full_name"])
                    print("Bio : %s") % (user_info["data"]["bio"])
                    print("Followers : %s") % (user_info["data"]["counts"]["followed_by"])
                    print("Follows : %s") % (user_info["data"]["counts"]["follows"])
                    print("Number of posts : %s") % (user_info["data"]["counts"]["media"])
                else:
                    return None
            else:
                print("Response code other than 200 received!!")
                print("Error type : %s") % (user_info["meta"]["error_type"])
    else:
        print("Please select correct Input!!")

# Method to retrieve the recent posts , let's you choose b/w your posts or using different User ID and returns the post ID
# and returns none if there is no data.
def get_posts(user_name):
    ans = raw_input("1. Carry the operation for yourself.\n2. Carry the operation for some other user .")
    if ans == '1':
        user_info = requests.get(BASE_URL + ("users/self/media/recent/?access_token=%s") %(APP_ACCESS_TOKEN)).json()
        if user_info["meta"]["code"] is 200:
            if len(user_info["data"]) :
                if user_info["data"][0]["type"] == "carousel":
                    i = len(user_info["data"][0]["carousel_media"])
                    index = 0
                    for index in range(i):
                        img_url = user_info["data"][0]["carousel_media"][index]["images"]["standard_resolution"]["url"]
                        img_name = str(user_info["data"][0]["id"]) + str(index+1) + '.jpeg'
                        urllib.urlretrieve(img_url,img_name)
                    return user_info["data"][0]["id"]


                elif user_info["data"][0]["type"] == "image":
                    img_url = user_info["data"][0]["images"]["standard_resolution"]["url"]
                    img_name = str(user_info["data"][0]["id"]) + '.jpeg'
                    urllib.urlretrieve(img_url,img_name)
                    return user_info["data"][0]["id"]
                else:
                    print("This type of media isn't supported yet!! Stay Tuned for more.")
                    exit()
            else:
                exit()

        else:
            print("Response code other than 200 received!!")
            print("Error type : %s") % (user_info["meta"]["error_type"])
    elif ans == '2':
        user_name = raw_input("Enter the username of the user : ")
        usr_id = get_user_id(user_name)
        if usr_id is None:
            print ("Sorry, the user name was not found!!")
        else:
            usr_id = str(usr_id)
            user_info = requests.get((BASE_URL + "users/%s/media/recent/?access_token=%s") %(usr_id , APP_ACCESS_TOKEN)).json()
            if user_info["meta"]["code"] is 200:
                if len(user_info["data"]) :
                    if user_info["data"][0]["type"] == "carousel":
                        i = len(user_info["data"][0]["carousel_media"])
                        index = 0
                        for index in range(i):
                            img_url = user_info["data"][0]["carousel_media"][index]["images"]["standard_resolution"]["url"]
                            img_name = str(user_info["data"][0]["id"]) + str(index+1) + '.jpeg'
                            urllib.urlretrieve(img_url,img_name)
                        return user_info["data"][0]["id"]
                    elif user_info["data"][0]["type"] == "image":
                        img_url = user_info["data"][0]["images"]["standard_resolution"]["url"]
                        img_name = str(user_info["data"][0]["id"]) + '.jpeg'
                        urllib.urlretrieve(img_url,img_name)
                        return user_info["data"][0]["id"]
                    else:
                        print("This type of media isn't supported yet!! Stay Tuned for more.")
                        exit()
                else:
                    return None

            else:
                print("Response code other than 200 received!!")
                priint("Error type : %s") %(user_info["meta"]["error_type"])
    else:
        print "Enter a correct value!! "
# Method to download the recent liked media of the user.
def recent_liked_media():
    user_info = requests.get(BASE_URL + ("users/self/media/recent/?access_token=%s") % (APP_ACCESS_TOKEN)).json()
    if user_info["meta"]["code"] is 200:
        img_url = user_info["data"][0]["images"]["standard_resolution"]["url"]
        img_name = str(user_info["data"][0]["id"]) + '.jpeg'
        urllib.urlretrieve(img_url , img_name)
    else:
        print("Response Code other than 200 recieved!!")

# Method to post a like on the recent media accepting the username of the user and download the post for confirmation.
def post_like(user_name):
    media_id = get_posts(user_name)
    if media_id == None:
        print ("Username not found!!")
    else:
        url = BASE_URL +("media/%s/likes") %(media_id)
        payload = {"access_token":APP_ACCESS_TOKEN}
        like_info = requests.post(url , payload).json()
        if like_info["meta"]["code"] is 200:
            print("Your like successfully posted.")
        else:
            print("Like was not posted due to some error.")

# Method to get a list of all the comments on a user's post and download the post for confirmation.
def get_comments(user_name):
    usr_id = get_posts(user_name)
    comment_info = requests.get(BASE_URL+ ("media/%s/comments?access_token=%s") %(usr_id , APP_ACCESS_TOKEN)).json()
    if comment_info["meta"]["code"] is 200:
        if comment_info["data"]:
            no_of_comm = len(comment_info["data"])
            print("List of comments on the post :")
            for index in range(no_of_comm):
                print("%s. %s") %(str(index+1) , comment_info["data"][index]["text"])
        else:
            print("No comment was found !!")
    else:
        print("Response code other than 200 found!!")

# Method to post a comment on a user's recent post using it's user name and download the post for confirmation.
def post_comment(user_name):
    media_id = get_posts(user_name)
    url = (BASE_URL + 'media/%s/comments') % (media_id)
    comment = raw_input("Enter the comment you want to post : ")
    payload = {"access_token": APP_ACCESS_TOKEN, "text": comment}
    comment_info = requests.post(url, payload).json()
    if comment_info["meta"]["code"] is 200:
        print("Your comment was successfully posted!!")
    else:
        print("Response code other than 200 was recieved!!")

# Method to fetch the posts of disaster struck areas by analysing their caption and taking location as input.
def fetch_special_posts(user_name):
    try:
        location = raw_input("Enter the location for which you want to fetch posts for : ")
        google_url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s" %(location)
        location_info = requests.get(google_url).json()
        longitude = str(location_info["results"][0]["geometry"]["location"]["lng"])
        latitude = str(location_info["results"][0]["geometry"]["location"]["lat"])
        location_info = requests.get((BASE_URL + "locations/search?lat=%s&lng=%s&access_token=%s") % (latitude,longitude,APP_ACCESS_TOKEN)).json()
        if location_info["meta"]["code"] is 200:
            if location_info["data"]:
                i = 0
                i = len(location_info["data"])
                if i is 0:
                    print("Sorry, no reults were found for the location that you entered!!")
                else:
                    print("%s Locations found for your search!!\nSelect one from the following list to proceed : ") %(str(i))
                    index = 0
                    for index in range(i):
                        print(("%d. %s") %(index+1 , location_info["data"][index]["name"]))
                    ans = raw_input("Enter your choice : ")
                    if ans < (i+1):
                        print "Enter correct value!!"
                    else:
                        ans = int(ans)
                        ans -= 1
                        location_id = str(location_info["data"][ans]["id"])
                        user_info = requests.get(BASE_URL + ("users/self/media/recent/?access_token=%s") % (APP_ACCESS_TOKEN)).json()
                        if user_info["meta"]["code"] is 200:
                            l = 0
                            l = len(user_info["data"])
                            if l is 0:
                                print("Sorry, this user has no posts!!")
                            else:
                                flag = 0
                                i = 0
                                for i in range(l):
                                    if user_info["data"][i]["location"]:
                                        if (str(user_info["data"][i]["location"]["id"]) == location_id):
                                            # Checking if the post is related to natural disaster using wordnet and then downloding it.
                                            #a = "tsunami, volcano, tornado, avalanche, earthquake, blizzard, drought, bushfire, tremor, dust_storm, magma, twister, windstorm, heat-wave, cyclone, forest-fire, flood, fire, hailstorm, lava, lightning, natural_disasters, hail, hurricane, seismic, erosion, whirlpool, Richter_scale, whirlwind, thunderstorm, barometer, blackout, low-pressure, volt, snowstorm, rainstorm, storm, violent_storm, sandstorm, Beaufort_scale, cumulonimbus, destruction, cataclysm, destroy, arsonist, wind_scale, arson, rescue, permafrost, disaster"
                                            a="weekend"
                                            list = a.split(', ')
                                            l = len(list)
                                            index = 0
                                            #checks the caption for the keywords
                                            for index in range(l):
                                                syn = wordnet.synsets(list[index])
                                                if syn:
                                                    j = len(syn)
                                                    for k in range(j):
                                                        if syn[k].lemmas():
                                                            a = len(syn[k].lemmas())
                                                            for b in range(a):
                                                                cap = user_info["data"][i]["caption"]["text"]
                                                                cap = cap.split()
                                                                x = len(cap)
                                                                for y in range(x):
                                                                    if cap[y] == syn[k].lemmas()[b].name():
                                                                        flag = 1
                                            if flag is 0:
                                                print("Sorry, No post was found with similar conditions!!")
                                            else:
                                                print("Matching Post was found, it will now be downloaded!")
                                                if user_info["data"][i]["type"] == "carousel":
                                                    s = len(user_info["data"][i]["carousel_media"])
                                                    index = 0
                                                    for index in range(s):
                                                        img_url = user_info["data"][i]["carousel_media"][index]["images"]["standard_resolution"]["url"]
                                                        img_name = str(user_info["data"][i]["id"]) + str(index + 1) + '.jpeg'
                                                        urllib.urlretrieve(img_url, img_name)
                                                elif user_info["data"][i]["type"] == "image":
                                                    img_url = user_info["data"][i]["images"]["standard_resolution"]["url"]
                                                    img_name = str(user_info["data"][i]["id"]) + '.jpeg'
                                                    urllib.urlretrieve(img_url, img_name)
                                                exit()
                                        else:
                                            print("No post was found for the chosen location!")
                        else:
                            print("Sorry, some error occurred!! ")


        else:
            print("Response code other than 200 received !!")
            print("Error type : %s") %(location_info["meta"]["error_type"])
    except ValueError:
        print("Enter a valid value !!")
    except IndexError:
        print("Enter a valid value !!")


# Method to start the bot.
def start_bot(user_name):
    while True:
        print '\nHere are your menu options:'
        print "a.Get details about a user\n"
        print "b.Get the recent post of a user\n"
        print "c.Like the recent  post of a user\n"
        print "d.Get the recent media liked by you\n"
        print "e.Get a list of comments on the recent post of a user\n"
        print "f.Make a comment on the recent post of a user\n"
        print "g.Fetch special posts related to natural disasters for a particular location\n"
        print "h.Exit"
        choice = raw_input("Enter you choice: ")
        if choice.upper() == 'A':
            get_info(user_name)
        if choice.upper() == 'B':
            get_posts(user_name)
        if choice.upper() == 'C':
            post_like(user_name)
        if choice.upper() == 'D':
            recent_liked_media()
        if choice.upper() == 'E':
            get_info(user_name)
        if choice.upper() == 'F':
            post_comment(user_name)
        if choice.upper() == 'G':
            fetch_special_posts(user_name)
        if choice.upper() == 'H':
            exit()
print '\n'
print 'Hey! Welcome to instaBot!'
user_name = raw_input("Kindly enter your username for which the Access Token is valid : ")
start_bot(user_name)


