from bs4 import BeautifulSoup
import requests
import pandas as pd

# Make a page request using the requests module
START_URL = "https://en.wikipedia.org/wiki/Brown_dwarf"
response = requests.get(START_URL)

# Create a BeautifulSoup object
soup = BeautifulSoup(response.content, "html.parser")

# Get all the tables of the page using find_all() method of the beautifulsoup4 library
tables = soup.find_all("table", attrs={"class": "wikitable"})

# Create an empty list
scraped_data = []

# Loop through each table and extract the data
for table in tables:
    table_body = table.find("tbody")
    table_rows = table_body.find_all("tr")
    
    # Get all the <tr> tags from the table
    for row in table_rows:
        table_cols = row.find_all("td")
        
        # Use a for loop to take out all the <td> tags, we only need the text and we can strip any other characters using strip() method
        temp_list = []
        for col_data in table_cols:
            data = col_data.text.strip()
            temp_list.append(data)
        
        # Keep all the <td> rows in the empty list made earlier
        scraped_data.append(temp_list)

# Create an empty list to store star name, radius, mass and distance data
star_name = []
radius = []
mass = []
distance = []

# Loop through the row list to get the star name, radius, mass and distance data, and append this to respective lists
for i in range(0, len(scraped_data)):
    if len(scraped_data[i]) > 3:
        star_name.append(scraped_data[i][0])
        radius.append(scraped_data[i][1])
        mass.append(scraped_data[i][2])
        distance.append(scraped_data[i][3])

# Using the pandas library make a DataFrame from the above list
data = {'Star_name': star_name, 'Radius': radius, 'Mass': mass, 'Distance': distance}
brown_dwarfs_df = pd.DataFrame(data)

# Create a csv file from this list
brown_dwarfs_df.to_csv('brown_dwarfs_data.csv', index=True, index_label="id")