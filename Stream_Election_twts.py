# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 15:01:42 2018

@author: nyasa
"""

#Stream
from __future__ import absolute_import, print_function
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import os

'''This is the basic stream that stores election-related tweets locally.
    To get it to run, edit line 56 to input the local path where you'd like this stored.
    Also, edit line 43 to give the max file size of a warehouse (100 mb by default).

This runs 1st in our data pipeline:
1- Stream3.py to gather tweets based on election-related terms
2- Preprocess_Twts.py that tests the scraped tweets to see which among 7 tests hey trigger
3- check_Twts that checks tweets that trigger n tests of the 7 to see if they fail tests confirming
they are botlike.
'''


#Stream tweets
consumer_key="GVHhMXYiyj1fHExAu3Bbda3i9"
consumer_secret="j2IP4ocmoqesE9HS9yMey1HROXj6C6MIlnJds2zv2TMacPLVEJ"
access_token="798242515833016321-xAAnsVIMJU1rP5cEpmVXxwQE0Jhdw0p"
access_token_secret="DkkwatnPO6sI9JIIhogAAXDNPy34mcZrxtbu3W7EOPDOO"


class StdOutListener(StreamListener):
    
    def on_data(self, data):

        #Write to warehouse
        with open(wh, "a") as warehouse:     
            warehouse.write(data + '\n')
            fileinfo = os.stat(wh)
            #Check that warehouse file size is less than 5 mb
            max_file_size = 100000000
            if (fileinfo.st_size > max_file_size):
                print('Max warehouse file size exceeded.')
                print('Run again on a new warehouse number to make for speedier processing.')
                return False
        
        return True

    def on_error(self, status): 
        print(status)
        


if __name__ == '__main__':    
    listener = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    #Ask for run version
    print('What run of the stream is this?')
    streamV = input('-->')
    
    #Input local address of a text file made specifically for this (warehouse)
    folder_path = 'C:/Users/nyasa/Documents/Classes/Data Mining/Project/warehouses/'
    wh = (folder_path + 'warehouse' + streamV + '.txt')
    print('Streaming Tweets to warehouse'+ streamV+ '.txt')
    
    
    #Stream tweets
    stream = Stream(auth, listener)
    #track general election terms
    t = ['midterm','midterms','election','elections','vote','voting','votes','Vote','ballot','Trump','democracy','Resistance','Blue Wave','BlueWave', 'polls', 'poll']    
    stream.filter(track= t, stall_warnings=True, async=True)

            
 