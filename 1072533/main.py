import requests  # for downloading the csv
import pandas as pd  # for dataframes
import matplotlib.pyplot as plt  # for graphs
import sqlite3 as sql  # for sql database save

# to download the csv from the site.The url was taken from the site when you hover the csv download button
url = 'https://data.buffalony.gov/api/views/2cjd-uvx7/rows.csv?accessType=DOWNLOAD'
r = requests.get(url, allow_redirects=True)

# to copy contents into the file
open('Monthly_Recycling_and_Waste_Collection_Statistics.csv', 'wb').write(r.content)

# making a panda dataframe
plz = pd.read_csv(
    "Monthly_Recycling_and_Waste_Collection_Statistics.csv",
    header=0,
    parse_dates=["DATE"]
)

# grouping by and creating the csvs
plzWaste = plz.groupby(plz.DATE.dt.year)["TOTAL (IN TONS)"].sum()
# print(plzWaste) #just for testing the csvs
plzWaste.to_csv("WastePerYEAR.csv", index=True)

plzWasteTYPES = plz.groupby("TYPE")["TOTAL (IN TONS)"].sum()
# print(plzWasteTYPES)
plzWasteTYPES.to_csv("ValuesPerTYPE.csv", index=True)

plzWasteTOPMONTHS = plz.sort_values(by=["TOTAL (IN TONS)"], ascending=False).iloc[0:5]
# print(plzWasteTOPMONTHS)
plzWasteTOPMONTHS.to_csv("TopMONTHS.csv", index=False)

# graphing graphs
plt.rcParams["figure.figsize"] = (19.2, 10.8)  # change the resolution because some text didn't fit
plzWaste.plot(x='DATE', y='TOTAL (IN TONS)', kind='line')  # creating the plots
plt.savefig('WastePerYear.png')  # saving all the graphs as pngs for better viewing
plt.show()

plzWasteTYPES.plot(x='TYPE', y='TOTAL (IN TONS)', kind='bar')
plt.ylim(0, 250000)  # setting y boundaries to better show the results
plt.text(1.745, 245000, str(int(1074974)))  # showing the outlier's result
plt.text(4.9, 1000, str(int(130)))  # -||-
plt.savefig('WastePerType.png')
plt.show()

plzWasteTOPMONTHS.plot(x='MONTH', y='TOTAL (IN TONS)', kind='bar')
plt.ylim(11000, 13000)  # setting y boundaries again to better show res
plt.text(-0.071, 10860, str(int(2013)))  # showing the year manually because I couldn't in the plot
plt.text(0.929, 10860, str(int(2014)))
plt.text(1.929, 10860, str(int(2014)))
plt.text(2.929, 10860, str(int(2014)))
plt.text(3.929, 10760, str(int(2015)))
plt.savefig('WasteTopMonths.png')
plt.show()

# conn to sql using sqlite
conn = sql.connect('waste.db')  # creating the database
plz.to_sql('waste', conn, if_exists='replace')  # adding the main csv
plzWaste.to_sql('wastePerYear', conn, if_exists='replace')  # adding all the groups
plzWasteTYPES.to_sql('wasteTYPES', conn, if_exists='replace')
plzWasteTOPMONTHS.to_sql('wasteTopMonths', conn, if_exists='replace')
