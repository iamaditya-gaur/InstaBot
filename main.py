#TODO complete the objectives for get another user's post sec.
import requests
import urllib
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

# Method to Display the user info, let's you choose b/w self info and info using User ID
def get_info(user_name):
    ans=raw_input("1. Fetch your own Instagram information.\n2. Fetch someone else's Insatagram information.")
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
    elif ans == '2' :
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
    else:
        print("Please select correct Input!!")

# Method to retrieve the recent posts , let's you choose b/w your posts or using different User ID and returns the post ID
# and returns none if there is no data.
def get_posts(user_name):
    ans = raw_input("1. Fetch your own Media posts.\n2. Fetch someone else's Media posts.")
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
    elif ans == '2':
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

    else:
        print("Please select correct Input!!")

# Method to download the recent liked media of the user.
def recent_liked_media():
    user_info = requests.get(BASE_URL + ("users/self/media/recent/?access_token=%s") % (APP_ACCESS_TOKEN)).json()
    if user_info["meta"]["code"] is 200:
        img_url = user_info["data"][0]["images"]["standard_resolution"]["url"]
        img_name = str(user_info["data"][0]["id"]) + '.jpeg'
        urllib.urlretrieve(img_url , img_name)
    else:
        print("Response Code other than 200 recieved!!")

# Method to post a like on a media accepting the username of the user.
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

# Method to get a list of all the comments on a user's post
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

# Method to post a comment on a user's recent post using it's user name.
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



