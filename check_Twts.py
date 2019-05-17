# -*- coding: utf-8 -*-
"""
@author: nyasa
"""

import tweepy
from difflib import SequenceMatcher
import time
import csv
from newspaper import Article
from datetime import datetime


'''
check_Twts.py
In this method we'll check tweet activity in 4 ways:
    1)check to see if an account tweeted the same thing out in the last n tweets
    2)check to see if an account is tweeting mostly a repost
    3)check to see if an account tweets out in 3 or more languages
    4)check to see if an account is tweeting articles with the article title as the tweet comment.

TO RUN: edit line #46 to input folder path for your project. Additionally, default min test check 
for number of tests an account triggered for us to process here is on line #64. Default is 6.
    
This runs 3rd in our data pipeline:
1- Stream3.py to gather tweets based on election-related terms
2- Preprocess_Twts.py that tests the scraped tweets to see which among 8 tests hey trigger
3- check_Twts that checks tweets that trigger n tests of the 8 to see if they fail tests confirming
they are botlike.
    
'''


def main():
    #Auth api
    consumer_key=""
    consumer_secret=""
    access_token=""
    access_token_secret=""
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
     
    #Project folder path
    folder_path = 'C:/Users/nyasa/Documents/Classes/Data Mining/Project/warehouses/'

    #Start Procesing
    print('Getting screen names...')
    #Read out and store screen names
    nameSet = []
    testsfailed = []
    inPath = (folder_path + 'master.csv')
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
    min_tests = 6
    for i in range(len(nameSet)):
        if int(testsfailed[i]) == min_tests:
            botish.append(nameSet[i])
            
    botish = Remove(botish)
    ##print(len(botish)) should be 3314
    csvIn_file.close()
    
    print('Checking to see if they fail botlike tests.')
    #Check calls left
    print('Calls left to start with:')
    getLeft(api)
    #Check if first 15 are botlike
    #Write csv recording botlike tests failed
    pathOut = (folder_path + 'botlike.csv')
    with open(pathOut, 'a', newline='') as csvOut_file:
        csv_writer = csv.writer(csvOut_file, delimiter = ',')
        csv_writer.writerow(['Screen Name','Full Reposts (last 200 Twts)','Mostly Reposts','3+ Langs Used','Article Headline Tweeter','Failed a Test?'])
        for j in range(len(botish)):
            ##Screen name, full repost, Mostly repost, 3++Langs used
            botTests = ['', 0, 0, 0, 0, 0]
            thisSN = botish[(j)] ##Due to stopping at row 121
            print('')
            print('->Checking '+thisSN)
            botTests[0] = thisSN
            try:
                theseTwts = get_status_lists(thisSN, 100, api)
                #Check if they have any reposts
                if reposts(theseTwts[0]) == True:
                    botTests[1] = 1
                    botTests[5] = 1
                #Check if there is a majority repost
                if majority_repost(theseTwts[0]) == True:
                    botTests[2] = 1
                    botTests[5] = 1
                #Check if the user uses more than 2 languages
                langS = set(theseTwts[2])
                if  len(langS)> 2:
                    botTests[3] = 1
                    botTests[5] = 1
                #Check if accnt is a headline retweeter
                if theseTwts[3] == 1:
                    botTests[4] = 1
                    botTests[5] = 1
                
            except tweepy.TweepError:
                botTests[1] = 'Account Deleted'
                print('This account appears to be deleted.')
            
            #Check calls left
            getLeft(api)
    
            #Write to csv
            csv_writer.writerow(botTests)
        
        
        
    #Close csv files 
    csvOut_file.close()

#Methods
def Remove(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list
    
def assessRegularity(date_list):
    check = False
    #We have a list of datetime objects e.g. 'Thu Jul 28 00:08:39 +0000 2016'
    ##We want to handle type conversion and exclude seconds
    
    diffList = []
   
    now1 = datetime.now()
    curDiff = now1 - date_list[0]
    for i in range(len(date_list)):
        if i < len(date_list):
            curDiff = (date_list[i] - date_list[i+1])
            diffList.append(curDiff)
    diffSet = set(diffList)
    if len(diffSet) != len(diffList):
        #We have a copy difference
        check = True
    return(check)
    
#Check if tweet contains a link and tweets the article headline as the text
def checkHeadliner2(statuses_obj):
    check = False
    isEmpty = False
    failedDnLd = False
    aURL = ''
    twt_txt = ''
    hdLn = ''
    #Check if a given status has a URL
    for i in range(len(statuses_obj)):
        if not statuses_obj[i].entities['urls']:
            #If there is no URL
            isEmpty = True
        else:
            #If there is a URL, retrieve it
            aURL = statuses_obj[i].entities['urls'][0]['url']
            #Get article headline
            article = Article(aURL)
            article.download()
            try:
                article.parse()
                hdLn = article.title
            except:
                failedDnLd = True
            
            #Retrieve tweet text
            twt_txt = statuses_obj[i].full_text
            #Compare retrieved headline to tweet text
            if hdLn != '':
                twt_list = twt_txt.split()
                hdLn_list = hdLn.split()
                simCnt = 0
                l1 = len(twt_list)
                l2 = len(hdLn_list)
                least = l1
                if l1>l2:
                    least = l2
                if l1<l2:
                    least = l1
                for i in range(least):
                    if twt_list[i] == hdLn_list[i]:
                        simCnt+=1
                #Check if 5 or more words between the two are the same
                if simCnt > 4:
                    check = True
                
    return(check)
    


#Check calls left
def getOldestID(sn, api):
    return(0)
    
def getLeft(api):
    #Check calls left
    limits = api.rate_limit_status()
    usertimeline_remain = limits['resources']['statuses']['/statuses/user_timeline']['remaining']
    usertimeline_limit = limits['resources']['statuses']['/statuses/user_timeline']['limit']
    usertimeline_time = limits['resources']['statuses']['/statuses/user_timeline']['reset']
    usertimeline_time_local = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(usertimeline_time))
    print('Twitter API: remain: %s / limit: %s - reseting at: %s' %(usertimeline_remain, usertimeline_limit, usertimeline_time_local))



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
        
    #print('Checking status '+str(hl_cnt))
    if checkHeadliner2(statuses) == True:
        hdLnr = 1
        
    twt_list = [tweets_txt, tweets_times, langs_used, hdLnr]   
    return(twt_list)

#Method to remove reply and retweet from tweet main text
    ##These are either formatted 'RT @screen_name:' or '@screen_name'
def cleanTwts(twt_list):
    for twt in twt_list:
        

        return(0)

#Method to check if pure reposts
def reposts(twt_list):
    #Check if there are duplicates by cloning to a set, which removes duplicates
    twt_set = set(twt_list)
    check = False
    if len(twt_set) != len(twt_list):
        check = True
    return(check)

#Method to check if majority reposts    
def majority_repost(twt_list):
    #Check if the the tweet list contains tweets with 75% similarity
    check = False
    threshold = 0.75
    for twt1 in twt_list:
        for twt2 in twt_list:
            if twt1 != twt2:
                similarity = SequenceMatcher(None, twt1, twt2).ratio()
                if similarity > threshold:
                    check = True
    return(check)

if __name__ == "__main__":
    main()
