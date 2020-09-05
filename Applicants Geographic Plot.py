#!/usr/bin/env python
# coding: utf-8

# # Importing Folium for geographic plotting

# In[1]:


import folium
#defining location to be considered
map = folium.Map(location=[22.2771178,80.86467], zoom_start=5)


# In[2]:


#displaying map
map


# # Fetching Data for Count of Applicants basis City

# In[3]:


import connectors
import pandas as pd

conn = connectors.db_conn()
cur = conn.cursor()
sql_query = "select count(apid) as applicants , case when current_state = 'DELHI' then 'Delhi' else current_city end as region from applicants group by 2 order by 1 desc"
db_data = pd.read_sql_query(sql_query, conn)
print(db_data)
## Always close the connection
conn = None


# # Plotting fetched data on India Map and applying visualisation effects

# In[4]:


folium.Choropleth(geo_data= 'India.geojson', #loading geojson file uploaded
             data=db_data, # my dataset
             columns=['region', 'applicants'], # region is here for matching the geojson regions, applicants is the column that changes the color of regions
             key_on= 'feature.properties.NAME_2', # this path contains region in str type, this region should match with our region column
             fill_color='BuPu', 
             fill_opacity=0.7, 
             line_opacity=0.2,
             legend_name = 'Number of Applicants').add_to(map)


# In[5]:


map


# In[6]:


# We can see clearly that Delhi has the highest number of applicants(obviously) ,
#so now mapping applicants region wise within Delhi


# # Fetching number of applicants in Delhi - Region Wise

# In[7]:


conn = connectors.db_conn()
cur = conn.cursor()
sql_query = "select count(apid) as applicants , current_city as region from applicants where current_state = 'DELHI' group by 2 order by 1 desc LIMIT 9"
db_data1 = pd.read_sql_query(sql_query, conn)
print(db_data1)
## Always close the connection
conn = None


# In[8]:


#getting max value of applicants to set for heatmap
max_value = db_data1['applicants'][0]


# # Importing Delhi geojson from my Github

# In[9]:


import geopandas
map_data = geopandas.read_file('https://gist.githubusercontent.com/Prakhar-Chaurasia/b8bf5bba8f75e4a2a71672e432975045/raw/b5034c02314fad84a8a53f8e808bf8104cd9d4f3/map.geojson')


# In[10]:


print(map_data)
# We will need Dist_name


# In[11]:


#plotting an empty map
map_data.plot()


# In[12]:


# joining the geodataframe with data from DB
merged = map_data.set_index('Dist_Name').join(db_data1.set_index('region'))
#.head() returns the top 5(by default ) lines of the dataframe
merged.head()


# # Pre-requisites for plotting via matplotlib

# In[13]:


import matplotlib.pyplot as plt
# set a variable that will call whatever column we want to visualise on the map
variable = 'applicants'
# set the range for the choropleth
vmin, vmax = 0, max_value 
# create figure and axes for Matplotlib
fig, ax = plt.subplots(1, figsize=(10, 6))

#creating the map
merged.plot(column=variable, cmap='BuGn', linewidth=0.8, ax=ax, edgecolor='0.8')


# # Time for some beautification

# In[14]:


# remove the axis
ax.axis('off')
# add a title
ax.set_title('Delhi Applicants - Region Wise', fontdict={'fontsize': '25', 'fontweight' : '3'})
# create an annotation for the data source
ax.annotate('Source: Self', xy=(0.1, .08), xycoords='figure fraction', horizontalalignment='left', 
            verticalalignment='top', fontsize=12, color='#555555')

# Create colorbar as a legend
sm = plt.cm.ScalarMappable(cmap='BuGn', norm=plt.Normalize(vmin=vmin, vmax=vmax))
# empty array for the data range
sm._A = []
# add the colorbar to the figure
cbar = fig.colorbar(sm)
#saving our map as .png file.
fig.savefig('map_export.png', dpi=300)


# In[15]:


# Python program to read  
# image using matplotlib 
  
# importing matplotlib modules 
import matplotlib.image as mpimg 
import matplotlib.pyplot as plt 
  
# Read Images 
img = mpimg.imread('map_export.png') 
  
# Output Images 
plt.imshow(img , interpolation='nearest', aspect = 'auto')


# In[ ]:




