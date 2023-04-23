# -*- coding: utf-8 -*-
"""book recommendation system.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ip5clQnH3lQmNjraF887nuPThZd1GZ3k
"""

import numpy as np
import pandas as pd


books= pd.read_csv('Books.csv')
users= pd.read_csv('Users.csv')
ratings=pd.read_csv('Ratings.csv')
import difflib
list_of_all_movie_names = books['Book-Title']
list_of_all_movie_names = list_of_all_movie_names.to_frame()
list_of_all_movie_names.drop_duplicates('Book-Title', inplace=True)
list_of_all_movie_names = list_of_all_movie_names['Book-Title'].tolist()
close_match_movie_list = difflib.get_close_matches("bwefbw3ifb34ifb43yfb3ywfb", list_of_all_movie_names)

size = len(close_match_movie_list)
if size != 0:
    print(size)
close_match_movie_list

books.isnull().sum()

users.isnull().sum()

ratings.isnull().sum()

books.duplicated().sum()

ratings.duplicated().sum()

users.duplicated().sum()

"""## popularity based recommendation"""

ratings_with_name=ratings.merge(books,on='ISBN')
ratings_with_name

ratings_with_name.groupby('Book-Title').count()

num_rating_df=ratings_with_name.groupby('Book-Title').count()['Book-Rating'].reset_index()
num_rating_df

num_rating_df.rename(columns={'Book-Rating':'num_rating'},inplace=True)
num_rating_df

avg_rating_df=ratings_with_name.groupby('Book-Title').mean()['Book-Rating'].reset_index()
avg_rating_df.rename(columns={'Book-Rating':'avg_rating'},inplace=True)
avg_rating_df

popular_df=num_rating_df.merge(avg_rating_df,on='Book-Title')
popular_df

popular_df=popular_df[popular_df['num_rating']>250].sort_values('avg_rating',ascending=False).head(50)
popular_df

popular_df=popular_df.merge(books,on='Book-Title').drop_duplicates('Book-Title')[['Book-Title','Book-Author','num_rating','avg_rating','Image-URL-M']]
popular_df

test=ratings_with_name.groupby('User-ID').count()['Book-Rating']>=100;
test=test[test].index
test=ratings_with_name[ratings_with_name['User-ID'].isin(test)]
temp=test.groupby('User-ID').count()['Book-Rating']<200;
temp=temp[temp].index
test=test[test['User-ID'].isin(temp)]
temp=test.groupby('Book-Title').count()['Book-Rating']>=50
temp=temp[temp].index
test=test[test['Book-Title'].isin(temp)]
test

z=ratings_with_name.groupby('User-ID').count()['Book-Rating']>200
good_users=z[z].index
good_users.shape

filtered_rating=ratings_with_name[ratings_with_name['User-ID'].isin(good_users)]
filtered_rating

y=filtered_rating.groupby('Book-Title').count()['Book-Rating']>=50
famous_books=y[y].index
famous_books

final_ratings=filtered_rating[filtered_rating['Book-Title'].isin(famous_books)]

final_ratings.drop_duplicates()

final_ratings.groupby('User-ID').sum()

final_ratings.groupby('Book-Title').sum()

user=final_ratings["User-ID"].unique()
book=final_ratings["Book-Title"].unique()
pivot=[];
def pre_processing(user):
  pre_processed=[0]*len(book)
  df=final_ratings[final_ratings['User-ID'].isin([user])]
  for index, row in df.iterrows():
     for i in range(0,len(book)):
       if(book[i] == row['Book-Title']):
         pre_processed[i]=row['Book-Rating']
  return pre_processed
for i in range(0,len(user)):
  pivot.append(pre_processing(user[i]))

def pre_processing_user(user_book,user_rating):
  pre_processed2=[0]*len(book);
  for i in range(len(user_book)):
    for j in range(len(book)):
      if( book[j] == user_book[i] ):
        pre_processed2[j]=user_rating[i]
  return pre_processed2;

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
def recommendation(user_book,user_rating):
  top_N=20
  b=pre_processing_user(user_book,user_rating)
  a=cosine_similarity(pivot,[b])
  indices = np.argsort(a, axis=0)
  indices = indices[::-1]
  recom=[0]*len(book)
  for i in range(0,top_N):
    for j in range(0,len(book)):
      if(pivot[indices[i][0]][j]>8):
        if(recom[j]!=0):
          recom[j]=(recom[j]+pivot[indices[i][0]][j])/2;
        else:
          recom[j]=pivot[indices[i][0]][j]
  indices = np.argsort(recom, axis=0)
  indices = indices[::-1]
  recom=[]
  for i in range(0,top_N):
    recom.append(book[indices[i]])
  return recom[:top_N+1]


my_df=final_ratings[final_ratings['User-ID'].isin([user[0]])]
tt=['KKK']*my_df.shape[0]
ttt=[0]*my_df.shape[0]
p=0
for index, row in my_df.iterrows():
     tt[p]=row['Book-Title']
     ttt[p]=row['Book-Rating']
     p=p+1;
recom=recommendation(tt,ttt)
final_ratings[final_ratings['Book-Title'].isin(recom)]['Book-Title'].unique()

import pickle
class Myclass:
  def predict(self,tt,ttt):
      decision=recommendation(tt,ttt)
      return decision
model=Myclass()
pickle.dump(model, open('suggestion.pkl','wb'))
model = pickle.load(open('suggestion.pkl','rb'))
print(model.predict(['Harry Potter and the Prisoner of Azkaban (Book 3)' ,"Harry Potter and the Sorcerer's Stone (Book 1)",'Mirror Image'],[9,9,8]))

