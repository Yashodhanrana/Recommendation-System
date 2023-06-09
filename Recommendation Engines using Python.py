#!/usr/bin/env python
# coding: utf-8

# ## Recommendation System

# In[2]:


import pandas as pd
import numpy as np


# In[3]:


credits = pd.read_csv("tmdb_5000_credits.csv")


# In[7]:


movies_df = pd.read_csv("tmdb_5000_movies.csv")


# In[8]:


credits.head()


# In[9]:


movies_df.head()


# In[11]:


print("Credits:",credits.shape)
print("Movies Dataframe:",movies_df.shape)


# In[14]:


credits_column_renamed = credits.rename(index=str, columns={"movie_id": "id"})
movies_df_merge = movies_df.merge(credits_column_renamed, on='id')
movies_df_merge.head()


# In[15]:


movies_cleaned_df = movies_df_merge.drop(columns=['homepage', 'title_x', 'title_y', 'status','production_countries'])
movies_cleaned_df.head()


# In[16]:


movies_cleaned_df.info()


# ### Using Weighted average for each movie's  Average Rating

# ![image.png](attachment:image.png)
# 
# 
#                   Source: http://trailerpark.weebly.com/imdb-rating.html?source=post_page---------------------------

# In[18]:


# Calculate all the components based on the above formula
v=movies_cleaned_df['vote_count']
R=movies_cleaned_df['vote_average']
C=movies_cleaned_df['vote_average'].mean()
m=movies_cleaned_df['vote_count'].quantile(0.70)


# In[19]:


movies_cleaned_df['weighted_average']=((R*v)+ (C*m))/(v+m)


# In[21]:


movies_cleaned_df.head()


# In[23]:


movie_sorted_ranking=movies_cleaned_df.sort_values('weighted_average',ascending=False)
movie_sorted_ranking[['original_title', 'vote_count', 'vote_average', 'weighted_average', 'popularity']].head(20)


# In[34]:


import matplotlib.pyplot as plt
import seaborn as sns

weight_average=movie_sorted_ranking.sort_values('weighted_average',ascending=False)
plt.figure(figsize=(12,6))
axis1=sns.barplot(x=weight_average['weighted_average'].head(10), y=weight_average['original_title'].head(10), data=weight_average)
plt.xlim(4, 10)
plt.title('Best Movies by average votes', weight='bold')
plt.xlabel('Weighted Average Score', weight='bold')
plt.ylabel('Movie Title', weight='bold')
plt.savefig('best_movies.png')


# In[38]:


popularity.head()


# In[39]:


popularity=movie_sorted_ranking.sort_values('popularity',ascending=False)
plt.figure(figsize=(12,6))
ax=sns.barplot(x=popularity['popularity'].head(10), y=popularity['original_title'].head(10), data=popularity)

plt.title('Most Popular by Votes', weight='bold')
plt.xlabel('Score of Popularity', weight='bold')
plt.ylabel('Movie Title', weight='bold')
plt.savefig('best_popular_movies.png')


# ### Recommendation based on scaled weighted average and popularity score(Priority is given 50% to both)

# In[41]:


from sklearn.preprocessing import MinMaxScaler

scaling=MinMaxScaler()
movie_scaled_df=scaling.fit_transform(movies_cleaned_df[['weighted_average','popularity']])
movie_normalized_df=pd.DataFrame(movie_scaled_df,columns=['weighted_average','popularity'])
movie_normalized_df.head()


# In[42]:


movies_cleaned_df[['normalized_weight_average','normalized_popularity']]= movie_normalized_df


# In[43]:


movies_cleaned_df.head()


# In[44]:


# add new column and multiply by 50%
movies_cleaned_df['score'] = movies_cleaned_df['normalized_weight_average'] * 0.5 + movies_cleaned_df['normalized_popularity'] * 0.5
movies_scored_df = movies_cleaned_df.sort_values(['score'], ascending=False)
movies_scored_df[['original_title', 'normalized_weight_average', 'normalized_popularity', 'score']].head(20)


# In[45]:


scored_df = movies_cleaned_df.sort_values('score', ascending=False)

plt.figure(figsize=(16,6))

ax = sns.barplot(x=scored_df['score'].head(10), y=scored_df['original_title'].head(10), data=scored_df, palette='deep')

#plt.xlim(3.55, 5.25)
plt.title('Best Rated & Most Popular Blend', weight='bold')
plt.xlabel('Score', weight='bold')
plt.ylabel('Movie Title', weight='bold')

plt.savefig('scored_movies.png')


# In[ ]:




