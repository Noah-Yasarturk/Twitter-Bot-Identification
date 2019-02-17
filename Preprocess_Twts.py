# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 11:17:45 2018

@author: nyasa
"""

#import tweepy
import csv
from datetime import date
import datetime


'''
Preprocess_Twts.py.
It will take as input the warehouse to process and then create csv files, one for each test 
to be triggered. Those csvs will then be processed to a master csv which records all tests a 
screen name triggers as well as a total.

The master csv will then be processed, greatest number of tests failed first, filling out 
another csv which records if those screen names fail twt processing methods. 

TO RUN: edit your folder path into line #45 and be ready to input the tweet warehouse file you're working.

This runs 2nd in our data pipeline:
1- Stream3.py to gather tweets based on election-related terms
2- Preprocess_Twts.py that tests the scraped tweets to see which among 8 tests hey trigger
3- check_Twts that checks tweets that trigger n tests of the 8 to see if they fail tests confirming
they are botlike.
'''

def main():
    print('Which warehouse would you like to process?')
    print('Please input the associated number.')
    #Create a list of the tweets

    tweetList = []
    #Record today's date in 2 formats
    todayMDY = datetime.datetime.today().strftime('%m-%d-%y')

    #Accept user input    
    run = input('-->')
    runS = str(run)
    #Location for project
    folder_path = 'C:/Users/nyasa/Documents/Classes/Data Mining/Project/warehouses/'
    wh = (folder_path + 'warehouse' +runS+'.txt')
    print('Beginning processing of warehouse' +runS+'.txt')
    print('Counting tweets ...')
    #Open this warehouse and write all tweets to tweetList
    with open(wh) as f:
        for line in f:
            if '\"retweeted_status\":' in line:
                tweetList.append(line)
    f.close()
    print('The number of tweets in warehouse' +runS+ '.txt currently is '+str(len(tweetList))+'.')

    #Iterate through tweetList, adding each tweet to the appropriate tests_Triggerred csv file
    print('Writing to csvs')
    preproc_csv_path = folder_path
    
    #No Location
    csvPath1 = (preproc_csv_path + 'noLoc.csv')
    #No Bio
    csvPath2 = (preproc_csv_path + 'noBio.csv')
    #Default Profile Pic
    csvPath3 = (preproc_csv_path+ 'defPic.csv')
    #High favorites to followers
    csvPath4 = (preproc_csv_path + 'hiFav2Folw.csv')
    #High tweets to followers
    csvPath5 = (preproc_csv_path + 'hiTwt2Folwr.csv')
    #At following threshold for today
    csvPath6 = (preproc_csv_path + 'folwThreshToday.csv')
    #At overall follower threshold
    csvPath7 = (preproc_csv_path + 'overallThresh.csv')
    #Username not in screen name
    csvPath8 = (preproc_csv_path + 'un_NotIn_sn.csv')
    #Young account
    csvPath9 = (preproc_csv_path + 'yungAccnt.csv')
    
    #Master csv
    csvPathM = (preproc_csv_path + 'master.csv')
    
    #Iterate through tweetList and sort to nameLists to be put into csvs
    nL1 = []
    nL2 = []
    nL3 = []
    nL4 = []
    nL5 = []
    nL6 = []
    nL7 = []
    nL8 = []
    nL9 = []
    
    #List of all screen names
    nLS = []
    
    for twt in tweetList:
        # No location
        if hasLoc(twt) == False:
            nL1.append(getScreenName(twt))
        #No Bio
        if hasBio(twt) == False:
            nL2.append(getScreenName(twt))
        #Default profile pic
        if isPicDefault(twt) == True:
            nL3.append(getScreenName(twt))
        #HiFav to Folwr
        favCnt = getFavs(twt)
        flwrCnt = getFlwrs(twt)
        if hasHiFavLoFolw(favCnt, flwrCnt) == True:
            nL4.append(getScreenName(twt))
        #HiTwt to Folwr
        twtCnt = getTwtCnt(twt)
        if HiTwtLoFlwr(twtCnt, flwrCnt) == True:
            nL5.append(getScreenName(twt))
        #At following thresh (1000) today
        flwCnt = getFlws(twt)
        if dlyFlwLmt(flwCnt) == True:
            nL6.append(getScreenName(twt))
        #At overall follower thresh
        if atThreshold(flwCnt, flwrCnt) == True:
            nL7.append(getScreenName(twt))
        #UN not in SN
        screenName = getScreenName(twt)
        userName = getUserName(twt)
        if UNinScreenName(screenName, userName) == True:
            nL8.append(getScreenName(twt))
        '''
        The below lines are BUGGED as accntYung (d8compare internal method) is bugged
        
        #Young account
        if accntYung(twt, todayMDY) == True:
            nL9.append(getScreenName(twt))'''
        #Write twt to list of all tweets
        nLS.append(getScreenName(twt))
        
    
    #Delete list duplicates
    nL1 = Remove(nL1)
    nL2 = Remove(nL2)
    nL3 = Remove(nL3)
    nL4 = Remove(nL4)
    nL5 = Remove(nL5)
    nL6 = Remove(nL6)
    nL7 = Remove(nL7)
    nL8 = Remove(nL8)
    nL9 = Remove(nL9)
    nLS = Remove(nLS)

    #List of lists
    nLL = [nL1,nL2,nL3,nL4,nL5,nL6,nL7,nL8,nL9]
    
       
    #Write list names to csv files
    with open(csvPath1, 'a', newline='') as csv_file1:
        csv_writer1 = csv.writer(csv_file1, delimiter = ',')
        csv_writer1.writerow(['Total names from warehouse '+ runS + ' with no location: '+str(len(nL1))])
        for n in nL1:
            csv_writer1.writerow([n])
    with open(csvPath2, 'a', newline='') as csv_file2:
        csv_writer2 = csv.writer(csv_file2, delimiter = ',')
        csv_writer2.writerow(['Total names from warehouse '+ runS + ' with no bio: '+str(len(nL2))])
        for n in nL2:
            csv_writer2.writerow([n])
    with open(csvPath3, 'a', newline='') as csv_file3:
        csv_writer3 = csv.writer(csv_file3, delimiter = ',')
        csv_writer3.writerow(['Total names from warehouse '+ runS + ' with default profile pic: '+str(len(nL3))])
        for n in nL3:
            csv_writer3.writerow([n])
    with open(csvPath4, 'a', newline='') as csv_file4:
        csv_writer4 = csv.writer(csv_file4, delimiter = ',')
        csv_writer4.writerow(['Total names from warehouse '+ runS + ' with HiFav to Folwr: '+str(len(nL4))])
        for n in nL4:
            csv_writer4.writerow([n])
    with open(csvPath5, 'a', newline='') as csv_file5:
        csv_writer5 = csv.writer(csv_file5, delimiter = ',')
        csv_writer5.writerow(['Total names from warehouse '+ runS + ' with HiTwt to Folwr: '+str(len(nL5))])
        for n in nL5:
            csv_writer5.writerow([n])
    with open(csvPath6, 'a', newline='') as csv_file6:
        csv_writer6 = csv.writer(csv_file6, delimiter = ',')
        csv_writer6.writerow(['Total names from warehouse '+ runS + ' at following threshold today: '+str(len(nL6))])
        for n in nL6:
            csv_writer6.writerow([n])
    with open(csvPath7, 'a', newline='') as csv_file7:
        csv_writer7 = csv.writer(csv_file7, delimiter = ',')
        csv_writer7.writerow(['Total names from warehouse '+ runS + ' at follower overall threshold: '+str(len(nL7))])
        for n in nL7:
            csv_writer7.writerow([n])
    with open(csvPath8, 'a', newline='') as csv_file8:
        csv_writer8 = csv.writer(csv_file8, delimiter = ',')
        csv_writer8.writerow(['Total names from warehouse '+ runS + ' with UN not in SN: '+str(len(nL8))])
        for n in nL8:
            csv_writer8.writerow([n])
    with open(csvPath9, 'a', newline='') as csv_file9:
        csv_writer9 = csv.writer(csv_file9, delimiter = ',')
        for n in nL9:
            csv_writer9.writerow([n])
    
    #Master csv
    print('Writing to master csv')
    with open(csvPathM, 'a', newline='') as csv_fileM:
        csv_writerM = csv.writer(csv_fileM, delimiter = ',')
        for nm in nLS:
            csv_writerM.writerow(masterRow(nm, nLL))
    
    
    
    #Close csv files
    csv_file1.close()
    csv_file2.close()
    csv_file3.close()
    csv_file4.close()
    csv_file5.close()
    csv_file6.close()
    csv_file7.close()
    csv_file8.close()
    csv_file9.close()
    csv_fileM.close()
    print('Done.')
    
#Processing methods
def Remove(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list
    
def masterRow(sn, lists):
    #Returns a list of truth values to be written as a row 
    #sn is screen name
    tot = 0
    thisRow = [0,0,0,0,0,0,0,0,0, tot]
    if sn in lists[0]:
        thisRow[0] = 1
        tot +=1
    if sn in lists[1]:
        thisRow[1] = 1 
        tot+=1
    if sn in lists[2]:
        thisRow[2] = 1
        tot+=1
    if sn in lists[3]:
        thisRow[3] = 1
        tot+=1
    if sn in lists[4]:
        thisRow[4] = 1
        tot+=1
    if sn in lists[5]:
        thisRow[5] = 1
        tot+=1
    if sn in lists[6]:
        thisRow[6] = 1
        tot+=1
    if sn in lists[7]:
        thisRow[7] = 1
        tot+=1
    if sn in lists[8]:
        thisRow[8] = 1
        tot+=1    
    thisRow = [sn, str(thisRow[0]),str(thisRow[1]),str(thisRow[2]),str(thisRow[3]),str(thisRow[4]),str(thisRow[5]),str(thisRow[6]),str(thisRow[7]),str(thisRow[8]),str(tot)]   
    return(thisRow)
    
#Getters and Setters
def getScreenName(tweet):
    '''This method returns the screen name contained between '","screen_name":"'
    and '","location"' .
    '''
    screenName = ''
    scrnFront = '\",\"screen_name\":\"'
    scrnBack = '\",\"location\"'
    scrnBehind = '\"name\":"'
    scrnSplit1 = tweet.split(scrnBehind,1)
    #scrnSplit1[1] is now '"(username)", "screen_name":...'
    scrnSplit2 = scrnSplit1[1].split(scrnBack,1)
    #scrnSplit2[0] is now "(username)", "screen_name":,"(screenName)"'
    scrnSplit3 = scrnSplit2[0].split(scrnFront,1)
    screenName = scrnSplit3[1]
    return(screenName)
    
    
def getUserName(tweet):
    '''This method returns the user name contained between '"name":"'
    and '","screen_name":' . 
    '''
    un = ''
    unFront = '\",\"screen_name\":\",\"'
    unBack = '\",\"location\"'
    unBehind = '\"name\":"'
    unSplit1 = tweet.split(unBehind,1)
    #scrnSplit1[1] is now '"(username)", "screen_name":...'
    unSplit2 = unSplit1[1].split(unBack,1)
    #scrnSplit2[0] is now "(username)", "screen_name":,"(screenName)"'
    unSplit3 = unSplit2[0].split(unFront,1)
    #scrnSplit3[1] is now '(screenName)"'
    unSplit4 = unSplit3[0].split('\"',1)
    un = unSplit4[0]
    return(un)
    
    
def getDateTwtd(tweet):
    '''This method gets the tweet date from the tweet as a list.
    The list currently looks like: [Month as number, day]
    Date of the tweet/retweet is after '{"created_at":"(date string)' and before
        ' +0000 2018","id":'. 
        
        This needs to return the day it was tweeted.
    '''
    dateSplit1 = tweet.split('{\"created_at\":',1)
    #dateSplit is now comprised of an empty string and then the start of the date
    #Trim off the behind end
    dateBack = (' +0000 2018\",\"id\":')
    dateSplit2 = dateSplit1[1].split(dateBack,1)
    '''dateSplit2 is now comprised of the date as '(Weekday 3-letter) (Month 3-letter) (MonthDay) (Time as hour:minute:second)'
    and then next index as rest of tweet'''
    dateFull = dateSplit2[0]
    dateFull = dateFull.replace('\"',"")
    #Isolate Month as number and Monthday from dateFull
    ## Example dateFull: 'Thu Oct 25 03:37:17'
    ## Format front chop - this is based on a presiction, not any actual insight
    wkDays = ['Mon','Tues','Wed','Thu','Fri','Sat','Sun']
    dateLessFull = []
    for day in range(len(wkDays)):
        if wkDays[day] in dateFull:
            dateLessFull = dateFull.split((wkDays[day]+' '),1)
    #dateLessFull now starts with the info we want
    ## Isolate Month - again, the format of the month string is unknown to me rn
    mnths = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun','July','Aug','Sept','Oct','Nov','Dec']
    getMonth = 0
    dateLessFull2 = []
    for month in mnths:
        if month in dateLessFull[1]:
            getMonth = str(mnths.index(month)+1)
            dateLessFull2 = dateLessFull[1].split((month+' '), 1)
    #We have the month correctly stoored into getMonth; getDay now
    days = list(range(1,32))
    getDay = 0
    for day in days:
        i = days.index(day)
        
        #add the 0 to single digit numbers
        if i<9:
            days[i] = ('0'+str(day) )
        #Convert rest to string
        days[i] = str(days[i])
        
        #Check to see if the first value of dateLessFull2[1] contains a days
        if days[i] in dateLessFull2[1]:
            getDay = days[i]
            break
        
    #We have the day ccorrectly stored into getDay
    dateS = (str(getMonth)+'-'+str(getDay))
    return(dateS)

    
def getTwtCnt(tweet):
    try:
       twtCnt = 0
       '''Number of tweets is denoted by "statuses_count": , which is in between
       "favourites_count":(int) and "created_at":
        '''
       tcFront = '\"statuses_count\":'
       tcBack = ',\"created_at\":'
       tcBehind = '\"favourites_count\":'
       tcSplit1 = tweet.split(tcBehind,1)
       tcSplit2 = tcSplit1[1].split(tcBack,1)
       tcSplit3 = tcSplit2[0].split(tcFront,1)
       twtCnt = int(tcSplit3[1])
       return twtCnt
    except IndexError:
        return(0)
    
def getFlwrs(tweet):
    try:
        flwrCnt = 0
        #Find follower count similarly
        flwrFront = '\"followers_count\":'
        flwrBack = ',\"friends_count\"'
        flwrBehind = '\"verified\":'
        flwrSplit1 = tweet.split(flwrBehind,1)
        flwrSplit2 = flwrSplit1[1].split(flwrBack,1)
        flwrSplit3 = flwrSplit2[0].split(flwrFront,1)
        flwrCnt = int(flwrSplit3[1])
        return(flwrCnt)
        
    except IndexError:
        return(0)
    
   
    
def getFavs(tweet):
    try:
        favCnt = 0
         #Locate the favorites count
        ##It's always directly in between favFront and favBack
        favFront = '\"favourites_count\":'
        favBack = ',\"statuses_count\"'
        ##Split data
        favBehind = '\"listed_count\":'
        favSplit1 = tweet.split(favBehind,1)
        ###Data now split where '(a # and a comma) "favourites_count":(cnt) is the
        ###start of favSplit1[1].
        favSplit2 = favSplit1[1].split(favBack,1)
        ###Data now split where "favourites_count":(cnt) is favSplit2[0]
        favSplit3 = favSplit2[0].split(favFront,1)
        favCnt = int(favSplit3[1])
        
        return(favCnt)
    
    except IndexError:
        return(0)
   
     
def getFlws(tweet):
    try:
        flwCnt = 0
        #Locate the follow count
        ##It's always directly in between flwFront and flwBack
        flwFront = ',\"friends_count\":'
        flwBack = ',\"listed_count\":'
        ##Split data
        flwBehind = '\"followers_count\":'
        flwSplit1 = tweet.split(flwBehind,1)
        ###Data now split where '(a # and a comma) "favourites_count":(cnt) is the
        ###start of favSplit1[1].
        flwSplit2 = flwSplit1[1].split(flwBack,1)
        ###Data now split where "favourites_count":(cnt) is favSplit2[0]
        flwSplit3 = flwSplit2[0].split(flwFront,1)
        flwCnt = int(flwSplit3[1])
        return(flwCnt)
    
    except IndexError:
        return(0)

#Profile Info methods
def accntYung(tweet, today):
    '''
    This method returns true if the account that made the tweet is less than
    30 days old. The parameter 'today' must follow the following format:
    '%m-%d-%y' , or for example '11-05-18'
    '''
    yung = False
    #Get date account was created
    dateRaw = getAccntCreateDate(tweet)
    ##Date should now take the form similar to the following:
    ##'Fri Jun 10 07:09:42 +0000 2016'
    
    # Store remainding dateRaw into list
    dateList = dateRaw.split()
    ##The values in question are now in dateList[1]-Month, 
    ##dateList[2]-Monthday,dateList[5]-Year
    #Convert date into the appropriate format
    month = ''
    monthDay = dateList[2]
    year = dateList[5]
    mnths = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun','July','Aug','Sept','Oct','Nov','Dec']
    for i in range(12):
        if mnths[i] == dateList[1]:
            month = i
    dateFormatted = (str(month) + '-' + str(monthDay) + '-' + str(year))
    #Compare to today's date ; are there 30 days or less between today's
    #date and the account creation date?
    diff = d8Compare(dateFormatted,today)
    if diff >= 30:
        yung = True
    
    return(yung)

def d8Compare(date1, date2):
    '''Accepts 2 strings as dates in the format '%m-%d-%y' , or for example 
    '11-05-18', and returns how many days are between the two;
    
    BUGGED - (ValueError: day is out of range for month)
    '''
    d1split = date1.split('-',2)
    d2split = date2.split('-',2)
    print(d1split)
    #Format year
    y1 = d1split[2].replace("\"", "")
    y2 = d2split[2].replace("\"", "")
   
    #date method accepts as parameters year, month, day
    ##Handle leap year
    if (d1split[1]==29 and d1split[0]==2 and y1%4!=0):
        d1split[1] = 28
    if (d2split[1]==29 and d2split[0]==2 and y2%4!=0):
        d2split[1] = 28
        
    d1 = date(int(y1), int(d1split[0]), int(d1split[1]))
    d2 = date(int(y2), int(d2split[0]), int(d2split[1]))
    delta = d2 - d1
    if (delta.days<0):
        delta = delta * -1
    return(delta.days)

def getAccntCreateDate(tweet):
    #Get date account was created
    ##Accnt creation date follows "created_at": after the user object (and 
    ##therefore after the first "created_at":).
    ##The prior attribute is "statuses_count": and the following one is 
    ##"utc_offset".
    # Split apart at "in_reply_to_screen_name":
    dateRaw = ''
    yungHalf = ',\"user\":{'
    yungSplit0 = tweet.split(yungHalf, 1)
    ##yungSplit0[1] is now the latter half of the tweet, excluding the first
    ##"created_at":
    yungFront = '\"created_at\":'
    yungBack = ',\"utc_offset\":'
    yungBehind = '\"statuses_count\":'
    yungSplit1 = yungSplit0[1].split(yungBehind,1)
    yungSplit2 = yungSplit1[1].split(yungBack,1)
    yungSplit3 = yungSplit2[0].split(yungFront,1)
    dateRaw = yungSplit3[1]
    return(dateRaw)

        
        
def UNinScreenName(screenName, userName):
    '''This tests to see if any combination/case of the username (longer) is found
    within the screen name (the @name).
    '''
    UNhasScreenName = False
    
    #Split up username by spaces
    unSpaceSplit = userName.split()
    #Check to see if any of the words are in the screen name
    l = len(unSpaceSplit)
    for i in range(l):
        part = unSpaceSplit[i].lower()
        #remove numbers from the portion of the userName
        partNoNum = ''.join([j for j in part if not j.isdigit()])
        if partNoNum in screenName.lower():
            UNhasScreenName = True
    
    #Split up username by underscore
    unUnderscoreSplit = userName.split('_')
    #Check to see if any of the words are in the screen name
    l = len(unUnderscoreSplit)
    for i in range(l):
        part = unUnderscoreSplit[i].lower()
        #remove numbers from the portion of the userName
        partNoNum = ''.join([j for j in part if not j.isdigit()])
        if partNoNum in screenName.lower():
            UNhasScreenName = True
    #print(unRA)
    return(UNhasScreenName)    
        
def dlyFlwLmt(flwCnt):
    #Test to see if Twitter account is at the daily follow limit, 1000
    if (flwCnt==1000):
        return(True)   
    else:
        return(False)
        
        
def isPicDefault(tweet):
    #Test to make sure user has default profile pic
    defaultPicURL = 'https:\/\/abs.twimg.com\/sticky\/default_profile_images\/default_profile_normal.png'
    if (defaultPicURL in tweet):
        return(True)
    else:
        return(False)
        
def hasBio(tweet):
     #Test to make sure that there is no bio from the user
    noBio = '\"description\":null'
    #Split data string into an array where "translator_type" specifies the split.
    bioSplit = tweet.split('\"translator_type\"', 1)
    if (noBio in bioSplit[0]):
        return(False)
    else:
        return(True)
        
def hasLoc(tweet):
     #Test to make sure the user has no location set
    #Split data string into an array where "url" specifies the split.
    locSplit = tweet.split('\"url\"',1)
    noLoc = '\"location\":null'
    if (noLoc in locSplit[0]):
        return(False)
    else:
        return(True)
        
def hasHiFavLoFolw(favCnt, flwrCnt):
    if ((flwrCnt!=0) and (favCnt/flwrCnt)>100):
        return True
    else:
        return False
    
def atThreshold(flwCnt, flwrCnt):
    #Test to see if user is at follower threshold
    #Construct test to determine if the following count (friend count) is 
    #either at Twitter's 5,000 threshold or if it equals their follower count
    #(which must be over 5,000) minus 5,000 times .10 plus 5,000
    if (flwCnt == 5000) or (flwCnt == (.10*(flwrCnt-5000)+5000)):
        return(True)
    else:
        return(False)
        
def HiTwtLoFlwr(twtCnt, flwrCnt):
    #Check for high tweet to follow count (500x more)
    if (flwrCnt!=0):
        if (twtCnt/flwrCnt>=500):
            return(True)
        else:
            return(False)
            
if __name__ == "__main__":
    main()
        



