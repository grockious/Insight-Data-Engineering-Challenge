# Imported Packages
import json
import re
import os
import time

# Initiating the Timer
start_time=time.time()

# Enter The File Address Here
file_address='tweet_input/tweets.txt'

# Initializations
unicode_counter=0
tweet_count=0
outputfile_temp=[]

# Extracting Tweet Text and Time
for each_line in open(file_address):
    current_tweet_dictionary=json.loads(each_line)
    try:
        current_tweet_text=current_tweet_dictionary['text']
        current_tweet_time=current_tweet_dictionary['created_at']
        tweet_count += 1
        # Removing Non-ASCII Characters
        current_tweet_text_nounicode=current_tweet_text.encode('ascii','ignore')
    
        # Counting Tweets with Unicode Characters
        unicode_counter+=(current_tweet_text_nounicode!=current_tweet_text)
    
        # Removing White-Space Escape Characters
        current_tweet_text_nounicode_nowhitespace=re.sub('\s', ' ',current_tweet_text_nounicode)
        
        # Appending to the Outputfile List
        outputfile_temp.append(current_tweet_text_nounicode_nowhitespace+' (timestamp: '+current_tweet_time+')')
    except:
        outputfile_temp.append('THIS IS NOT A TWEET')
    
# Showing the Number of Unicode Tweets at the End
dash_length=len(str(unicode_counter)+' tweets contained unicode.')
outputfile_temp.append('\n'+'-'*dash_length+'\n'+str(unicode_counter)+' tweets contained unicode.')
outputfile_temp.append('-'*dash_length)

# Writing to the Output file
with open("tweet_output/f1.txt", "w") as outputfile:
    # OS-Dependent Line Seperation
    outputfile.write(os.linesep.join(outputfile_temp))
    
# Final Message
print('All the tweets are collected successfully in "tweet_output/f1.txt" within %s seconds.' %(time.time()-start_time))
    
