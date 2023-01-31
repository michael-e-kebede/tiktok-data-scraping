# TikTok Scraper
A Python script to scrape data from TikTok profiles.

## Dependencies
- pandas
- bs4
- selenium
- random
- time

## Usage
1. Assign the target TikTok profile link to a variable link
2. Use selenium's webdriver to open the link and get the page source
3. Scroll down 3 times to load more posts from the profile
4. Use BeautifulSoup to parse the page source into HTML elements
5. Find and scrape data elements such as profile name, profile picture, number of followers, number of likes, etc.
6. Store the scraped data in a list
7. If there are posts, iterate through the posts and append the post link to a list account_post
8. The script ends by checking if the profile has any posts, if not, set account_post to "No Posts Found"

## Note
The script only retrieves the first 50 posts of the target profile.
The script uses a random sleep time between 10 to 25 seconds to simulate human-like scrolling and to prevent being blocked by TikTok's servers.


