import praw
import time
import sqlite3

conn = sqlite3.connect('storage.db') # connect to the database. if it doesn't exist, automatically create.
c = conn.cursor()
submission_id = [] # these are the local variables where the comment and submission ids are stored.
comment_id = []


def process_submission(submission):
        if submission.id in submission_id: # if the posts id is already in our database, ignore.
                return None
        else:
                iresponded = submission.reply("Upvote if this submission is a Useful Red Circle! Downvote if it is Useless.")
                iresponded.mod.distinguish(how='yes', sticky='True') # distinguish the post and sticky it.
                submission_id.append(submission.id) # add the submission id to our variable
                comment_id.append(iresponded.id) # add the comment id to our variable
                c.execute('INSERT INTO stuffToPlot (commentID, submissionID) VALUES (?, ?)', # insert the comment and submission id into the database.
                        (iresponded.id, submission.id))
                conn.commit() # commit the change
                return

def process_commented_submissions():
        if comment_id == []: # if there are no comments, return.
                return
        else:
                for acomment in comment_id: # for each comment in our array, run the following code
                        theobject = reddit.comment(acomment) # grab the comment object
                        if theobject.score < 1: # if the score is less than 1, run the following code.
                                print("A submission has 0 points. Sending message to ModMail.")
                                theobject.edit("**This post has fell below the threshold. The moderators have been notified.**") # edit the original comment, informing the user
                                parent = theobject.parent() # grab the submission id, (the parent of the comment.)
                                comment_id.remove(theobject) # remove the id from the local variable
                                c.execute("DELETE FROM stuffToPlot WHERE commentID='{}'".format(acomment)) # remove the comment from the database
                                conn.commit()
                                thingtoremove = reddit.submission(id=parent) # grab the submission
                                reddit.subreddit('x').message('Post violation', 'The post ' + submission.url + 'has reached below the threshold.')

                        else:
                                continue
                return


print("Logging into reddit!")
reddit = praw.Reddit(user_agent='x',
                                        client_id='x', client_secret='x',
                                        username='x', password='x')


print("Logged into reddit!")
c.execute('CREATE TABLE IF NOT EXISTS stuffToPlot(commentID TEXT, submissionID TEXT)') # create tables if they dont exist
print("Finished database configuration")
print("Now attempting to populate variables with data.")
c.execute("SELECT commentID FROM stuffToPlot")
data =  c.fetchall()
for row in data:
        comment_id.append(row[0])    # add the database comment ids to the local variable
print("Finished comment data entry.")
c.execute("SELECT submissionID from stuffToPlot")
moredata = c.fetchall()
for row in moredata:
        submission_id.append(row[0]) # add the submission ids to the local variable
print("Finished submission data entry, ready to go!")


while True:
        for submission in reddit.subreddit("x").new(limit=35):
                process_submission(submission)


        process_commented_submissions()