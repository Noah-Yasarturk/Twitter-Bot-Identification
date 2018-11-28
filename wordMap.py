# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 04:07:14 2018

@author: nyasa
"""

'''
In this module, I'll generate a wordmap from the suspect bots.
'''

import csv
import tweepy


def main():
    #Auth api
    consumer_key="GVHhMXYiyj1fHExAu3Bbda3i9"
    consumer_secret="j2IP4ocmoqesE9HS9yMey1HROXj6C6MIlnJds2zv2TMacPLVEJ"
    access_token="798242515833016321-xAAnsVIMJU1rP5cEpmVXxwQE0Jhdw0p"
    access_token_secret="DkkwatnPO6sI9JIIhogAAXDNPy34mcZrxtbu3W7EOPDOO"
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    
    #Get screen names that fail 6 tests
    print('Getting screen names...')
    #Read out and store screen names
    nameSet = []
    testsfailed = []
    inPath = 'C:/Users/nyasa/Documents/Classes/Data Mining/Project/Trial 4/tests_Triggered/master.csv'
    with open(inPath, 'r') as csvIn_file:
        csv_reader = csv.reader(csvIn_file, delimiter= ',')
        for row in csv_reader:
            if row[10] != 'Total tests failed:':
                testsfailed.append(row[10])
            if row[0] != 'Screen Name':
                nameSet.append(row[0])
    #Sort out only the Screen Names that fail more than 5 tests
    print('Extracting names that fail more than 5 tests...')
    botish = []
    for i in range(len(nameSet)):
        if int(testsfailed[i]) == 6:
            botish.append(nameSet[i])
    csvIn_file.close()
    
    #botish now has our screen names
    #Now, get 25 last tweets from these 143 users
    bigTwtList = []
    for usr in botish:
        print('Gathering tweets from '+usr)
        try:
            this_twt_list = get_status_lists(usr, 25, api)[0]
            bigTwtList.append(this_twt_list)
        except tweepy.TweepError:
            print('Oh no')
        
    #Write tweets to a text file
    print('Writing to file')
    wordMap_file_path = 'C:/Users/nyasa/Documents/Classes/Data Mining/Project/Report/twtList.txt'
    with open(wordMap_file_path, 'a') as wordFile:
        for twtList in bigTwtList:
            for twt in twtList:
                try:
                    wordFile.write(twt+'\n')
                except:
                    print('Oh no')
    wordFile.close()
    '''
    #Create wordmap from textfile
    print('Creating wordcloud')
    text = open(wordMap_file_path).read()
    # Generate a word cloud image
    wordcloud = WordCloud().generate(text)
    # Display the generated image:
    
    # the matplotlib way:
    import matplotlib.pyplot as plt
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    # lower max_font_size
    wordcloud = WordCloud(max_font_size=40).generate(text)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    image = wordcloud.to_image()
    image.show()'''
    
    
#Get set of tweet texts and times and languages and if it's a headliner
def get_status_lists(sn, n, api):
    tweets_txt = []
    tweets_times = []
    langs_used = []
    hdLnr = 0
    statuses = api.user_timeline(screen_name= sn, count = n, tweet_mode = 'extended')
    for status in statuses:
        tweets_txt.append(status.full_text)
    for times in statuses:
        tweets_times.append(status.created_at)
    for langs in statuses:
        langs_used.append(status.lang)
    '''
    #print('Checking status '+str(hl_cnt))
    if checkHeadliner2(statuses) == True:
        hdLnr = 1'''
        
    twt_list = [tweets_txt, tweets_times, langs_used, hdLnr]   
    return(twt_list)



if __name__ == "__main__":
    main()
