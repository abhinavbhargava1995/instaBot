# My Instagram username is abhinav1995b
# Install requests library to make network requests
import requests,urllib
# regular expression(re)
import re
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

# Generate an access token from instagram.com/developer
APP_ACCESS_TOKEN = '4006838471.b6bbc2d.4687b8894558469f82f4817b1816de92'
# Base URL of instagram
BASE_URL = 'https://api.instagram.com/v1/'

# Function declaration to get our own information
def self_info():

    request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'

# Function declaration to get the ID of a user by username
def get_user_id(insta_username):

    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()

# Function declaration to get the info of a user by username
def get_user_info(insta_username):

    user_id = get_user_id(insta_username)

    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'

# Function declaration to get your recent post
def get_own_post():

  request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
  print 'GET request url : %s' % (request_url)
  own_media = requests.get(request_url).json()

  if own_media['meta']['code'] == 200:
     if len(own_media['data']):
        image_name = own_media['data'][0]['id'] + '.jpeg'
        image_url = own_media['data'][0]['images']['standard_resolution']['url']
        urllib.urlretrieve(image_url, image_name)
        print 'Your image has been downloaded!'
     else:
        print 'Post does not exist!'
  else:
     print 'Status code other than 200 received!'
  return None

# Function declaration to get the recent post of a user by username
def get_user_post(insta_username):

    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url=(BASE_URL + 'users/%s/media/recent/?access_token=%s') %(user_id,APP_ACCESS_TOKEN)
    user_media=requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'

        else:
            print 'There is no recent post!'
    else:
        print 'status code other then 200'

# Function declaration to get the ID of the recent post of a user by username
def get_post_id(insta_username):
    user_id = get_user_id(insta_username)

    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()

# Function declaration to like the recent post of a user
def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url=(BASE_URL + 'media/%s/likes') % (media_id)
    payload={'access_token':APP_ACCESS_TOKEN}
    post_a_like = requests.post(request_url, payload).json()

    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'

# Function declaration to make a comment on the recent post of the user
def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("your comment: ")
    if re.search(r'[a-z]+', comment_text, re.IGNORECASE) and comment_text == comment_text.upper():
        print 'Sorry!! you cannot enter a comment with all capital alphabets .'
    elif len(comment_text) > 300:
        print "Sorry!!Your comment can't be added it contains characters having length more than 300"
    elif len(re.findall(r'#[^#]+\b', comment_text, re.UNICODE | re.MULTILINE)) > 4:
           print 'The comment cannot contain more than 4 hashtags.'
    elif len(re.findall(r'\bhttps?://\S+\.\S+', comment_text)) > 1:
        print 'The comment cannot contain more than 1 URL.'
    else:
        payload = {"access_token": APP_ACCESS_TOKEN, "text": comment_text}
        request_url = (BASE_URL + 'media/%s/comments') % (media_id)
        print 'POST request url : %s' % (request_url)
        make_comment = requests.post(request_url, payload).json()
        if make_comment['meta']['code'] == 200:
            print "Successfully added a new comment!"
        else:
            print "Unable to add comment. Try again!"

# this function is used to get list of comments on the post of user
def list_of_comments(insta_username):
    media_id=get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments?access_token=%s') % (media_id,APP_ACCESS_TOKEN)
    get_comments=requests.get(request_url).json()
    i=0
    if get_comments['meta']['code']==200:
        for ele in get_comments['data']:
            print get_comments['data'][i]['from']['username']+":"+ get_comments['data'][i]['text']
            i=i+1
    else:
        print 'Status code other than 200 received!'

# by using this function we can get list of person which likes the post of the user
def list_of_likes(insta_username):
    media_id=get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes?access_token=%s') % (media_id,APP_ACCESS_TOKEN)

    get_likes=requests.get(request_url).json()
    i=0
    if get_likes['meta']['code']==200:
        for ele in get_likes['data']:
            print get_likes['data'][i]['username']
            i=i+1
    else:
        print 'Status code other than 200 received!'

# this function download that image which is recently liked by the owner of instabot
def recent_media_liked():

    request_url = (BASE_URL + 'users/self/media/liked?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'There is no recent post!'
    else:
        print 'status code other then 200'

# this function will allow the user to enter a username and he post no which user want to access or fetch
def get_media_of_your_choice(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'user does not exist!!'
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    user_media = requests.get(request_url).json()
    if user_media['meta']['code'] == 200:
        if len(user_media['data']):

            post_number = raw_input("enter no of post which you want : ")

            post_number = int(post_number)

            x = post_number - 1
            if x < len(user_media['data']):
                image_name = user_media['data'][x]['id'] + '.jpeg'
                image_url = user_media['data'][x]['images']['standard_resolution']['url']
                urllib.urlretrieve(image_url, image_name)
                print 'Your image has been downloaded!'

            else:

                print "This post is not available !! Please enter a valid post number "
        else:
            print'user media does not exist'
    else:
        print 'status code other then 200'

# code to compare negative and positive comments on a particular's posts and plot it on a pie chart.
def positive_vs_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()
    count_of_positive_comments=0
    count_of_negative_comments =0

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            for x in range(0, len(comment_info['data'])):
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text,analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                     count_of_negative_comments=count_of_negative_comments+1
                     print count_of_negative_comments
                     print 'Negative comment : %s' % (comment_text)
                else:
                     count_of_positive_comments=count_of_positive_comments+1
                     print count_of_positive_comments
                     print 'Positive comment : %s\n' % (comment_text)

        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'
    labels = ['Positive Comments', 'Negative Comments']
    numbers = [count_of_positive_comments, count_of_negative_comments]
    color = ['blue', 'red']
    explode = (0.1, 0)
    plt.pie(numbers, explode=explode, labels=labels, colors=color,autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.show()

# starting the instaBot

def start_bot():
    print 'Hey! Welcome to instaBot!'
    while True:
        print 'Here are your menu options:'
        print "a.Get your own details\n"
        print "b.Get details of a user by username\n"
        print "c.Get details of a user post\n"
        print "d.Get your own recent post\n"
        print "e.Like the recent post of a user\n"
        print "f.Make a comment on the recent post of a user\n"
        print "g.get list of comments on the recent post of a user\n"
        print "h.get list of likes on the recent post of a user\n"
        print "i.get recent media media liked by user\n"
        print "j.get_media_of_your_choice\n"
        print "k.get no of negative and positive comments on the recent post of a user\n"
        print "l.Exit"

        choice = raw_input("Enter you choice: ")
        if choice == "a":
            self_info()

        elif choice == "b":
            insta_username = raw_input("Enter the username of the user: ")
            if len(insta_username)> 0 and insta_username.isspace() == False and insta_username.isdigit()==False:
                if not set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):
                    get_user_info(insta_username)
                else:
                    print "Sorry!! Add user_name whose information you want to get"

            else:
                print "Please enter valid username"

        elif choice == "c":
            insta_username = raw_input("Enter the username of the user: ")
            if len(insta_username)> 0 and insta_username.isspace() == False and insta_username.isdigit()==False:
                if not set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):
                    get_user_post(insta_username)
                else:
                    print "Sorry!! Add user_name whose information you want to get"
            else:
                print "Please enter valid username"

        elif choice == "d":
            get_own_post()

        elif choice == "e":
            insta_username = raw_input("Enter the username of the user: ")
            if len(insta_username)> 0 and insta_username.isspace() == False and insta_username.isdigit()==False:
                if not set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):
                    like_a_post(insta_username)
                else:
                    print "Sorry!! Add user_name whose information you want to get"
            else:
                print "Please enter valid username"

        elif choice == "f":
            insta_username = raw_input("Enter the username of the user: ")
            if len(insta_username)> 0 and insta_username.isspace() == False and insta_username.isdigit()==False:
                if not set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):
                    post_a_comment(insta_username)
                else:
                    print "Sorry!! Add user_name whose information you want to get"
            else:
                print "Please enter valid username"

        elif choice == "g":
            insta_username = raw_input("Enter the username of the user: ")
            if len(insta_username)> 0 and insta_username.isspace() == False and insta_username.isdigit()==False:
                if not set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):
                    list_of_comments(insta_username)
                else:
                    print "Sorry!! Add user_name whose information you want to get"
            else:
                print "Please enter valid username"

        elif choice == "h":
            insta_username = raw_input("Enter the username of the user: ")
            if len(insta_username)> 0 and insta_username.isspace() == False and insta_username.isdigit()==False:
                if not set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):
                    list_of_likes(insta_username)
                else:
                    print "Sorry!! Add user_name whose information you want to get"
            else:
                print "Please enter valid username"

        elif choice == "i":
            recent_media_liked()

        elif choice == "j":
            insta_username = raw_input("Enter the username of the user: ")
            if len(insta_username)> 0 and insta_username.isspace() == False and insta_username.isdigit()==False:
                if not set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):
                    get_media_of_your_choice(insta_username)
                else:
                    print "Sorry!! Add user_name whose information you want to get"
            else:
                print "Please enter valid username"

        elif choice == "k":
            insta_username = raw_input("Enter the username of the user: ")
            if len(insta_username)> 0 and insta_username.isspace() == False and insta_username.isdigit()==False:
                if not set('[~!@#$%^&*()+{}":;\']" "').intersection(insta_username):
                    positive_vs_negative_comment(insta_username)
                else:
                    print "Sorry!! Add user_name whose information you want to get"
            else:
                print "Please enter valid username"

        elif choice == "l":
            exit()

        else:
            print "Sorry!! wrong choice"

start_bot()