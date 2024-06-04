import praw
import re

# reads details of reddit comments and returns the following:
"""
    1. comment title
    2. comment text
"""

reddit = praw.Reddit(
    client_id="oOw4fow-1_tGus112XSmEA",
    client_secret="GJG26tAGnhF-8puopRKANTIpaplOrg",
    user_agent="semiautomaticbrainrot"
)

logfile = '../logs/reddit_log.txt'

# using PRAW to scrape post data
class RedditComment:

    # initialise the class with praw
    def __init__(self, url):
        self.comment = reddit.comment(url=url)
        self.author = self.comment.author
        self.post = self.comment.submission.title
        self.cleanupBody()
        self.cleanupTitle()
    
    def getCommentBody(self):
        return self.comment.body
    
    def __str__(self):
        return f"{self.post},...,{self.comment.body}"
    
    # my shitty implementation of a censoring system, also helps avoid the AI reading out mistyped symbols
    def cleanupBody(self):
        self.comment.body = re.sub('[^A-Za-z0-9 ,.]+', '', self.comment.body)       # replace punctuation and other symbols
        self.comment.body = self.comment.body.replace('\n', '. ')
        self.comment.body = self.comment.body.replace('shit', 'slop')
        self.comment.body = self.comment.body.replace('fuck', 'futt')
        self.comment.body = self.comment.body.replace('bitch', 'female dog')
        self.comment.body = self.comment.body.replace('cunt', 'futter')
        self.comment.body = self.comment.body.replace('sex', 'naked time')
        self.comment.body = self.comment.body.replace('kill', 'unalive')
        self.comment.body = self.comment.body.replace('dead', 'gone')
        self.comment.body = self.comment.body.replace('.', '. ')

    # same thing but on the title. I tried to do this in one function, just couldn't get it to work for some reason.
    def cleanupTitle(self):
        self.post = re.sub('[^A-Za-z0-9 ,.]+', '', self.post)       # replace punctuation and other symbols
        self.post = self.post.replace('\n', '. ')
        self.post = self.post.replace('shit', 'slop')
        self.post = self.post.replace('fuck', 'futt')
        self.post = self.post.replace('bitch', 'female dog')
        self.post = self.post.replace('cunt', 'futter')
        self.post = self.post.replace('sex', 'naked time')
        self.post = self.post.replace('kill', 'unalive')
        self.post = self.post.replace('dead', 'gone')
        self.post = self.post.replace('.', '. ')
    
    # writes the comment body to a log file for debugging reasons
    def writeToFile(self):
        with open(logfile, '+w') as fp:
            fp.write(self.getCommentBody())
            print(self.getCommentBody())
            print("successfully wrote comment body to "  + logfile)

def _debug(url):
    comment = RedditComment(url)
    print(str(comment))
    comment.cleanupBody()
    comment.writeToFile()

# _debug("https://www.reddit.com/r/AskReddit/comments/1bl1zbs/comment/kw32hkq/")