import pandas as pd
import time
from selenium import webdriver
from bs4 import BeautifulSoup as BS
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
# Initialize Selenium WebDriver (make sure to set up the correct path to your WebDriver)


# Read the CSV file
# article_list = pd.read_csv('reddit_url.csv')

# Define a function to fetch and format the content
def fetch_reddit_content(article_url):
  
    chrome_options = uc.ChromeOptions()
    chrome_options.headless=False # Uncomment if you want to run headless
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    

    driver = uc.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get(article_url)
    time.sleep(2)  # Adjust sleep time as necessary for page load
    # progress_callback(4)
    # Scroll to load all comments
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Adjust sleep time as necessary for comments load
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        
        try:
            driver.find_element(By.XPATH,'//*[@id="comment-tree"]/faceplate-partial/div[1]').click()
            time.sleep(5)
        except:
            pass
        if new_height == last_height:
            break
        last_height = new_height
    
    soup = BS(driver.page_source, 'html.parser')
    # Extract the original post description
    post_title = soup.find('h1').get_text()
    driver.save_screenshot('redot.png')
    post_desc = soup.find('div', id="t3_1d0leag-post-rtjson-content").get_text()
    
    # Extract all comments
    code_id = article_url.split("comments/")[-1].split("/")[0]
    all_post = soup.find_all("shreddit-comment")
    print(len(all_post))
    comments_output = []
    
    # Loop through each comment in the post
    for post in all_post:
        try:
            comment = {}
            comment['Comment Url'] = 'https://www.reddit.com' + post.get('permalink')
            comment['Comment Posted Date'] = post.find("faceplate-timeago").find('time').get('title')
            comment['Comment Text'] = post.find("div", attrs={"slot": "comment"}).get_text(strip=True)
            comment['Comment UpVotes'] = post.get('score')
            comment['Comment Author'] = post.find('faceplate-tracker', attrs={'noun': "comment_author"}).text.strip() if post.find('faceplate-tracker', attrs={'noun': "comment_author"}) else None
            comment['Comment Profile Url'] = 'https://www.reddit.com' + post.find('faceplate-tracker', attrs={'noun': "comment_author"}).find('a').get('href') if post.find('faceplate-tracker', attrs={'noun': "comment_author"}) else None
            comments_output.append(comment)
        except Exception as e:
            print(f"An error occurred: {e}")
            continue
        
    driver.quit()
    return post_title, post_desc, comments_output
script=[]
# Generate the script
def generate_script(article_url):
    
    
    post_title,post_desc, comments = fetch_reddit_content(article_url)
    total_steps = len(comments)
    script.append("Narrator Opening: Welcome back to our channel! Today we are diving into Reddit thread!\n")
    script.append(f"Title Card: {post_title.strip()}\n")
    script.append(f"Reading Original Post: {post_desc.strip()}\n\n")
    script.append(f"\n\n")
    script.append(f"Scene Transition :Comments Pop Up\n\n")
    for i, comment in enumerate(comments):
        script.append(f"Comment by {comment['Comment Author']}: {comment['Comment Text']}\n")
        # script.append("Narrator Comment: This user raises an interesting point...\n")
        # progress = ((i + 1) / total_steps * 80) + 20  # Adjusting progress calculation
        # progress_callback(progress)
    script.append("Narrator Closing: That’s all for today's post. Thank you for listening!\n")

    return "\n".join(script)

# Create the script and save to a text file


# Clean up Selenium WebDriver


# fetch_reddit_content('https://www.reddit.com/r/relationship_advice/comments/1d0leag/my_30m_future_mil_57f_keeps_inviting_people_to/')