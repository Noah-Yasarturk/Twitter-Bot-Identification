# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 13:39:03 2018

@author: nyasa
"""
import csv


'''
Here, i'll take one of the results of the sorting (a text file)
and morph it to a csv where each line is a screen name.
This is to allow for easy searching of bots.


This runs 3rd in our data pipeline:
1- Stream3.py to gather tweets
2- Process3.py to sort them into warehouses
3- prep4ManualClassification.py to process warehouses into csvs of screen names
4- Process3-2.py to check if tweets are bot-like

'''


def main():
    #path to noLocnoBionoPic
    path1 = 'C:/Users/nyasa/Documents/Classes/Data Mining/Project/testRepos/noLocnoBionoPic2.txt'
    #path to hiFavLoFlwr2
    path2 = 'C:/Users/nyasa/Documents/Classes/Data Mining/Project/testRepos/hiFavLoFlwr2.txt'
    #Address folwThresh
    path3 = 'C:/Users/nyasa/Documents/Classes/Data Mining/Project/testRepos/folwThresh.txt'
    #Address hiTwtLoFlwr
    path4 = 'C:/Users/nyasa/Documents/Classes/Data Mining/Project/testRepos/hiTwtLoFlwr.txt'
    #Address folwThresh_HiFavLoFlwr_hiTwtLoFlwr
    path5 = 'C:/Users/nyasa/Documents/Classes/Data Mining/Project/testRepos/folwThresh_HiFavLoFlwr_hiTwtLoFlwr.txt'
    #Address to dailyFolwThresh
    path6 = 'C:/Users/nyasa/Documents/Classes/Data Mining/Project/testRepos/dailyFolwThresh.txt'
    #Address to dailyFolwThreshToday
    path7 = 'C:/Users/nyasa/Documents/Classes/Data Mining/Project/testRepos/dailyFolwThreshToday.txt'
    #Address to dailyFolwThreshToday_noLocnoBionoPic
    path8 = 'C:/Users/nyasa/Documents/Classes/Data Mining/Project/testRepos/dailyFolwThreshToday_noLocnoBionoPic.txt'
    #Address to dailyFolwThresh_noLocnoBionoPic
    path9 = 'C:/Users/nyasa/Documents/Classes/Data Mining/Project/testRepos/dailyFolwThresh_noLocnoBionoPic.txt'
    #Address to unNotinScrnNm
    path10 = 'C:/Users/nyasa/Documents/Classes/Data Mining/Project/testRepos/unNotinScrnNm.txt'
    ##Address to unNotinScrnNm_hiTwtLoFlwr
    path11 = 'C:/Users/nyasa/Documents/Classes/Data Mining/Project/testRepos/unNotinScrnNm_hiTwtLoFlwr.txt'
    #path 9 and path 2 and path 1 together
    path12 = 'C:/Users/nyasa/Documents/Classes/Data Mining/Project/testRepos/unNotinScrnNm_hiTwtLoFlwr_noLocnoBionoPic.txt'
    
    
    #Open text file warehouses and store tweets to appropriate arrays
    #Text repo file we're opening with
    testRepo1 = open(path1, 'r')
    twtList1 = []
    for line in testRepo1:
        if '\"retweeted_status\":' in line:
                twtList1.append(line)
    
    testRepo2 = open(path2, 'r')
    twtList2 = []
    for line in testRepo2:
        if '\"retweeted_status\":' in line:
                twtList2.append(line)
    
    testRepo3 = open(path3, 'r')
    twtList3 = []
    for line in testRepo3:
        if '\"retweeted_status\":' in line:
                twtList3.append(line)
                
    testRepo4 = open(path4, 'r')
    twtList4 = []
    for line in testRepo4:
        if '\"retweeted_status\":' in line:
                twtList4.append(line)
    
    testRepo5 = open(path5, 'r')
    twtList5 = []
    for line in testRepo5:
        if '\"retweeted_status\":' in line:
                twtList5.append(line)
    
    testRepo6 = open(path6, 'r')
    twtList6 = []
    for line in testRepo6:
        if '\"retweeted_status\":' in line:
                twtList6.append(line)
                
    testRepo7 = open(path7, 'r')
    twtList7 = []
    for line in testRepo7:
        if '\"retweeted_status\":' in line:
                twtList7.append(line)
    
    testRepo8 = open(path8, 'r')
    twtList8 = []
    for line in testRepo8:
        if '\"retweeted_status\":' in line:
                twtList8.append(line)
    
    testRepo9 = open(path9, 'r')
    twtList9 = []
    for line in testRepo9:
        if '\"retweeted_status\":' in line:
                twtList9.append(line)
    
    testRepo10 = open(path10, 'r')
    twtList10 = []
    for line in testRepo10:
        if '\"retweeted_status\":' in line:
                twtList10.append(line)
                
    testRepo11 = open(path11, 'r')
    twtList11 = []
    for line in testRepo11:
        if '\"retweeted_status\":' in line:
                twtList11.append(line)
    
    testRepo12 = open(path12, 'r')
    twtList12 = []
    for line in testRepo12:
        if '\"retweeted_status\":' in line:
                twtList12.append(line)
    
    
    #Delete tweet list duplicates
    twtList1 = Remove(twtList1)
    twtList2 = Remove(twtList2)
    twtList3 = Remove(twtList3)
    twtList4 = Remove(twtList4)
    twtList5 = Remove(twtList5)
    twtList6 = Remove(twtList6)
    twtList7 = Remove(twtList7)
    twtList8 = Remove(twtList8)
    twtList9 = Remove(twtList9)
    twtList10 = Remove(twtList10)
    twtList11 = Remove(twtList11)
    twtList12 = Remove(twtList12)
    
    
    
    #Store tweets into appropriate csvs
    csvPath1 = 'C:/Users/nyasa/Documents/Classes/Data Mining/Project/Manual Investigation/noPicNoBioNoLoc.csv'
    with open(csvPath1, mode='w', newline='') as csv_file1:
        csv_writer1 = csv.writer(csv_file1, delimiter = ',')
        csv_writer1.writerow(['Screen names with default pic, no bio, no location:'])
        for twt in twtList1:
            csv_writer1.writerow([getScreenName(twt)])
    
    csvPath2 = 'C:/Users/nyasa/Documents/Classes/Data Mining/Project/Manual Investigation/hiFavLoFlwr2.csv'
    with open(csvPath2, mode='w', newline='') as csv_file2:
        csv_writer2 = csv.writer(csv_file2, delimiter = ',')
        csv_writer2.writerow(['Screen names with high like to follower ratio:'])
        for twt in twtList2:
            csv_writer2.writerow([getScreenName(twt)])
    
    csvPath3 = 'C:/Users/nyasa/Documents/Classes/Data Mining/Project/Manual Investigation/folwThresh.csv'
    with open(csvPath3, mode='w', newline='') as csv_file3:
        csv_writer3 = csv.writer(csv_file3, delimiter = ',')
        csv_writer3.writerow(['Screen names at follow threshold'])
        for twt in twtList3:
            csv_writer3.writerow([getScreenName(twt)])
            
    csvPath4 = 'C:/Users/nyasa/Documents/Classes/Data Mining/Project/Manual Investigation/hiTwttoFolw.csv'
    with open(csvPath4, mode='w', newline='') as csv_file4:
        csv_writer4 = csv.writer(csv_file4, delimiter = ',')
        csv_writer4.writerow(['Screen names with high tweet to follower ratio'])
        for twt in twtList4:
            csv_writer4.writerow([getScreenName(twt)])
            
    csvPath5 = 'C:/Users/nyasa/Documents/Classes/Data Mining/Project/Manual Investigation/folwThresh_HiFavLoFlwr_hiTwtLoFlwr.csv'
    with open(csvPath5, mode='w', newline='') as csv_file5:
        csv_writer5 = csv.writer(csv_file5, delimiter = ',')
        csv_writer5.writerow(['Screen names with folwThresh_HiFavLoFlwr_hiTwtLoFlwr'])
        for twt in twtList5:
            csv_writer5.writerow([getScreenName(twt)])
            
    csvPath6 = 'C:/Users/nyasa/Documents/Classes/Data Mining/Project/Manual Investigation/DailyThresh.csv'
    with open(csvPath6, mode='w', newline='') as csv_file6:
        csv_writer6 = csv.writer(csv_file6, delimiter = ',')
        csv_writer6.writerow(['Screen names at Daily Follow Threshold:'])
        for twt in twtList6:
            csv_writer6.writerow([getScreenName(twt)])

    csvPath7 = 'C:/Users/nyasa/Documents/Classes/Data Mining/Project/Manual Investigation/dailyFolwThreshToday.csv'
    with open(csvPath7, mode='w', newline='') as csv_file7:
        csv_writer7 = csv.writer(csv_file7, delimiter = ',')
        csv_writer7.writerow(['Screen names at Daily Follow Threshold today:'])
        for twt in twtList7:
            csv_writer7.writerow([getScreenName(twt)])

    csvPath8 = 'C:/Users/nyasa/Documents/Classes/Data Mining/Project/Manual Investigation/dailyFolwThreshToday_noLocnoBionoPic.csv'
    with open(csvPath8, mode='w', newline='') as csv_file8:
        csv_writer8 = csv.writer(csv_file8, delimiter = ',')
        csv_writer8.writerow(['Screen names w/ dailyFolwThreshToday_noLocnoBionoPic:'])
        for twt in twtList8:
            csv_writer8.writerow([getScreenName(twt)])

    csvPath9 = 'C:/Users/nyasa/Documents/Classes/Data Mining/Project/Manual Investigation/dailyFolwThresh_noLocnoBionoPic.csv'
    with open(csvPath9, mode='w', newline='') as csv_file9:
        csv_writer9 = csv.writer(csv_file9, delimiter = ',')
        csv_writer9.writerow(['Screen names w/ dailyFolwThresh_noLocnoBionoPic:'])
        for twt in twtList9:
            csv_writer9.writerow([getScreenName(twt)])

    csvPath10 = 'C:/Users/nyasa/Documents/Classes/Data Mining/Project/Manual Investigation/unNotinScreenName.csv'
    with open(csvPath10, mode='w', newline='') as csv_file10:
        csv_writer10 = csv.writer(csv_file10, delimiter = ',')
        csv_writer10.writerow(['Screen name diff from Username:'])
        for twt in twtList10:
            csv_writer10.writerow([getScreenName(twt)])
            
    csvPath11 = 'C:/Users/nyasa/Documents/Classes/Data Mining/Project/Manual Investigation/unNotinScrnNm_hiTwtLoFlwr.csv'
    with open(csvPath11, mode='w', newline='') as csv_file11:
        csv_writer11 = csv.writer(csv_file11, delimiter = ',')
        csv_writer11.writerow(['Screen name diff from Username:'])
        for twt in twtList11:
            csv_writer11.writerow([getScreenName(twt)])
        
    ##unNotinScreenName and HiTwtLoFolwr and noLocnoBionoPic
    csvPath12 = 'C:/Users/nyasa/Documents/Classes/Data Mining/Project/Manual Investigation/unNotinScreenName_HiTwtLoFolwr_noLocnoBionoPic.csv'
    with open(csvPath12, mode='w', newline='') as csv_file12:
        csv_writer12 = csv.writer(csv_file12, delimiter = ',')
        csv_writer12.writerow(['Screen name diff from Username AND bot features:'])
        for twt in twtList12:
            csv_writer12.writerow([getScreenName(twt)])
    
    #Close openned files
    #Text warehouses
    testRepo1.close()
    testRepo2.close()
    testRepo3.close()
    testRepo4.close()
    testRepo5.close()
    testRepo6.close()
    testRepo7.close()
    testRepo8.close()
    testRepo9.close()
    testRepo10.close()
    testRepo11.close()
    testRepo12.close()
    #Csvs we've written to
    csv_file1.close()
    csv_file2.close()
    csv_file3.close()
    csv_file4.close()
    csv_file5.close()    
    csv_file6.close()
    csv_file7.close()
    csv_file8.close()
    csv_file9.close()
    csv_file10.close()
    csv_file11.close()
    csv_file12.close()


# Python code to remove duplicate elements 
def Remove(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list


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

if __name__ == "__main__":
    main()
        
    