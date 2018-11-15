# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 15:01:42 2018

@author: nyasa
"""

#Stream3
from __future__ import absolute_import, print_function
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

'''This is the basic stream that stores election-related tweets locally.

This runs 1st in our data pipeline:
1- Stream3.py to gather tweets
2- Process3.py to sort them into warehouses
3- prep4ManualClassification.py to process warehouses into csvs of screen names
4- Process3-2.py to check if tweets are bot-like

'''


#Stream tweets
consumer_key=""
consumer_secret=""
access_token=""
access_token_secret=""


class StdOutListener(StreamListener):
    
    def on_data(self, data):

        #Write to warehouse
        with open(wh, "a") as warehouse:     
            warehouse.write(data + '\n')
        return True

    def on_error(self, status): 
        print(status)
        


if __name__ == '__main__':    
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    #Ask for run version
    print('What run of the stream is this?')
    streamV = input('-->')
    
    #Input local address of a text file made specifically for this (warehouse)
    wh = ('C:/Users/nyasa/Documents/Classes/Data Mining/Project/warehouses/warehouse'
          + streamV + '.txt')
    print('Streaming Tweets to warehouse'+ streamV+ '.txt')
    
    
    #Stream tweets
    stream = Stream(auth, l)
    #track general election terms
    t = ['midterm','midterms','election','elections','vote','voting','votes','Vote','ballot','Trump','democracy','Resistance','Blue Wave','BlueWave', 'polls', 'poll']    
    stream.filter(track= t, stall_warnings=True, async=True)

            
 
