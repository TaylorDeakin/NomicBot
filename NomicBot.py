import time
import praw
import re
import json
import io

r = praw.Reddit('/r/yet_another_nomic monitor v 0.1 by /u/KingAmles'
                'Url: github.com/TaylorDeakin/NomicBot')

r.login(disable_warning=True)

# matches any three numbers in a row, ex 303
pattern = re.compile('([0-9]){3}')

already_done = []  # subreddit we want to browse
subreddit = r.get_subreddit('yet_another_nomic')
proposals_array = []
json_file = io.open('data.json', 'w', encoding='utf-8')

for submission in subreddit.get_hot(limit=10):
    # if we haven't covered the submission already, and it matches at least one of these conditions
    if submission.id not in already_done and ("Proposal" in submission.title or pattern.match(submission.title)):

        op_text = submission.selftext.lower()
        comments = submission.comments
        title = submission.title
        submitter = submission.author.name
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
                seconder = comment.author.name
                ayes.append(comment.author.name)
            # also make sure we're not duplicating entries
            elif "nay" in commentText and comment.author.name not in nays:
                nays.append(comment.author.name)

        proposals_array.append(json.dumps(
            {"title": title, "proposer": submitter, "seconder": seconder, "ayes": ayes, "nays": nays}))

        already_done.append(submission.id)

json_file.write('{ "proposals" : [')

# print this out as valid json
for proposal in proposals_array[:-1]:
    json_file.write(proposal)
    json_file.write(",\n")
# need to do last item separately, as it can't have a comma
else:
    json_file.write(proposals_array[-1])
# close the
json_file.write(']}')
json_file.close()

print("done")
