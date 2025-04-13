import pandas as pd

url = "https://en.wikipedia.org/wiki/List_of_association_football_stadiums_by_capacity"
tables = pd.read_html(url)

# Inspect how many tables were found:
print("Number of tables found:", len(tables))

# For example, if the first table contains the stadium list:
stadium_table = tables[0]

# Show the first few rows to inspect the columns:
print(stadium_table.head())