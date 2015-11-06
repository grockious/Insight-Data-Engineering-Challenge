# Imported Packages
import json
import scipy as sp
import os
import time

# User-Defined Function(s)
# Function1: Remove the Edges and the Node of the Expired Hashtag 'expired_hashtag' from the graph
def drop_expired_out(graph, expired_hashtag):
    # Finding Other Hashtags Connected to the Expired Hashtag 'expired_hashtag'
    connected_hashtags = graph[expired_hashtag]
    # Removing the Edges of the Expired Hashtag 'expired_hashtag' from the Graph
    for each_hashtag in connected_hashtags:
        graph[each_hashtag].remove(expired_hashtag)
    # Removing the Node of the Expired Hashtag 'expired_hashtag' from the Graph    
    del graph[expired_hashtag]
    return graph

# Initiating the Timer
start_time = time.time()

# Enter The File Address Here
file_address = "tweet_input/tweets.txt"

# Initializations
graph = {}
hashtags_dict = {}
outputfile_temp = []

# Opening the Input File
with open(file_address) as input_file:
    # Reading the Input File Line by Line
    for each_line in input_file:
        current_tweet = json.loads(each_line)
        try:
            # Extracting the Timestamp
            timestamp = int(current_tweet['timestamp_ms'])/1000
        except:
            # Handling the Case of Non-Tweet Line
            outputfile_temp.append("The new line was not a tweet")
            continue
        
        try:
            # Cleaning the Hashtags
            hashtags = sp.unique(['#'+each_hashtag['text'].lower() for each_hashtag in current_tweet['entities']['hashtags']])
            hashtags = [each_hashtag.encode('ascii','ignore') for each_hashtag in hashtags]
            # Creating a Dictionary for the New Hashtags as {'hashtag1':tweet's time stamp,...}
            new_hashtags_dict = dict([(each_hashtag, timestamp) for each_hashtag in hashtags])
        except:
            # The Case That the New Tweet Does Not Have Any Hashtag
            new_hashtags_dict = {}
        
        # Identifying Expired Hashtags
        expired_hashtags = []
        for each_hashtag in hashtags_dict.keys():
            delta_t = timestamp - hashtags_dict.get(each_hashtag, timestamp)
            if delta_t > 60:
                expired_hashtags.append(each_hashtag)
        
        # Removing the Expire Hashtag 'expired_hashtag' from the Hashtags Dictionary 'hashtags_dict' and Graph        
        for each_hashtag in expired_hashtags:
            del hashtags_dict[each_hashtag]
            graph = drop_expired_out(graph, each_hashtag)
        
        # Updating the Hashtag Dictionary 'hashtags_dict'
        hashtags_dict.update(new_hashtags_dict)
        
        # Adding the New Edges and New Nodes to the Graph
        for each_hashtag in new_hashtags_dict.keys():
            graph[each_hashtag] = list(sp.unique(graph.get(each_hashtag,[]) + new_hashtags_dict.keys()))
            graph[each_hashtag].remove(each_hashtag)
        
        # Calculating the Degree of Each Node 
        degrees = [len(graph[each_node]) for each_node in graph.keys()]
        
        # Calculating the Average Degree 
        try:
            avg_degree = str(round(1.0*sum(degrees)/sp.count_nonzero(degrees),2))
        except:
            # The Average Degree Must be Zero in the Case of No Edge
            avg_degree = str(0)
        
        # Appending to the Output List 
        outputfile_temp.append(avg_degree)

# Writing to the Output file
with open("tweet_output/f2.txt", "w") as output_file:
    # OS-Dependent Line Seperation
    output_file.write(os.linesep.join(outputfile_temp))

# Final Message    
print('The calculated graph averages are written successfully in "tweet_output/f2.txt" within %s seconds.' % (time.time() - start_time))