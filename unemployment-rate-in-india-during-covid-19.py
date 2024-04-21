#!/usr/bin/env python
# coding: utf-8

# 
# # unemployment in India during covid-19
# 
# ### objective of analysis is -
# 
# * To know the covid-19 impact on job market
# 
# * which state survive and which state has more impact on
# 
# 
# ## This dataset contains the unemployment rate of all the states in India
# 
# * States = states in India
# * Date = date which the unemployment rate observed
# * Frequency = measuring frequency (Monthly)
# * Estimated Unemployment Rate (%) = percentage of people unemployed in each States of India
# * Estimated Employed = Number of people employed
# * Estimated Labour Participation Rate (%) = The labour force participation rate is the portion of the working population in the 16-64 years' age group in the economy currently in employment or seeking employment.
# 
# 
# 
# 

# # Index
# 
# * <a href="#Data-Import">Data Import</a>
# * <a href="#Stats">Stats</a>
# * <a href="#Data-exploratory-Analysis">Data exploratory Analysis</a>
# * <a href="#Impact-of-Lockdown-on-States-Estimated-Employed">Impact-of-Lockdown-on-States-Estimated-Employed</a>
# 

# In[1]:


import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

import calendar


# In[2]:


import datetime as dt

import plotly.io as pio
pio.templates


# In[3]:


import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from IPython.display import HTML


# # Data Import

# In[4]:



df = pd.read_csv('Unemployment_Rate_upto_11_2020.csv')


# In[5]:


df.head()


# In[6]:


df.info()


# In[7]:


df.isnull().sum()


# In[8]:


df.columns =['States','Date','Frequency','Estimated Unemployment Rate','Estimated Employed','Estimated Labour Participation Rate','Region','longitude','latitude']


# In[9]:


df['Date'] = pd.to_datetime(df['Date'],dayfirst=True)


# In[10]:


df['Frequency']= df['Frequency'].astype('category')


# In[11]:


df['Month'] =  df['Date'].dt.month


# In[12]:


df['Month_int'] = df['Month'].apply(lambda x : int(x))


# In[13]:



df['Month_name'] =  df['Month_int'].apply(lambda x: calendar.month_abbr[x])


# In[14]:


df['Region'] = df['Region'].astype('category')


# In[15]:


df.drop(columns='Month',inplace=True)
df.head(3)


# # Stats

# In[16]:


df_stats = df[['Estimated Unemployment Rate',
      'Estimated Employed', 'Estimated Labour Participation Rate']]


round(df_stats.describe().T,2)


# In[17]:


region_stats = df.groupby(['Region'])[['Estimated Unemployment Rate','Estimated Employed','Estimated Labour Participation Rate']].mean().reset_index()

region_stats = round(region_stats,2)


region_stats


# In[18]:


heat_maps = df[['Estimated Unemployment Rate',
       'Estimated Employed', 'Estimated Labour Participation Rate',
       'longitude', 'latitude', 'Month_int']]

heat_maps = heat_maps.corr()

plt.figure(figsize=(10,6))
sns.set_context('notebook',font_scale=1)
sns.heatmap(heat_maps, annot=True,cmap='summer');


# # Data exploratory Analysis

# In[19]:


fig = px.box(df,x='States',y='Estimated Unemployment Rate',color='States',title='Unemployment rate',template='plotly')
fig.update_layout(xaxis={'categoryorder':'total descending'})
fig.show()

# The below box shows unemployement rate in each state in India


# In[20]:


fig = px.scatter_matrix(df,template='plotly',
    dimensions=['Estimated Unemployment Rate','Estimated Employed',
                'Estimated Labour Participation Rate'],
    color='Region')
fig.show()


# In[21]:


plot_ump = df[['Estimated Unemployment Rate','States']]

df_unemp = plot_ump.groupby('States').mean().reset_index()

df_unemp = df_unemp.sort_values('Estimated Unemployment Rate')

fig = px.bar(df_unemp, x='States',y='Estimated Unemployment Rate',color='States',
            title='Average Unemployment Rate in each state',template='plotly')

fig.show()


# In[22]:


fig = px.bar(df, x='Region',y='Estimated Unemployment Rate',animation_frame = 'Month_name',color='States',
            title='Unemployment rate across region from Jan.2020 to Oct.2020', height=700,template='plotly')

fig.update_layout(xaxis={'categoryorder':'total descending'})

fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2000

fig.show()


# In[23]:


unemplo_df = df[['States','Region','Estimated Unemployment Rate','Estimated Employed','Estimated Labour Participation Rate']]

unemplo = unemplo_df.groupby(['Region','States'])['Estimated Unemployment Rate'].mean().reset_index()


# In[24]:


fig = px.sunburst(unemplo, path=['Region','States'], values='Estimated Unemployment Rate',
                  color_continuous_scale='Plasma',title= 'unemployment rate in each region and state',
                  height=650,template='ggplot2')


fig.show()


# 
# # Impact of Lockdown on States Estimated Employed
# 
# 
# * On 24 March 2020, the Government of India under Prime Minister Narendra Modi ordered a nationwide lockdown for 21 days
# 
# 

# In[25]:


fig = px.scatter_geo(df,'longitude', 'latitude', color="Region",
                     hover_name="States", size="Estimated Unemployment Rate",
                     animation_frame="Month_name",scope='asia',template='plotly',title='Impack of lockdown on employement across regions')

fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2000

fig.update_geos(lataxis_range=[5,35], lonaxis_range=[65, 100],oceancolor="#6dd5ed",
    showocean=True)

fig.show()


# In[26]:


lock = df[(df['Month_int'] >= 4) & (df['Month_int'] <=7)]

bf_lock = df[(df['Month_int'] >= 1) & (df['Month_int'] <=4)]


# In[27]:


g_lock = lock.groupby('States')['Estimated Unemployment Rate'].mean().reset_index()

g_bf_lock = bf_lock.groupby('States')['Estimated Unemployment Rate'].mean().reset_index()


g_lock['Unemployment Rate before lockdown'] = g_bf_lock['Estimated Unemployment Rate']

g_lock.columns = ['States','Unemployment Rate after lockdown','Unemployment Rate before lockdown']

g_lock.head(2)


# In[28]:


# percentage change in unemployment rate
g_lock['percentage change in unemployment'] = round(g_lock['Unemployment Rate after lockdown'] - g_lock['Unemployment Rate before lockdown']/g_lock['Unemployment Rate before lockdown'],2)


# In[29]:


plot_per = g_lock.sort_values('percentage change in unemployment')


# In[30]:


# percentage change in unemployment after lockdown

fig = px.bar(plot_per, x='States',y='percentage change in unemployment',color='percentage change in unemployment',
            title='percentage change in Unemployment in each state after lockdown',template='ggplot2')

fig.show()


# # most impacted states/UT
# 
# * Puducherry
# * Jharkhand
# * Bihar
# * Haryana
# * Tripura
# 

# In[31]:


# function to sort value based on impact

def sort_impact(x):
    if x <= 10:
        return 'impacted States'
    elif x <= 20:
        return 'hard impacted States'
    elif x <= 30:
        return 'harder impacted States'
    elif x <= 40:
        return 'hardest impacted States'
    return x    


# In[32]:


plot_per['impact status'] = plot_per['percentage change in unemployment'].apply(lambda x:sort_impact(x))


# In[33]:


fig = px.bar(plot_per, y='States',x='percentage change in unemployment',color='impact status',
            title='Impact of lockdown on employment across states',template='ggplot2',height=650)


fig.show()


# ### upvote if you like it
# 
# ### Thanks!

# In[ ]:




