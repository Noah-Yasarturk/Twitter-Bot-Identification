# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 09:31:55 2018

@author: nyasa
"""
#imports
import datetime
from datetime import date

'''
Process3 fixes the method errors in Process2-2.py

This runs 2nd in our data pipeline:
1- Stream3.py to gather tweets
2- Process3.py to sort them into warehouses
3- prep4ManualClassification.py to process warehouses into csvs of screen names
4- Process3-2.py to check if tweets are bot-like

'''

def main():
    print('Which warehouse would you like to process?')
    #Create a list of the tweets
    tweetList = []
    
    #Get today's date as Month-Day
    todayMD = datetime.datetime.today().strftime('%m-%d')
    todayMDY = datetime.datetime.today().strftime('%m-%d-%y')
    #copyFile = open('C:/Users/nyasa/Documents/Classes/Data Mining/Project/Trial 3/copyFile.txt', 'a')
    run = input('-->')
    runS = str(run)
    wh = ('C:/Users/nyasa/Documents/Classes/Data Mining/Project/warehouses/warehouse' +runS+'.txt')
    print('Beginning processing of warehouse' +runS+'.txt')
    print('Counting tweets ...')
    with open(wh) as f:
        for line in f:
            if '\"retweeted_status\":' in line:
                tweetList.append(line)
                #copyFile.write(line)
                #print(line)
    f.close()
    print('The number of tweets in warehouse' +runS+ '.txt currently is '+str(len(tweetList))+'.')
    
    #Iterate through tweetList, adding each tweet to the appropriate tct repo file
    ## Address noLocnoBionoPic2
    file1 = open('C:/Users/nyasa/Documents/Classes/Data Mining/Project/testRepos/noLocnoBionoPic2.txt', 'a')
    ## Address hiFavLoFlwr2
    file2 = open('C:/Users/nyasa/Documents/Classes/Data Mining/Project/testRepos/hiFavLoFlwr2.txt', 'a')
    ## Address folwThresh
    file3 = open('C:/Users/nyasa/Documents/Classes/Data Mining/Project/testRepos/folwThresh.txt', 'a')
    ## Address hiTwtLoFlwr
    file4 = open('C:/Users/nyasa/Documents/Classes/Data Mining/Project/testRepos/hiTwtLoFlwr.txt', 'a')
    ## Address folwThresh_HiFavLoFlwr_hiTwtLoFlwr
    file5 = open('C:/Users/nyasa/Documents/Classes/Data Mining/Project/testRepos/folwThresh_HiFavLoFlwr_hiTwtLoFlwr.txt',
                 'a')
    file6 = open('C:/Users/nyasa/Documents/Classes/Data Mining/Project/testRepos/dailyFolwThresh.txt',
                 'a')
    file7 = open('C:/Users/nyasa/Documents/Classes/Data Mining/Project/testRepos/dailyFolwThreshToday.txt',
                 'a')
    file8 = open('C:/Users/nyasa/Documents/Classes/Data Mining/Project/testRepos/dailyFolwThreshToday_noLocnoBionoPic.txt',
                 'a')
    file9 = open('C:/Users/nyasa/Documents/Classes/Data Mining/Project/testRepos/dailyFolwThresh_noLocnoBionoPic.txt',
                 'a')
    file10 = open('C:/Users/nyasa/Documents/Classes/Data Mining/Project/testRepos/unNotinScrnNm.txt',
                 'a')
    file11 = open('C:/Users/nyasa/Documents/Classes/Data Mining/Project/testRepos/unNotinScrnNm_hiTwtLoFlwr.txt',
                 'a')
    file12 = open('C:/Users/nyasa/Documents/Classes/Data Mining/Project/testRepos/unNotinScrnNm_hiTwtLoFlwr_noLocnoBionoPic.txt',
                 'a')
    file13 = open('C:/Users/nyasa/Documents/Classes/Data Mining/Project/testRepos/yungAccnt.txt',
                 'a')
    
    #Count of how many in this run:
    ##Have no bio
    noBioCnt = 0
    ##Have no location
    noLocCnt = 0
    ##Have default profile pic
    noPicCnt = 0
    ##Have 100x as many likes as followers
    hiFavLoFlwrCnt = 0
    ##Are at following threshold
    folwThreshCnt = 0
    ##Have 500x as many tweets as followers
    hiTwtLoFolwrCnt = 0
    ##Are at the daily follow threshold, 1000
    dlyFlwThreshCnt = 0
    ##Are at the daily follow threshold, 1000, TODAY
    dlyFlwThreshTodayCnt = 0
    ##Are at the daily follow threshold, 1000, TODAY, AND noLocnoBionoPic
    dlyFlwThresh2day_noLocnoBionoPicCnt = 0
    ##Are at the daily follow threshold, 1000, AND noLocnoBionoPic
    dlyFlwThreshCnt_noLocnoBionoPicCnt = 0
    ##Does the @name/screen name have anythong from the username?
    unNotSnCnt = 0
    ##Hi twt:Folwr ratio, un not in screen name
    HiTwtLoFolwr_unNotSnCnt = 0
    ##Hi twt:Folwr ratio, un not in screen name, noLocnoBionoPicCnt
    HiTwtLoFolwr_unNotSn_noLocnoBionoPicCnt = 0
    ##Account less than 30 days old
    yungAccntCnt = 0
    
    twtCnt = len(tweetList)
    for t in range(twtCnt):
        #Store current tweeet
        twt = tweetList[t]
        #Tweet attributes
        favCnt = getFavs(twt)
        flwrCnt = getFlwrs(twt)
        flwCnt = getFlws(twt)
        
        #test variables
        t1 = isPicDefault(twt)
        t2 = hasBio(twt)
        t3 = hasLoc(twt)
        t4 = hasHiFavLoFolw(favCnt, flwrCnt)
        t5 = atThreshold(flwCnt, flwrCnt)
        t6 = HiTwtLoFlwr(twtCnt, flwrCnt)
        t7 = dlyFlwLmt(flwCnt)
        t8 = ((getDateTwtd(twt))==todayMD) and (t7==True)
        t9 = (UNinScreenName(getUserName(twt), getScreenName(twt)))
        ## BUGGED (due to d8compare) t10 = accntYung(twt, todayMDY)
        
        #if noLocnoBionoPic
        if ((t1==True) and (t2==False) and (t3==False)):
            noBioCnt = noBioCnt + 1
            noLocCnt = noLocCnt + 1
            noPicCnt = noPicCnt + 1
            file1.write(twt+'\n\n')
        
        #if hiFavLoFlwr
        if (t4==True):
            hiFavLoFlwrCnt = hiFavLoFlwrCnt + 1
            file2.write(twt+'\n\n')
        
        #if folwThresh
        if (t5==True):
            folwThreshCnt = folwThreshCnt + 1
            file3.write(twt+'\n\n')
        
        #if hiTwtLoFolwr
        if (t6==True):
            hiTwtLoFolwrCnt = hiTwtLoFolwrCnt + 1
            file4.write(twt+'\n\n')
            
        #if folwThresh_HiFavLoFlwr_hiTwtLoFlwr
        if (t4==True and t5==True and t6==True):
            file5.write(twt+'\n\n')
            
        #if at daily follow limit
        if (t7==True):
            dlyFlwThreshCnt = dlyFlwThreshCnt + 1
            file6.write(twt+'\n\n')
            
        #if at daily follow limit TODAY
        if (t8==True):
            dlyFlwThreshTodayCnt = dlyFlwThreshTodayCnt + 1
            file7.write(twt+'\n\n')
            
        #if at the daily follower limit TODAY AND noLocnoBionoPic
        if(t8==True and (t1==True) and (t2==False) and (t3==False)):
            dlyFlwThresh2day_noLocnoBionoPicCnt = dlyFlwThresh2day_noLocnoBionoPicCnt + 1
            file8.write(twt+'\n\n')
            
        #if at daily follower limit AND noLocnoBionoPic
        if(t7==True and ((t1==True) and (t2==False) and (t3==False))):
            dlyFlwThreshCnt_noLocnoBionoPicCnt = dlyFlwThreshCnt_noLocnoBionoPicCnt +1
            file9.write(twt+'\n\n')
            
        #if the tweet user's username is not in their screen name (@name)
        if(t9==False):
            unNotSnCnt = unNotSnCnt + 1
            file10.write(twt+'\n\n')
            
        #if HiTwtLoFolwr and unNotinScreenName
        if(t6==True and t9==False):
            HiTwtLoFolwr_unNotSnCnt += 1
            file11.write(twt+'\n\n')
            
        #if HiTwtLoFolwr and unNotinScreenName and noLocnoBionoPic
        if( t6==True and t9==False and ((t1==True) and (t2==False) and (t3==False))):
            HiTwtLoFolwr_unNotSn_noLocnoBionoPicCnt += 1
            file12.write(twt+'\n\n')
        '''   BUGGED- due to d8compare
        #if account is less than 30 days old
        if (t10==True):
            yungAccntCnt +=1
            file13.write(twt+'\n\n')'''
        
   
    #Print counts of tests/sorting
    print('Results:')
    print('(Currently, noLocnoBionoPic is one method)')
    print('')
    print('Number of accounts w/:')
    #print(" -no location: " + str(noLocCnt))
    #print(" -no bio: " + str(noBioCnt))
    #print(" -default profile picture: " + str(noPicCnt))
    print(" -noLocnoBionoPic: " + str(noPicCnt))
    print(" -100x as many likes as follows: " + str(hiFavLoFlwrCnt))
    print(" -followings near the thresholds: " + str(folwThreshCnt))
    print(" -1000x as many tweets as followers: "+ str(hiTwtLoFolwrCnt))
    print(" -All 3 of the above: " + str(hiFavLoFlwrCnt+folwThreshCnt+hiTwtLoFolwrCnt))
    print(" -followings at the daily threshold: " + str(dlyFlwThreshCnt))
    print(" -followings at the daily threshold AND noLocnoBionoPicCnt: " + str(dlyFlwThreshCnt_noLocnoBionoPicCnt))
    print(" -at daily follow threshold today: "+str(dlyFlwThreshTodayCnt))
    print(" -at daily follow threshold today AND noLocnoBionoPicCnt: "+str(dlyFlwThresh2day_noLocnoBionoPicCnt))
    print(" -have a username not in the @name: " + str(unNotSnCnt))
    print(" -have a username not in the @name AND high tweets per followers: " + str(HiTwtLoFolwr_unNotSnCnt))
    print(" -have a username not in the @name AND high tweets per followers AND noLocnoBionoPic: " + str(HiTwtLoFolwr_unNotSn_noLocnoBionoPicCnt))
    print(" -have an account created less than or equal to 30 days ago: "+yungAccntCnt)
    
    #After processing, close the files.
    file1.close()
    file2.close()
    file3.close()
    file4.close()
    file5.close()
    file6.close()
    file7.close()
    file8.close()
    file9.close()
    file10.close()
    file11.close()
    file12.close()
    file13.close()




#Processing methods
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
        #Locate the favorites count
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
    dateRaw = getAccntCre8d8(tweet)
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

def getAccntCre8d8(tweet):
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
        



