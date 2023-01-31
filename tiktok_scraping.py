#import all dependencies needed
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from random import randint
from time import sleep

#Assign the link to a variable so that it will be easier to pass through later
link = 'https://www.tiktok.com/@charlidamelio'

#Since we were not able to get the website code using "re" or "requests" we would use selenium's webdriver
driver = webdriver.Chrome('driver/chromedriver')
driver.get(link)

sleep(randint(20, 25))

#Once the link opens, we scroll about three times which gets us a minimum of about 50 posts if the user has uploaded. If the user has uploaded less or has not uploaded at all, it will stop on the last post
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
sleep(randint(10, 20))

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
sleep(randint(10, 18))

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
sleep(randint(10, 22))

#Get the webpage's code
soup = BeautifulSoup(driver.page_source, 'html.parser')

#Declare empty unordered lists so that we can append the scrapped results later
user_Name = []
user_Image = []
user_About = []
user_Likes = []
user_Followers = []
user_Following = []
account_post = []
average_engagement = []

#try to identify if there are any posts in the user's link
#if THERE IS POSTS, 
if len(soup.find_all('div', {'class': 'tiktok-x6y88p-DivItemContainerV2 e19c29qe7'})) != 0:
    i = 0
    #find the html class of the posts and iterate through posting divs 50 times to get link (If account does not have 50 posts, iterates to the total number of posts the account has)
    for posts in soup.find_all('div', {'class': 'tiktok-x6y88p-DivItemContainerV2 e19c29qe7'}):
        if i == 50:
            break
        try:
            post = posts.find('div', {'class': 'tiktok-yz6ijl-DivWrapper e1cg0wnj1'}).a['href']
        except Exception as e:
            continue
        account_post.append(post)
        i += 1
    #set the i_value to the length of the appended posts so that we will have the same number of lengths on the appended dictionaries
    i_value = len(account_post)

#if THERE IS NO POST
else:
    #Set i_value to 0 so that it does not iterate later and append the account post to be set to "No Posts Found" when adding it to the CSV
    i_value = 0
    post = "No Posts Found"
    account_post.append(post)

#Find the page section to get a traget to scrape
page_section = soup.find('div', {'class': 'tiktok-1g04lal-DivShareLayoutHeader-StyledDivShareLayoutHeaderV2 enm41492'})

#get the username of the account
userName_div = page_section.find('div', {'class': 'tiktok-1hdrv89-DivShareTitleContainer ekmpd5l3'})
userName = userName_div.find('h2').text.strip()

#get the user imge link of the account
proilePic_div = page_section.find('div', {'class': 'tiktok-uha12h-DivContainer e1vl87hj1'})
userImage = proilePic_div.find('span').img['src']

#call other css functions and obtain the number of people the user is following
countInfo = page_section.find('h2', {'class': 'tiktok-7k173h-H2CountInfos e1457k4r0'})
#get info to all the information regarding Following, Follower and Likes
FollwInfo = countInfo.find_all('div', {'class': 'tiktok-1kd69nj-DivNumber e1457k4r1'})
#get the follower info by calling the first div class in the list
Following = FollwInfo[0].text.strip()
#replace the "Following" text since we only want the number
Following = Following.replace('Following', '')

#if the user has a "K", convert it to an actual number (Thousads) (NoTe: This is used in order calculate the average engagement of specific posts)
if 'K' in Following:
    Following = Following.replace('K', '')
    Following = float(Following)
    Following = Following * 1000

#if the user has a "M", convert it to an actual number (Millions) (NoTe: This is used in order calculate the average engagement of specific posts)
elif 'M' in Following:
    Following = Following.replace('M', '')
    Following = float(Following)
    Following = Following * 1000000

#if the user has a "B", convert it to an actual number (Billions) (NoTe: This is used in order calculate the average engagement of specific posts)
elif 'B' in Following:
    Following = Following.replace('B', '')
    Following = float(Following)
    Following = Following * 1000000000 

#get the follower info by calling the second div class in the list
Followers = FollwInfo[1].text.strip()
#replace the "Followers" text since we only want the number
Followers = Followers.replace('Followers', '')

#if the user has a "K", convert it to an actual number (Thousads) (NoTe: This is used in order calculate the average engagement of specific posts)
if 'K' in Followers:
    Followers_int = Followers.replace('K', '')
    Followers_int = float(Followers_int)
    Followers_int = Followers_int * 1000

#if the user has a "M", convert it to an actual number (Millions) (NoTe: This is used in order calculate the average engagement of specific posts)
elif 'M' in Followers:
    Followers_int = Followers.replace('M', '')
    Followers_int = float(Followers_int)
    Followers_int = Followers_int * 1000000

#if the user has a "B", convert it to an actual number (Billions) (NoTe: This is used in order calculate the average engagement of specific posts)
elif 'B' in Followers:
    Followers_int = Followers.replace('B', '')
    Followers_int = float(Followers_int)
    Followers_int = Followers_int * 1000000000 


#get the likes info by calling the third div class in the list
Likes = FollwInfo[2].text.strip()

#replace the "Likes" text since we only want the number
Likes = Likes.replace('Likes', '')

#if the user has a "K", convert it to an actual number (Thousads)
if 'K' in Likes:
    Likes = Likes.replace('K', '')
    Likes = float(Likes)
    Likes = Likes * 1000

#if the user has a "M", convert it to an actual number (Millions)
elif 'M' in Likes:
    Likes = Likes.replace('M', '')
    Likes = float(Likes)
    Likes = Likes * 1000000

#if the user has a "B", convert it to an actual number (Billions)
elif 'B' in Likes:
    Likes = Likes.replace('B', '')
    Likes = float(Likes)
    Likes = Likes * 1000000000 

#call other css functions and obtain the user's about page
About = page_section.find('h2', {'class': 'tiktok-1n8z9r7-H2ShareDesc e1457k4r3'}).text.strip()
#replace any space so that it won't have specific texts when going to the csv file
About = About.replace('\n', ' ')

#try to identify the number of views the account has in the posts
#if THERE IS POSTS
if len(soup.find_all('div', {'class': 'tiktok-x6y88p-DivItemContainerV2 e19c29qe7'})) != 0:
    i = 0
    #find the html class of the posts and iterate through posting divs i_value times to get the number of views
    for view_count in soup.find_all('div', {'class': 'tiktok-11u47i-DivCardFooter e148ts220'}):
        if i == i_value:
            break

        #get the number of views a specific post has
        viewCount = view_count.find('strong').text.strip()

        #then approximate the result to change in to an approximation of what is written (i.e 2K = 2000)
        if 'K' in viewCount:
            viewCount = viewCount.replace('K', '')
            viewCount = float(viewCount)
            viewCount = viewCount * 1000
        elif 'M' in viewCount:
            viewCount = viewCount.replace('M', '')
            viewCount = float(viewCount)
            viewCount = viewCount * 1000000
        elif 'B' in viewCount:
            viewCount = viewCount.replace('B', '')
            viewCount = float(viewCount)
            viewCount = viewCount * 1000000000
        viewCount = float(viewCount)
        #divide the viewCount to the account's number of followers so that we get the average engagement and then append it
        viewCount = viewCount/Followers_int
        average_engagement.append(viewCount)
        i += 1

#if THERE IS NO POST
else:
    #assign viewCount to "N/A" since the account has no uploaded videos hence no specific video views and append it
    viewCount = "N/A"
    average_engagement.append(viewCount)

#if the account has posts, we append the following (duplicate) "i_value" times inorder to get the same number of columns that match the accounts posts and average engagemnt
if viewCount != "N/A":
    for i in range(i_value):
        user_Name.append(userName)
        user_Image.append(userImage)
        user_Following.append(Following)
        user_Followers.append(Followers_int)
        user_Likes.append(Likes)
        user_About.append(About)

#if account has no posts, append them once so that we would have one row
else:
    user_Name.append(userName)
    user_Image.append(userImage)
    user_Following.append(Following)
    user_Followers.append(Followers_int)
    user_Likes.append(Likes)
    user_About.append(About)

#create a dictionary so that we can put the appended lists in a Data Frame
dict = {'User Name': user_Name,
        'User Image': user_Image,
        'User Following': user_Following,
        'Users Followers': Followers_int,
        'User Likes': user_Likes,
        'User About': user_About,
        'Post Link': account_post,
        'Average Engagement': average_engagement,
}

#save the dictonary in a Data Frame
df = pd.DataFrame(dict)

#export the resultng df to a csv file
df.to_csv('Scraped Result.csv')