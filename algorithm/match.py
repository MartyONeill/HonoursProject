from lib2to3.pgen2.pgen import DFAState
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from mezza.models import Event

from algorithm.preprocess import preprocess

import pandas as pd
import matplotlib.pyplot as plt

def extract_data(object):

    object_tags = ""

    # > recieve tags from object (Event/Talent/Venue)    
    object_qs = object.account_tags.all().values_list('tags', flat=True)

    # > preprocess requires list as param, convert tags into list
    for i in range(len(object_qs)):
        object_tags += object_qs[i]
    
    # > preprocess, recieve the raw data
    obj_data = preprocess(object.description, object_tags)

    return obj_data

def create_corpus(talent_obj, all_events):

    # > create corpus with all string representations to be used in vectorization
    # > initialise arrays
    corpus = []
    keys = []
    names = []

    # > extract data from talent, add to corpus at index 0, 
    # > keys = id for lookup later, name used for clustering labels
    corpus.append(extract_data(talent_obj))
    keys.append(talent_obj.user.id)
    names.append(talent_obj.user.username)

    # > perform same process for each event, also recieving tags from host venue
    for event in all_events:

        event_tags_str = ""
        event_qs = (event.event_tags.all().values_list('tags', flat=True))

        for i in range(len(event_qs)):
            event_tags_str += event_qs[i]

        for venue_tags in event.venue.account_tags.all():               
            event_tags_str += venue_tags.tags

        # > add data from corpus
        keys.append(event.id)
        names.append(event.venue.name)
        event = preprocess(event.description, event_tags_str)

        # > add new event data to corpus, at indexes 0 ... n
        corpus.append(event)

    return keys, names, corpus

#def recommended_events(talent_obj, all_events):


    # recommended_events_list = []

    # corpus = []
    # keys = []

    # corpus.append(extract_data(talent_obj))
    # keys.append(talent_obj.user.id)

    # for event in all_events:

    #     event_tags_str = ""
    #     event_qs = (event.event_tags.all().values_list('tags', flat=True))

    #     for i in range(len(event_qs)):
    #         event_tags_str += event_qs[i]

    #     for venue_tags in event.venue.account_tags.all():               
    #         event_tags_str += venue_tags.tags

    #     keys.append(event.id)
    #     #event = preprocess(event.description, (event.tags + event.venue.tags))
    #     event = preprocess(event.description, event_tags_str)
    #     corpus.append(event)

def recommended_events(keys, corpus):

    recommended_events_list = []

    # > recieve cosine_scores
    cosine_scores = tf_idf_cosine(corpus)

    # > normalise scores
    scores = normalise(cosine_scores)

    # > add EventIDs to the dataframe
    scores["Event_Id"] = toDataFrame(keys)

    # > returns top scores
    recommended_events = recommend(scores)

    # > for each event, retrieve object from DB using ID, return Events
    for event in range(len(recommended_events.index)):

        id = recommended_events["Event_Id"].iloc[event]
        recommended_events_list.append(Event.objects.get(pk=id))
    
    return recommended_events_list



def tf_idf_cosine(corpus):

    # > initialise vectorizer object
    vectorizer = TfidfVectorizer()

    # tf-idf weight for each word in corpus
    tfidf = vectorizer.fit_transform(corpus)

    # > comparing each document in corpus to itself 
    # > compare x to x - cosine score = 1
    cos_sim = cosine_similarity(tfidf, tfidf)

    # > create dataframe - matrix, 
    # > slice, only the first row is needed
    df = pd.DataFrame(cos_sim)
    return(df.iloc[1:, :1]) 


def normalise(df):

    # > initialise array to aid in normalising calculation
    arr = []

    for array in df.values.tolist():        
        for val in array:
            arr.append(val)

    arr_total = 0  
    norm_arr = []
    
    for val in arr:
        arr_total += val
    
    # > normalsie values between 0 and 1 
    for val2 in arr:
        norm_arr.append(val2/arr_total)

    # > add normlaised to dataframe
    df['Normalised'] = norm_arr

    return(df)#, arr_total, total)


def toDataFrame(arr):

    # > helper function, recieved array and returns dataframe
    # representation of it

    df = pd.DataFrame(arr)

    df = df.iloc[1:]

    return df 

def recommend(df):

    df = df.sort_values(by=['Normalised'], ascending=False)

    # > uncomment piechart(df), a piechart of the split of weight of documents will be shown
    # > seen in the dissertation
    #piechart(df)

    # ----- Normalise -----------
    total = 0
    count = 0

    # > upper 1/3 of values, this has some limitations as discussed in dissertation
    while total < 0.33:

        # > add by normalised value by index
        val = df["Normalised"].iloc[count]

        total += val
        count += 1

    df_recommend = df.iloc[:count]

    # > returns df of top 1/3 of venues by weight rather than count. 
    # > for example, if one venue is 90% similar and all others are only 10% similar, then
    # only the event with the top similairty will be returned
    return(df_recommend)

def piechart(df):

    # > helper code for generating a piechart of weigth of documents

    arr = df["Normalised"].values.tolist()
    labels = df["Event_Id"].values.tolist()
    sizes = []

    #print(arr)
    for val in arr:
        sizes.append(val * 100)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()
