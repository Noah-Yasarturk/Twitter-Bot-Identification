# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 08:42:05 2018

@author: nyasa
"""
from datetime import date


'''
In this python script, I'll test to ensure each of my test methods function
as intended.
I'll run these methods on a sample tweet.
'''


def main():
    #Take sample from the top of dailyFolwThresh
    sampleFile = 'C:/Users/nyasa/Documents/Classes/Data Mining/Project/Sample Data/sampleTwt.txt'
    #Convert txt file to string data
    with open(sampleFile, 'r') as myfile:
        data=myfile.read().replace('\n', '')
    today = datetime.datetime.today().strftime('%m-%d-%y')
    #print(data)
        
    #Test Methods
    print('Running tests of our methods ...')
    print('')
    
    ## Test getScreenName() ; should return 'michael_maxwell'
    '''
    print('getScreenName() returns '+ str(getScreenName(data))+'. It should be michael_maxwell.')
    ## Test getUserName() ; should return 'M Maxwell'
    print('getUserName() returns '+ getUserName(data)+'. It should be M Maxwell.')
    ## Test getDateTwtd() ; should return 11-01
    print('getDateTwtd() returns '+getDateTwtd(data)+'. It should be 11-01.')
    ## Test getTwtCnt() ; should return 21619
    print('getTwtCnt() returns '+str(getTwtCnt(data))+'. It should be 21619.')
    ## Test getFlwrs() ; should return 346
    print('getFlwrs() returns '+str(getFlwrs(data))+'. It should be 346.')
    ## Test getFavs() ; should return 14893
    print('getFavs() returns '+str(getFavs(data))+'. It should be 14893.')
    ## Test getFlws() ; should return 1000
    print('getFlws() returns '+str(getFlws(data))+'. It should be 1000.')
    ## Test UNinScreenName() ; should return True
    print('UNinScreenName() returns '+str(UNinScreenName(getUserName(data),getScreenName(data)))+'. It should be True.')
    ## Test dlyFlwLmt() ; should return True
    print('dlyFlwLmt() returns '+str(dlyFlwLmt(data, getFlws(data)))+'. It should be True.')
    ## Test isPicDefault()
    
    ## Test hasBio()
    
    ## Test hasLoc()
    
    ## Test hasHiFavLoFolw()
    print('hasHiFavLoFolw() returns '+str(hasHiFavLoFolw(data, getFavs(data), getFlws(data)))+'. It should be False.' )
    ## Test atThreshold()
    
    ## HiTwtLoFlwr()
    print('HiTwtLoFlwr() returns '+str(HiTwtLoFlwr(data, getTwtCnt(data), getFlwrs(data)))+'. It should be False.')
    ## Test getAccntCre8d8() ; should return "Thu Dec 18 01:33:24 +0000 2008"
    print('getAccntCre8d8() returns '+getAccntCre8d8(data)+'. It should be \"Thu Dec 18 01:33:24 +0000 2008\".')
    #print('getAccntCre8d8() returns '+getAccntCre8d8(data)+'. It should be \"Tue Jul 12 04:31:24 +0000 2011\".')
    ## Test d8Compare()
    d1 = ('2-28-2017')
    d2 = ('2-18-2017')
    print('d8Compare() returns '+str(d8Compare(d1,d2))+'. It should be 10.')'''
    ## Test accntYung on 4 samples
    s1 = 'C:/Users/nyasa/Documents/Classes/Data Mining/Project/Sample Data/s1.txt'
    s2 = 'C:/Users/nyasa/Documents/Classes/Data Mining/Project/Sample Data/s2.txt'
    s3 = 'C:/Users/nyasa/Documents/Classes/Data Mining/Project/Sample Data/s3.txt'
    s4 = 'C:/Users/nyasa/Documents/Classes/Data Mining/Project/Sample Data/s4.txt'
    print('accntYung returns '+accntYung(s1,today)+'. It should be )
    
    myfile.close()

#Processing methods
#Getters and Setters
def getAccntCre8d8(tweet):
    dateRaw = ''
    yungHalf = '\"in_reply_to_screen_name\":'
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
    screenName = ''
    scrnFront = '\",\"screen_name\":\",\"'
    scrnBack = '\",\"location\"'
    scrnBehind = '\"name\":"'
    scrnSplit1 = tweet.split(scrnBehind,1)
    #scrnSplit1[1] is now '"(username)", "screen_name":...'
    scrnSplit2 = scrnSplit1[1].split(scrnBack,1)
    #scrnSplit2[0] is now "(username)", "screen_name":,"(screenName)"'
    scrnSplit3 = scrnSplit2[0].split(scrnFront,1)
    #scrnSplit3[1] is now '(screenName)"'
    scrnSplit4 = scrnSplit3[0].split('\"',1)
    screenName = scrnSplit4[0]
    return(screenName)
    
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
    '11-05-18', and returns how many days are between the two
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
    return(delta.days)   
    
        
        
def UNinScreenName(userName, screenName):
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

        
        
def dlyFlwLmt(tweet, flwCnt):
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
        
def hasHiFavLoFolw(tweet, favCnt, flwrCnt):
    if ((flwrCnt!=0) and (favCnt/flwrCnt)>100):
        return True
    else:
        return False
    
def atThreshold(tweet, flwCnt, flwrCnt):
    #Test to see if user is at follower threshold
    #Construct test to determine if the following count (friend count) is 
    #either at Twitter's 5,000 threshold or if it equals their follower count
    #(which must be over 5,000) minus 5,000 times .10 plus 5,000
    if (flwCnt == 5000) or (flwCnt == (.10*(flwrCnt-5000)+5000)):
        return(True)
    else:
        return(False)
        
def HiTwtLoFlwr(tweet, twtCnt, flwrCnt):
    #Check for high tweet to follow count (1000x more)
    if (flwrCnt!=0):
        if (twtCnt/flwrCnt>=1000):
            return(True)
        else:
            return(False)
            
if __name__ == '__main__':    
    main()