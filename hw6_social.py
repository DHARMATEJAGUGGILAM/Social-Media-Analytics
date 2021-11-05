"""
Social Media Analytics Project
Name:
Roll Number:
"""

import hw6_social_tests as test

project = "Social" # don't edit this

### PART 1 ###

import pandas as pd
import nltk
nltk.download('vader_lexicon', quiet=True)
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
from typing import Counter
endChars = [ " ", "\n", "#", ".", ",", "?", "!", ":", ";", ")" ]

'''
makeDataFrame(filename)
#3 [Check6-1]
Parameters: str
Returns: dataframe
'''
def makeDataFrame(filename):
    Table_DF = pd.read_csv(filename)
    return Table_DF

'''
parseName(fromString)
#4 [Check6-1]
Parameters: str
Returns: str
'''
def parseName(fromString):
    index1 = fromString.find(":")
    index2 = fromString.find("(")
    index3 = fromString[index1+2:index2-1]       
    return index3


'''
parsePosition(fromString)
#4 [Check6-1]
Parameters: str
Returns: str
'''
def parsePosition(fromString):
    index4 = fromString.find("(")
    index5 = fromString.find("fr")
    index6 = fromString[index4+1:index5-1]   
    return index6


'''
parseState(fromString)
#4 [Check6-1]
Parameters: str
Returns: str
'''
def parseState(fromString):
    index2 = fromString.find("from")
    index4 = fromString.find(")")
    index5 = fromString[index2+5:index4]   
    return index5

'''
findHashtags(message)
#5 [Check6-1]
Parameters: str
Returns: list of strs
'''
def findHashtags(message):
    hashtag_list =[]
    msg=message.split("#")
    for word in msg[1:]:
        r = ""
        for charecter in word:
            if charecter in endChars:
                break
            r+= charecter
        r="#"+r
        hashtag_list.append(r)
    return hashtag_list

'''
getRegionFromState(stateDf, state)
#6 [Check6-1]
Parameters: dataframe ; str
Returns: str
'''
def getRegionFromState(stateDf, state):
    row=stateDf.loc[stateDf['state'] == state, 'region' ]
    return row.values[0]


'''
addColumns(data, stateDf)
#7 [Check6-1]
Parameters: dataframe ; dataframe
Returns: None
'''
def addColumns(data, stateDf):
    print(data['label'])
    names=[]
    positions= []
    states= []
    regions = []
    hashtags = []
    for index, row in data.iterrows():
        labelvalue = row['label']
        names.append(parseName(labelvalue)) 
        positions.append(parsePosition(labelvalue))
        states.append(parseState(labelvalue))
        regions.append(getRegionFromState(stateDf,parseState(labelvalue)))
        textvalue= row['text']
        hashtags.append(findHashtags(textvalue))
    data['name']=names
    data['position']=positions
    data['state']=states
    data['region']=regions
    data['hashtags']=hashtags
    #print(positions)
    return None


### PART 2 ###

'''
findSentiment(classifier, message)
#1 [Check6-2]
Parameters: SentimentIntensityAnalyzer ; str
Returns: str
'''
def findSentiment(classifier, message):
    score = classifier.polarity_scores(message)['compound']
    if score<-0.1:
        return "negative"
    elif score>0.1:
        return "positive"
    else :
        return "neutral"


'''
addSentimentColumn(data)
#2 [Check6-2]
Parameters: dataframe
Returns: None
'''
def addSentimentColumn(data):
    classifier = SentimentIntensityAnalyzer()
    # print(data)
    #print(data["text"])
    sentiments=[]
    for index, row in data.iterrows():
        message=data["text"].loc[index]
        text=findSentiment(classifier, message)
        sentiments.append(text)
        
    data["sentiment"]=sentiments
    #print(data["sentiment"])


    return


'''
getDataCountByState(data, colName, dataToCount)
#3 [Check6-2]
Parameters: dataframe ; str ; str
Returns: dict mapping strs to ints
'''
def getDataCountByState(data, colName, dataToCount):
    x={}
    for i, row in data.iterrows():
        if ((len(colName)==0) and (len(dataToCount)==0) or (row[colName]==dataToCount)):
                state=row["state"]
                if state not in x:
                    x[state] = 1
                else :
                    x[state] += 1
    return x
df = makeDataFrame("data/politicaldata.csv")
stateDf = makeDataFrame("data/statemappings.csv")
addColumns(df, stateDf)
addSentimentColumn(df)


    


'''
getDataForRegion(data, colName)
#4 [Check6-2]
Parameters: dataframe ; str
Returns: dict mapping strs to (dicts mapping strs to ints)
'''
def getDataForRegion(data, colName):
    y={}
    for i, row in data.iterrows():
        region=row["region"]
        if region not in y:
            y[region] = {}
        if  region  in y:
            attack=row[colName]
            if attack not in y[region]:
                y[region][attack] = 1
            else :
                y[region][attack] += 1
    return y


'''
getHashtagRates(data)
#5 [Check6-2]
Parameters: dataframe
Returns: dict mapping strs to ints
'''
def getHashtagRates(data):
    z={} 
    for i in data["hashtags"]: 
        for j in i: 
            if len(j)!=0 and j not in z: 
                z[j]=1 
            else: 
                z[j]+=1 
    return z


'''
mostCommonHashtags(hashtags, count)
#6 [Check6-2]
Parameters: dict mapping strs to ints ; int
Returns: dict mapping strs to ints
'''
def mostCommonHashtags(hashtags, count):
    x={}
    Total=0
    x_dict = sorted(hashtags, key=hashtags.get, reverse=True)
    for r in x_dict:
        if Total<count:
            x[r]= hashtags[r]
            Total=Total+1
        # print(count)
    return (x)



'''
getHashtagSentiment(data, hashtag)
#7 [Check6-2]
Parameters: dataframe ; str
Returns: float
'''
def getHashtagSentiment(data, hashtag):
    x=[]
    for index, row in data.iterrows():
        if hashtag in row['text']:
            if row['sentiment']=='positive':
                x.append(1)
            elif row['sentiment']=='negative':
                x.append(-1)
            elif row['sentiment']=='neutral':
                x.append(0)
            # print(row['text'])
    return sum(x)/len(x)


    


### PART 3 ###

'''
graphStateCounts(stateCounts, title)
#2 [Hw6]
Parameters: dict mapping strs to ints ; str
Returns: None
'''
def graphStateCounts(stateCounts, title):
    import matplotlib.pyplot as plt
    xlist=[i for i in stateCounts]
    w=0.8
    ylist=[stateCounts[i] for i in stateCounts]
    for index in range(len(ylist)):
        plt.bar(xlist[index],ylist[index],width=w)
    plt.xticks(ticks=list(range(len(xlist))),label=xlist,rotation="vertical")
    plt.title(title)
    plt.xlabel("State")
    plt.ylabel("Count")
    plt.show()
    return


'''
graphTopNStates(stateCounts, stateFeatureCounts, n, title)
#3 [Hw6]
Parameters: dict mapping strs to ints ; dict mapping strs to ints ; int ; str
Returns: None
'''
def graphTopNStates(stateCounts, stateFeatureCounts, n, title):
    featurerate={}
    topstates={}
    for i in stateFeatureCounts:
        featurerate[i]=(stateFeatureCounts[i]/stateCounts[i])
    topstates=dict(Counter(featurerate).most_common(n))
    graphStateCounts(topstates,title)


    return


'''
graphRegionComparison(regionDicts, title)
#4 [Hw6]
Parameters: dict mapping strs to (dicts mapping strs to ints) ; str
Returns: None
'''
def graphRegionComparison(regionDicts, title):
    regions= []
    features=[]
    regions_features=[]
    for region in regionDicts:
        regions.append(region)
        for feature in regionDicts[region]:
            if feature not in features:
                features.append(feature)
    for region in regionDicts:
        temp=[]
        for each in features:
            if each  in regionDicts[region]:
                temp.append(regionDicts[region][each])
            else:
                temp.append(0)
        regions_features.append(temp)
    sideBySideBarPlots(features,regions,regions_features,title)
    return


'''
graphHashtagSentimentByFrequency(data)
#4 [Hw6]
Parameters: dataframe
Returns: None
'''
def graphHashtagSentimentByFrequency(data):
    dictionary1=getHashtagRates(data)
    mostcommon=mostCommonHashtags(dictionary1,50)
    hashtaglist=[]
    frequencylist=[]
    sentimentlist=[]
    for i in mostcommon:
        hashtaglist.append(i)
        frequencylist.append(mostcommon[i])
        sentimentlist.append(getHashtagSentiment(data,i))
    scatterPlot(frequencylist,sentimentlist,hashtaglist,"Hashtags Frequency")

    return


#### PART 3 PROVIDED CODE ####
"""
Expects 3 lists - one of x labels, one of data labels, and one of data values - and a title.
You can use it to graph any number of datasets side-by-side to compare and contrast.
"""
def sideBySideBarPlots(xLabels, labelList, valueLists, title):
    import matplotlib.pyplot as plt

    w = 0.8 / len(labelList)  # the width of the bars
    xPositions = []
    for dataset in range(len(labelList)):
        xValues = []
        for i in range(len(xLabels)):
            xValues.append(i - 0.4 + w * (dataset + 0.5))
        xPositions.append(xValues)

    for index in range(len(valueLists)):
        plt.bar(xPositions[index], valueLists[index], width=w, label=labelList[index])

    plt.xticks(ticks=list(range(len(xLabels))), labels=xLabels, rotation="vertical")
    plt.legend()
    plt.title(title)

    plt.show()

"""
Expects two lists of probabilities and a list of labels (words) all the same length
and plots the probabilities of x and y, labels each point, and puts a title on top.
Expects that the y axis will be from -1 to 1. If you want a different y axis, change plt.ylim
"""
def scatterPlot(xValues, yValues, labels, title):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()

    plt.scatter(xValues, yValues)

    # make labels for the points
    for i in range(len(labels)):
        plt.annotate(labels[i], # this is the text
                    (xValues[i], yValues[i]), # this is the point to label
                    textcoords="offset points", # how to position the text
                    xytext=(0, 10), # distance from text to points (x,y)
                    ha='center') # horizontal alignment can be left, right or center

    plt.title(title)
    plt.ylim(-1, 1)

    # a bit of advanced code to draw a line on y=0
    ax.plot([0, 1], [0.5, 0.5], color='black', transform=ax.transAxes)

    plt.show()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":
    # print("\n" + "#"*15 + " WEEK 1 TESTS " +  "#" * 16 + "\n")
    # test.week1Tests()
    # print("\n" + "#"*15 + " WEEK 1 OUTPUT " + "#" * 15 + "\n")
    # test.runWeek1()

    ## Uncomment these for Week 2 ##
    """print("\n" + "#"*15 + " WEEK 2 TESTS " +  "#" * 16 + "\n")
    test.week2Tests()
    print("\n" + "#"*15 + " WEEK 2 OUTPUT " + "#" * 15 + "\n")
    test.runWeek2()"""

    ## Uncomment these for Week 3 ##
    print("\n" + "#"*15 + " WEEK 3 OUTPUT " + "#" * 15 + "\n")
    test.runWeek3()
    # df = makeDataFrame("data/politicaldata.csv")
    # stateDf = makeDataFrame("data/statemappings.csv")
    # addColumns(df, stateDf)
    #addSentimentColumn(df)
    #test.testGetDataCountByState(df)Get a Hashtag's Sentiment Score
    #test.testGetDataForRegion(df) 
    #test.testGetHashtagRates(df) 
    #test.testMostCommonHashtags(df)
    #test.testGetHashtagSentiment(df)
    #test.testAddColumns()
    
