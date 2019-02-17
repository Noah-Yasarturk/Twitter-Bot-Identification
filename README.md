# Twitter Bot Identification
This is a follow-up to a project conducted during the 2016 election in which I sought to predict the outcomes of the 2016 Presidential Election by streaming Twitter data, analyzing the data by state to determine if tweets were Pro-Clinton/Anti-Trump or Pro-Trump/Anti-Clinton, and reporting an overall evaluation of whether a given state would vote red or blue.

This project's current iteration focused on streaming election-related Twitter interactions in the weeks leading up to the 2018 midterms and implementing n tests to funnel the most bot-like accounts to our report.

In the future, I hope to further analyze the results test-by-test to develop a decision tree and further automate the bot identification process.


The tests are as such:
Preprocess.py
1. Check if location provided by account
2. Check if description provided by account
3. Check if profile picture is default profile picture
4. Determine if account has a high like-to-follower ratio
    - we somewhat arbitrarily determined 100x as many likes as followers would be considered  high using some sample bot accounts
5. Determine if account has a high tweet-to-follower ratio
    - similarly determined as like-to-follower ratio, 500x as many tweets as followers was seen as high
6. At Twitter's daily follow threshold - 1,000 - today
7. At Twitter's overall follow limit
8. Username not related to screen name
9. Account created in last 30 days (currrently bugged)
check_Twts.py
Accounts that failed 6/8 of the above tests would be additionally processed through the following tests.
1. Tweet text identical to included article's headline
2. Identical reposted tweets
3. >75% similar reposted tweets
4. Use of more than 2 languages in tweet content

For more information on how automated social media accounts are affecting our democracy, please check out the work of Renee Diresta:
http://www.reneediresta.com/


