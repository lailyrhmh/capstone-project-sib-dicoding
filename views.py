from flask import Blueprint, render_template, abort, request

views = Blueprint(__name__, "views")

import nltk
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('omw-1.4')

import numpy as np
# import matplotlib.pyplot as plt
import pandas as pd
from nltk.corpus import stopwords
stop = set(stopwords.words('english'))
stop.update(['.', ',', '"', "'", '?','|','!', ':', ';', '(', ')', '[', ']', '{', '}',''])
from nltk.stem import WordNetLemmatizer

df = pd.read_csv('./dataset/Daylio_Abid.csv')

new_df = df.dropna(axis = 0, how ='any')

new_df = df.drop(['full_date', 'date', 'time', 'weekday'], axis=1)

def search_activities(sub_mood):
    lemmatizer = WordNetLemmatizer()
    activitiescount = {}
    for i in range(939):
      sub_temp = (new_df["sub_mood"][i])
      if sub_mood in sub_temp:
          activitiestemp = [lemmatizer.lemmatize(temps.strip().replace('.','').replace(',','').lower()) for temps in str(new_df["activities"][i]).split('|') if temps.strip() not in stop ]
          for a in activitiestemp:
              if a not in activitiescount.keys():
                  activitiescount[a] = 1 
              else:
                  activitiescount[a] += 1
    sorted_activities = []
    sorted_activities = sorted(activitiescount, key=activitiescount.get, reverse=True)
    return sorted_activities


def activities_recommendation(sub_mood):
    topn = []
    topn = search_activities(sub_mood) #function create dictionary only for particular mood
    print("5 Recommendation Activities in %s are:"%(sub_mood))
    # print(topn[0])
    # print(topn[1])
    # print(topn[2])
    # print(topn[3])
    # print(topn[4])
    return topn[:5]

@views.route("/")
def home():
    return render_template("index.html")

@views.route("/form-mood")
def formMood():
    return render_template("form-mood.html")

@views.route("/recommendation-activity", methods=['GET'])
def recommendation():
    return render_template("activity-recomendation.html")

@views.route('/recommendation-activity/result')
def get_activities():
    sub_mood = request.args.get('sub_mood')
    result = activities_recommendation(sub_mood)
    result_str = 'You should eat {}, {}, or {}.'.format(result[0], result[1], result[2])
    return render_template('activity-result.html', result=result_str, sub_mood=sub_mood)
