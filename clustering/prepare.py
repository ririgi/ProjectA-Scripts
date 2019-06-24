import warnings
warnings.filterwarnings("ignore")

import os

import pandas as pd
import numpy as np

from ip2geotools.databases.noncommercial import DbIpCity

value = lambda x: x.strip("[]").replace("'", "").split(", ")
converters={"actiontaken": value,
			"devicetype": value,
			"deviceos": value,
			"osversion": value,
			"ipaddress": value,
			"browsertype": value,
			"connectivitytype": value,
			"screensize": value,
			"videoquality": value,
			"sitedomain": value,
			"devicename": value,
			"browserversion": value}

def getUnique(df, col):
	df = df[col].apply(tuple)
	unique = df.unique()
	unique = list(set([a for t in unique for a in t]))
	unique = [word.replace('nan', 'nan_'+col) for word in unique]
	return unique

def prepareDataDevice(data_dir, filename):
	cols = ["gigyaid", "devicetype", "deviceos", "browsertype", "screensize", "videoquality"]
	device_cols = ["devicetype", "deviceos", "browsertype", "screensize", "videoquality"]
	df = pd.read_csv(os.path.join(data_dir, filename), dtype = str, low_memory = False, usecols = cols, converters = converters)

	feature_cols = []
	for col in device_cols:
		x = getUnique(df, col)
		feature_cols.extend(x)
	print(df.columns)
	new_df = pd.DataFrame(index = df.gigyaid, columns = feature_cols)
	df = df.set_index("gigyaid")
	for user_id in df.index.unique():
		user = df.loc[user_id]
		for col in device_cols:
			a = user[col]
			a = [word.replace('nan', 'nan_'+col) for word in a]
			for b in a:
				new_df.loc[user_id][b] = 1

	new_df.fillna(0, inplace=True)
	return(new_df)

def ipToCity(ipaddresses):
	locations = []
	for ip in ipaddresses:
		try:
			response = DbIpCity.get(ip, api_key='free')
			loc = str(response.city) + "-" + str(response.region)
			locations.append(loc)
			print(ip, loc)
		except:
			pass
	return locations

def prepareLocation(data_dir, filename,  outfile):
	cols = ["gigyaid", "ipaddress"]
	df = pd.read_csv(os.path.join(data_dir, filename), dtype = str, low_memory = False, usecols = cols, converters = converters)
	df["location_city"] = df["ipaddress"].apply(lambda x: ipToCity(x))
	df.to_csv(os.path.join(outfile))
	print("Done converting to location")
	print("\n\n")

if __name__ == '__main__':
	# prepareLocation("../data/iWant/processed/preliminary", "september_2018.csv", "september_2018_location.csv")
	# prepareLocation("../data/iWant/processed/preliminary", "october_2018.csv", "october_2018_location.csv")
	prepareLocation("../data/iWant/processed/preliminary", "november_2018.csv", "november_2018_location.csv")
	prepareLocation("../data/iWant/processed/preliminary", "2019-03-03.csv", "2019-03-03_location.csv")
	prepareLocation("../data/iWant/processed/preliminary", "2019-01-06.csv", "2019-01-06_location.csv")
	prepareLocation("../data/iWant/processed/preliminary", "2018-12-09.csv", "2018-12-09_location.csv")
	prepareLocation("../data/iWant/processed/preliminary", "2019-02-03.csv", "2019-02-03_location.csv")

