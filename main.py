import scrape_script as scrape
import pymongo
import pandas as pd

#########################

conn = 'mongodb://localhost:27017'

client = pymongo.MongoClient(conn)

db = client.f1_db

########################

years_data = scrape.scrape()

##########################

years_dict = {}
for year in years_data:
    year_d = years_data[year][0].to_dict()
    year_dict = {}
    for column in year_d:
        row_list = []
        for row in year_d[column]:
            row_list.append(year_d[column][row])
        year_dict[column] = row_list
    years_dict[year] = year_dict

#####################################

db.drop_collection('race_results')
for year in years_dict:
    del years_dict[year]['Unnamed: 0']
    del years_dict[year]['Unnamed: 7']
    year_d = pd.DataFrame(years_dict[year]).to_dict(orient='records')
    for race in year_d:
        race['year'] = int(year)
        db.race_results.insert_one(race)

###############################

year = str(input('what year would you like to search?'))

races = db.race_results.find({'year':year})

for race in races:
    print(race)