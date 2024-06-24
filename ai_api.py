import praw

# Initialize PRAW with your credentials
reddit = praw.Reddit(client_id='nyhrOjCaHtroAd2rEJm8LA',
                     client_secret='lw7NvmPDjGKCbymHrXOvElnhJDK5SA',
                     user_agent='Leading_Internal_337')

def fetch_reddit_content(article_url):
    submission_id = article_url.split("comments/")[-1].split("/")[0]
    submission = reddit.submission(id=submission_id)
    
    post_title = submission.title
    post_desc = submission.selftext
    
    comments_output = []
    submission.comments.replace_more(limit=None)  # Load all comments
    
    for comment in submission.comments.list():
        comment_data = {
            'Comment Url': f"https://www.reddit.com{comment.permalink}",
            'Comment Posted Date': comment.created_utc,  # Convert to readable date if needed
            'Comment Text': comment.body,
            'Comment UpVotes': comment.score,
            'Comment Author': comment.author.name if comment.author else None,
            'Comment Profile Url': f"https://www.reddit.com/user/{comment.author.name}" if comment.author else None
        }
        comments_output.append(comment_data)
    
    return post_title, post_desc, comments_output

def generate_script(article_url):
    post_title, post_desc, comments = fetch_reddit_content(article_url)
    
    script = []
    script.append("Narrator Opening: Welcome back to our channel! Today we are diving into a Reddit thread!\n")
    script.append(f"Title Card: {post_title.strip()}\n")
    script.append(f"Reading Original Post: {post_desc.strip()}\n\n")
    script.append("Scene Transition: Comments Pop Up\n\n")
    
    for comment in comments:
        script.append(f"Comment by {comment['Comment Author']}: {comment['Comment Text']}\n")
    
    script.append("Narrator Closing: That’s all for today's post. Thank you for listening!\n")
    
    return "\n".join(script)


