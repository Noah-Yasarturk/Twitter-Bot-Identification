# US_Elections_4_Twits
Implementing basic Twitter scraping techniques, I hoped to be able to predict the outcome of U.S. elections. This was initiated in 2016 but continued in 2018.


The project quickly changed to identifying Twitter bots through multiple tests. Tweets are initially scraped using Stream3.py, preprocessed using Preprocess.py into csvs, and then finally tested through check_Usr_Twts_HdLn.py. Preprocess.py checks 7 tests using only the scraped tweets and creates csvs to keep track of all screen names that trigger any of the tests along with which tests they trigger. check_Usr_Twts_HdLn.py checks the master csv created in Preprocess.py to see if any of its screen names trigger 4 additonal, more rigorous tests.
