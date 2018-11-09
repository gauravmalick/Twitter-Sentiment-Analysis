import tweepy,re
from textblob import TextBlob
import matplotlib.pyplot as plt


class SentimentAnalysis:

    def __init__(self):
        self.tweets = []
        self.tweetText = []
        
    def cleanTweet(self, tweet):
        # Remove Links, Special Characters etc from tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())
   
    # function to calculate percentage
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')
    
    def plotPieChart(self, positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, noOfSearchTerms):
        labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]','Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]', 'Strongly Negative [' + str(snegative) + '%]']
        sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
        colors = ['yellowgreen','lightgreen','darkgreen', 'gold', 'red','lightsalmon','darkred']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('How people are reacting on ' + searchTerm + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()
    
    def SearchForTweet(self):
        consumerKey = '20XFqVsP3jLPGghUNwyBLJCp5'
        consumerSecret = 'YAfjnDUfaeWjqbPiT9cvwqk4PbaFsisKAI0MIXrCS1jv9S4NhC'
        accessToken = '3142382286-qfUt9Ynpl3gA1PbSlQoLQHyoWBAf5DkEs8GAvsg'
        accessTokenSecret = 'I8jbKMs6fHGukflwuQFrsWkc8IOakg0NjceNUePVSURhD'

        try:
            auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
            auth.set_access_token(accessToken, accessTokenSecret)
            api = tweepy.API(auth)
        except:
            print("Error: Authentication Failed")
        
        # input for term to be searched and how many tweets to search
        searchTerm = input("Enter Keyword/Tag to search about: ")
        NoOfTerms = int(input("Enter how many tweets to search: "))

        # searching for tweets
        self.tweets = tweepy.Cursor(api.search, q=searchTerm+" -filter:retweets", lang = "en").items(NoOfTerms)
        # creating some variables to store info
        polarity = 0
        positive = 0
        wpositive = 0
        spositive = 0
        negative = 0
        wnegative = 0
        snegative = 0
        neutral = 0
        
        positives = []
        wpositives = []
        spositives = []
        negatives = []
        wnegatives = []
        snegatives = []
        neutrals = []
        
        # iterating through tweets fetched
        for tweet in self.tweets:
            #Append to temp so that we can store in csv later. I use encode UTF-8
            cleaned_tweet= self.cleanTweet(tweet.text)
            self.tweetText.append(cleaned_tweet.encode('utf-8'))
            # print (tweet.text.translate(non_bmp_map))    #print tweet's text
            analysis = TextBlob(tweet.text)
            # print(analysis.sentiment)  # print tweet's polarity
            polarity += analysis.sentiment.polarity  # adding up polarities to find the average later

            if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
                neutral += 1
                neutrals.append(cleaned_tweet)
            elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
                wpositive += 1
                wpositives.append(cleaned_tweet)
            elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
                positive += 1
                positives.append(cleaned_tweet)
            elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
                spositive += 1
                spositives.append(cleaned_tweet)
            elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
                wnegative += 1
                wnegatives.append(cleaned_tweet)
            elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
                negative += 1
                negatives.append(cleaned_tweet)
            elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
                snegative += 1
                snegatives.append(cleaned_tweet)

        # finding average of how people are reacting
        positive = self.percentage(positive, NoOfTerms)
        wpositive = self.percentage(wpositive, NoOfTerms)
        spositive = self.percentage(spositive, NoOfTerms)
        negative = self.percentage(negative, NoOfTerms)
        wnegative = self.percentage(wnegative, NoOfTerms)
        snegative = self.percentage(snegative, NoOfTerms)
        neutral = self.percentage(neutral, NoOfTerms)

        # finding average reaction
        polarity = polarity / NoOfTerms

        # printing out data
        print("Natural Language Processing Project\n\t\t\t\t-By Gaurav Malik and Aman Bhardwaj\n")
        print("How people are reacting on " + searchTerm + " by analyzing " + str(NoOfTerms) + " tweets.")
        print()
        print("General Report: ")

        if (polarity == 0):
            status= "Neutral"
        elif (polarity > 0 and polarity <= 0.3):
            status= "Weakly Positive"
        elif (polarity > 0.3 and polarity <= 0.6):
            status= "Positive"
        elif (polarity > 0.6 and polarity <= 1):
            status= "Strongly Positive"
        elif (polarity > -0.3 and polarity <= 0):
            status= "Weakly Negative"
        elif (polarity > -0.6 and polarity <= -0.3):
            status= "Negative"
        elif (polarity > -1 and polarity <= -0.6):
            status= "Strongly Negative"
        
        print(status)
        print()
        print("Detailed Report: ")
        print(str(positive) + "% people thought it was positive")
        print(str(wpositive) + "% people thought it was weakly positive")
        print(str(spositive) + "% people thought it was strongly positive")
        print(str(negative) + "% people thought it was negative")
        print(str(wnegative) + "% people thought it was weakly negative")
        print(str(snegative) + "% people thought it was strongly negative")
        print(str(neutral) + "% people thought it was neutral")

        self.plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, NoOfTerms)
        
        print("\n\n5 Random Positive tweets:\n")
        for tweet in positives[:5]:
            print('--> ',tweet,'\n')
            
        print("\n\n5 Random Weakly Positive tweets:\n")
        for tweet in wpositives[:5]:
            print('--> ',tweet,'\n')
            
        print("\n\n5 Random Strongly Positive tweets:\n")
        for tweet in spositives[:5]:
            print('--> ',tweet,'\n')
            
        print("\n\n5 Random Negative tweets:\n")
        for tweet in negatives[:5]:
            print('--> ',tweet,'\n')
            
        print("\n\n5 Random Weakly Negative tweets:\n")
        for tweet in wnegatives[:5]:
            print('--> ',tweet,'\n')
        
        print("\n\n5 Random Strongly Negative tweets:\n")
        for tweet in snegatives[:5]:
            print('--> ',tweet,'\n')
            
        print("\n\n5 Random Neutral tweets:\n")
        for tweet in neutrals[:5]:
            print('--> ',tweet,'\n')
        
        f = open('analysis.txt','w')
        f.write("Natural Language Processing Project\n\t\t\t\t-By Gaurav malik and Aman Bhardwaj\n")
        f.write("\nHow people are reacting on " + searchTerm + " by analyzing " + str(NoOfTerms) + " tweets.")
        f.write("\n\nGeneral Report: \n")
        f.write(status)
        f.write("\n\nDetailed Report: \n")
        f.write(str(positive) + "% people thought it was positive\n")
        f.write(str(wpositive) + "% people thought it was weakly positive\n")
        f.write(str(spositive) + "% people thought it was strongly positive\n")
        f.write(str(negative) + "% people thought it was negative\n")
        f.write(str(wnegative) + "% people thought it was weakly negative\n")
        f.write(str(snegative) + "% people thought it was strongly negative\n")
        f.write(str(neutral) + "% people thought it was neutral\n")
        f.write("\nPositive Tweets: \n")
        for tweet in positives:
            f.write('--> ')
            r= tweet
            for i in range(len(r)):
                try:
                    f.write(r[i])
                except:
                    fake=1
            f.write('\n')
        f.write("\nWeakly Positive Tweets: \n")
        for tweet in wpositives:
            f.write('--> ')
            r= tweet
            for i in range(len(r)):
                try:
                    f.write(r[i])
                except:
                    fake=1
            f.write('\n')
        f.write("\nStrongly Positive Tweets: \n")
        for tweet in spositives:
            f.write('--> ')
            r= tweet
            for i in range(len(r)):
                try:
                    f.write(r[i])
                except:
                    fake=1
            f.write('\n')
        f.write("\nNegative Tweets: \n")
        for tweet in negatives:
            f.write('--> ')
            r= tweet
            for i in range(len(r)):
                try:
                    f.write(r[i])
                except:
                    fake=1
            f.write('\n')
        f.write("\nWeakly Negative Tweets: \n")
        for tweet in wnegatives:
            f.write('--> ')
            r= tweet
            for i in range(len(r)):
                try:
                    f.write(r[i])
                except:
                    fake=1
            f.write('\n')
        f.write("\nStrongly Negative Tweets: \n")
        for tweet in snegatives:
            f.write('--> ')
            r= tweet
            for i in range(len(r)):
                try:
                    f.write(r[i])
                except:
                    fake=1
            f.write('\n')
        f.write("\nNeutral Tweets: \n")
        for tweet in neutrals:
            f.write('--> ')
            r= tweet
            for i in range(len(r)):
                try:
                    f.write(r[i])
                except:
                    fake=1
            f.write('\n')
        f.close()
def main():        
    sa = SentimentAnalysis()
    sa.SearchForTweet()
    
if __name__== "__main__":
    main()