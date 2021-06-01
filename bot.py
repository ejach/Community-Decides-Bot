import os
import sqlite3

import praw

# Enter your subreddit without the r/
subreddit = ''
# Threshold that a comment crosses to send to modmail
threshold = 1

conn = sqlite3.connect('storage.db')  # connect to the database. if it doesn't exist, automatically create.
c = conn.cursor()
submission_id = []  # these are the local variables where the comment and submission ids are stored.
comment_id = []


def process_submission(submission):
    if submission.id in submission_id:  # if the posts id is already in our database, ignore.
        return None
    else:
        iresponded = submission.reply("Upvote if this submission follows the commmunity guidelines. Downvote "
                                      "if it does not. \n\n\n\n---\n\n^(Beep boop. I am a bot. If there are "
                                      "any issues, contact my) [^Owner ]("
                                      "https://www.reddit.com/message/compose/?to=draco123465&subject=/u/-k"
                                      "-bot)\n\n^(Check out the ) [^GitHub ]("
                                      "https://github.com/ejach/Community-Decides-Bot)")
        iresponded.mod.distinguish(how='yes', sticky='True')  # distinguish the post and sticky it.
        submission_id.append(submission.id)  # add the submission id to our variable
        comment_id.append(iresponded.id)  # add the comment id to our variable
        c.execute("INSERT INTO stuffToPlot (commentID, submissionID) VALUES (?, ?)",
                  # insert the comment and submission id into the database.
                  (iresponded.id, submission.id))
        conn.commit()  # commit the change
        return


def process_commented_submissions():
    if not comment_id:  # if there are no comments, return.
        return
    else:
        for acomment in comment_id:  # for each comment in our array, run the following code
            theobject = reddit.comment(acomment)  # grab the comment object
            if theobject.score < threshold:  # if the score is less than the threshold, run the following code.
                print("A submission has 0 points. Sending message to ModMail.")
                theobject.edit(
                    "**This post has fell below the threshold. The moderators have been notified.** \n\n\n\n---\n\n^("
                    "Beep boop. I am a bot. If there are any issues, contact my) [^Daddy ]("
                    "https://www.reddit.com/message/compose/?to=draco123465&subject=/u/-k-bot)\n\n^(Check out the ) ["
                    "^GitHub ](https://github.com/ejach/Community-Decides-Bot)")  # edit the original comment,
                # informing the user
                parent = theobject.parent()  # grab the submission id, (the parent of the comment.)
                comment_id.remove(theobject)  # remove the id from the local variable
                c.execute("DELETE FROM stuffToPlot WHERE commentID='{}'".format(
                    acomment))  # remove the comment from the database
                conn.commit()
                # grab the submission
                thingtoremove = reddit.submission(id=parent)
                # forwards the URL to the post to the modmail
                reddit.subreddit(subreddit).message('Post violation',
                                                    'The post ' + submission.url + ' has reached '
                                                                                   'below the '
                                                                                   'threshold.')
            else:
                continue
        return


print("Logging into reddit!")
reddit = praw.Reddit('bot1', config_interpolation="basic")
reddit.validate_on_submit = True

print("Logged into reddit!")
c.execute(
    'CREATE TABLE IF NOT EXISTS stuffToPlot(commentID TEXT, submissionID TEXT)')  # create tables if they dont exist
print("Finished database configuration")
print("Now attempting to populate variables with data.")
c.execute("SELECT commentID FROM stuffToPlot")
data = c.fetchall()
for row in data:
    comment_id.append(row[0])  # add the database comment ids to the local variable
print("Finished comment data entry.")
c.execute("SELECT submissionID from stuffToPlot")
moredata = c.fetchall()
for row in moredata:
    submission_id.append(row[0])  # add the submission ids to the local variable
print("Finished submission data entry, ready to go!")

while True:
    for submission in reddit.subreddit(subreddit).new(limit=35):
        process_submission(submission)

    process_commented_submissions()
