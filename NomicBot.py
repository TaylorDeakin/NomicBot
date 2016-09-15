import time
import praw
import re

r = praw.Reddit('/r/yet_another_nomic monitor by /u/KingAmles v 0.1'
                'Url: github.com/TaylorDeakin')

r.login()

# matches any three numbers in a row, ex 303
pattern = re.compile('([0-9]){3}')

already_done = []

while True:
    subreddit = r.get_subreddit('yet_another_nomic')
    for submission in subreddit.get_hot(limit=10):
        # if we haven't covered the submission already, and it matches at least one of these conditions
        if submission.id not in already_done and ("Proposal" in submission.title or pattern.match(submission.title)):

            op_text = submission.selftext.lower()

            print(submission.title)
            comments = submission.comments

            seconder = ""
            ayes = []
            nays = []
            flat_comments = praw.helpers.flatten_tree(comments)

            # loop through the comments
            for comment in flat_comments:
                # accounting for discrepancies in caps by lowering text
                commentText = comment.body.lower()
                # make sure we're not duplicating entries
                if "aye" in commentText and comment.author.name not in ayes:
                    ayes.append(comment.author.name)
                # make sure there isn't already a seconder
                elif "seconded" in commentText and not seconder:
                    seconder = comment.author
                    ayes.append(comment.author.name)
                # also make sure we're not duplicating entries
                elif "nay" in commentText and comment.author.name not in nays:
                    nays.append(comment.author.name)
            # print stuff
            print(seconder)
            print(nays)
            print(ayes)

            already_done.append(submission.id)
