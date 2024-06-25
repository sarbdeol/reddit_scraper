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
    
    # Load all comments and sub-comments
    submission.comments.replace_more(limit=None)
    
    def process_comment(comment):
        comment_data = {
            'Comment Url': f"https://www.reddit.com{comment.permalink}",
            'Comment Posted Date': comment.created_utc,  # Convert to readable date if needed
            'Comment Text': comment.body,
            'Comment UpVotes': comment.score,
            'Comment Author': comment.author.name if comment.author else None,
            'Comment Profile Url': f"https://www.reddit.com/user/{comment.author.name}" if comment.author else None,
            'Replies': []  # Placeholder for sub-comments
        }
        comments_output.append(comment_data)
        
        # Recursively fetch sub-comments
        for reply in comment.replies:
            process_sub_comment(reply, comment_data['Replies'])
    
    def process_sub_comment(sub_comment, parent_replies):
        sub_comment_data = {
            'Comment Url': f"https://www.reddit.com{sub_comment.permalink}",
            'Comment Posted Date': sub_comment.created_utc,  # Convert to readable date if needed
            'Comment Text': sub_comment.body,
            'Comment UpVotes': sub_comment.score,
            'Comment Author': sub_comment.author.name if sub_comment.author else None,
            'Comment Profile Url': f"https://www.reddit.com/user/{sub_comment.author.name}" if sub_comment.author else None
        }
        parent_replies.append(sub_comment_data)
        
        # Recursively fetch more sub-comments if needed
        for reply in sub_comment.replies:
            process_sub_comment(reply, parent_replies)
    
    # Process top-level comments
    for top_level_comment in submission.comments:
        process_comment(top_level_comment)
    
    return post_title, post_desc, comments_output

def generate_script(article_url):
    post_title, post_desc, comments = fetch_reddit_content(article_url)
    
    script = []
    script.append("Narrator Opening: Welcome back to our channel! Today we are diving into a Reddit thread!\n")
    script.append(f"Narrator Intro: {post_title.strip()}\n{post_desc.strip()}")
    # script.append(f"Reading Original Post: {post_desc.strip()}\n\n")
    script.append("Scene Transition: Comments Pop Up\n\n")
    
    for comment in comments:
        script.append(f"{comment['Comment Author']}: {comment['Comment Text']}\n")
        
        for sub_comment in comment['Replies']:
            script.append(f">> {sub_comment['Comment Author']}: {sub_comment['Comment Text']}\n")
    
    script.append("Narrator Closing: That’s all for today's post. Thank you for listening!\n")
    
    return "\n".join(script)

# # Example usage:
# article_url = 'https://www.reddit.com/r/worldnews/comments/abc123/title_of_post/'
# script = generate_script(article_url)
# print(script)
