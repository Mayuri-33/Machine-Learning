#!/usr/bin/env python
# coding: utf-8

# # Step 1: Initial exploration of the Dataset

# In[2]:


import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt


# In[3]:


data = pd.read_csv('C:/Users/Mayuri/Downloads/Indicators.csv')
data.shape


# This is really large dataset, at least in terms of the number of rows. But with 6 columns, what does this hold?

# In[4]:


data.head(10)


# Looks like it has different indicators for different countries with the year and value of the indicator.

# # How many UNIQUE country names are there?

# In[5]:


countries =data['CountryName'].unique()  #tolist= converts data into list
len(countries)


# # Are there same number of country codes?

# In[6]:


#How many unique country codes are there?  #tolist= converts data into list
countryCodes= data['CountryCode'].unique()
len(countryCodes)


# # Are there many indicators or few?

# In[7]:


#How many unique indicators are there?  #tolist= converts data into list
indicators= data['IndicatorName'].unique().tolist()
len(indicators)


# # How many years of data do we have?

# In[8]:


#How many years of data do we have?
years= data['Year'].unique().tolist()
len(years)


# # What's the range of years?

# In[9]:


print(str(min(years))+" to "+str(max(years)))


# # Matplotlib: Basic Plotting, Part 1

# Let's pick a country and an indicator to explore: CO2 Emissions per capita and the USA

# In[14]:


#select CO2 emissions for the United States 
hist_indicator= 'CO2 emissions \(metric'   #metric is used to select a specific data or we can say half data
hist_country='USA'

mask1= data['IndicatorName'].str.contains(hist_indicator)
mask2= data['CountryCode'].str.contains(hist_country)

#stage is just those indicators matching the USA for country code and CO2 emissions over time.
stage= data[mask1 & mask2]


# In[15]:


stage.head()


# # Let's see how emissions have changed over time using MatplotLib

# In[16]:


#get the years
years= stage['Year'].values
#get the values
co2= stage['Value'].values

#create
plt.bar(years, co2)
plt.show()


# In[18]:


#switch to a line plot
plt.plot(stage['Year'].values, stage['Value'].values)

#Label the axes
plt.xlabel('Year')
plt.ylabel(stage['IndicatorName'].iloc[0])

#label the figure
plt.title('CO2 Emissions in USA')

#to make more honest, start they y axis at 0
plt.axis([1959,2011, 0, 25])

plt.show()


# # Using Histogram to explore the distribution of values

# We could also visualize this data as a histogram to better explore the ranges of values in CO2 production per year.

# In[19]:


#If you want to just include those within one standard deviation for the mean, you could do the following
#lower= stage['Value'].mean()-stage['Value'].std()
#upper= stage['Value'].mean()+stage['Value'].std()
#hist_data= [x for x in stage[:10000]['Value']if x>lower and x<upper ]

#otherwise, let's look at all the data
hist_data= stage['Value'].values


# In[20]:


print(len(hist_data))


# In[21]:


#the histogram of the data 
plt.hist(hist_data, 10, density=False, facecolor='green')
#density= false means our width of bar will be same
plt.xlabel(stage['IndicatorName'].iloc[0])
plt.ylabel('# of Years')
plt.title('Histogram Example')

plt.grid(True)

plt.show()


# So the USA has many years where it produced between 19-20 metric tons per capita with outliers on either side.

# # But how do the USA's numbers relate to those of other countries?

# In[25]:


#select CO2 emissions for all countries in 2011
hist_indicator = 'CO2 emissions \(metric'
hist_year= 2011

mask1= data['IndicatorName'].str.contains(hist_indicator)
mask2= data['Year'].isin([hist_year])

#apply our mask
co2_2011= data[mask1 & mask2]
co2_2011.head()


# For how many countries do we have CO2 per capita emissions data in 2011

# In[26]:


print(len(co2_2011))


# In[27]:


#let's plot a histogram of the emissions per capita by country

#subplots returns a tuple with the figure, axis attributes.
fig, ax = plt.subplots()

ax.annotate("USA",
            xy=(18,5), xycoords= 'data',
            xytext= (18, 30), textcoords='data',
            arrowprops= dict(arrowstyle="->",
                             connectionstyle="arc3"),
           )

plt.hist(co2_2011['Value'], facecolor='blue')
#density: width of your bins false will have all same size of bins.
plt.xlabel(stage['IndicatorName'].iloc[0])
plt.ylabel('# of Countries')
plt.title('Histogram of CO2 Emissions Per Capita')

#plt.axis([10, 22, 0, 14])
plt.grid(True)
plt.show()


# So the USA, at ~18 CO2 emissions (metric tons per capital) is quite high among all countries.
# 
# An interesting next step, which we'll save for you, would be to explore how this relates to other industrialized nations and to look at the outliers with those values in the 40s!

# # Matplotlib: Basic Plotting, Part 2

# Relationship between GDP and CO2 Emissions in USA

# In[28]:


#select GDP Per capita emissions for the United States
hist_indicator= 'GDP per capita \(constant 2005'
hist_country = 'USA'

mask1= data['IndicatorName'].str.contains(hist_indicator)
mask2= data['CountryCode'].str.contains(hist_country)

#stage is just those indicators matching the USA for country code and CO2 emissions over time.
gdp_stage= data[mask1 & mask2]

#plot gdp_stage vs stage


# In[30]:


gdp_stage.head(2)


# In[31]:


stage.head(2)


# In[34]:


#switch to a line plot
plt.plot(gdp_stage['Year'].values, gdp_stage['Value'].values)

#label the axes 
plt.xlabel('Year')
plt.ylabel(gdp_stage['IndicatorName'].iloc[0])

#label the figure 
plt.title('GDP Per Capita USA')

#to make more honest, start the y axis at 0
#plt.axis([1959, 2011, 0,25])    #line can't be seen as due to this co-ordi are just as an example and may not suitable for below plot

plt.show()


# # ScatterPlot for comparing GDP against CO2 emissions (per capita)

# First, we'll need to make sure we're looking at the same time frames

# In[35]:


print("GDP Min Year= ", gdp_stage['Year'].min(), "max:", gdp_stage['Year'].max())
print("CO2 Min Year= ", stage['Year'].min(), "max: ", stage['Year'].max())


# We have 3 extra years of GDP data, so let's trim those off so the scatterplot has equal length arrays to compare (this is actually required by scatterplot)

# In[36]:


gdp_stage_trunc = gdp_stage[gdp_stage['Year']< 2012]
print(len(gdp_stage_trunc))
print(len(stage))


# In[40]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt

fig, axis = plt.subplots()
#Grid lines, Xticks, Xlabel, Ylabel

#axis.yaxis.grid(True)
axis.set_title('CO2 Emissions vs. GDP (per capita)', fontsize= 10)
axis.set_xlabel(gdp_stage_trunc['IndicatorName'].iloc[0], fontsize=10)
axis.set_ylabel(stage['IndicatorName'].iloc[0], fontsize=10)

X = gdp_stage_trunc['Value']  #gdp USA
Y = stage['Value']   #co2 USA

axis.scatter(X, Y)
plt.show()


# This doesn't look like a strong relationship. We can test this by looking at correlation.

# In[42]:


np.corrcoef(gdp_stage_trunc['Value'], stage['Value'])


# A correlation of 0.07 is pretty weak, but you'll learn more about correlation in the next course.

# You could continue to explore this to see if other countries have a closer relationship between CO2 emissions and GDP. Perhaps is it stronger for developing countries?

# In[ ]:




