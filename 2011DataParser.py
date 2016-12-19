import os
import csv
import pandas as pd

teams = ["arizona_cardinals","miami_dolphins","atlanta_falcons","minnesota_vikings","baltimore_ravens","new_england_patriots",
"buffalo_bills","new_orleans_saints","carolina_panthers","new_york_giants","chicago_bears","new_york_jets","cincinnati_bengals","oakland_raiders",
"cleveland_browns","philadelphia_eagles","dallas_cowboys","pittsburgh_steelers","denver_broncos","san_diego_chargers",
"detroit_lions","san_francisco_49ers","green_bay_packers","seattle_seahawks","houston_texans","st._louis_rams",
"indianapolis_colts","tampa_bay_buccaneers","jacksonville_jaguars","tennessee_titans","kansas_city_chiefs","washington_redskins"]

for team in teams:
    filename = "Madden-12-2011-data/" + team + '__madden_nfl_12_.xlsx'
    xls = pd.ExcelFile(filename)
    # print(xls.sheet_names)
    sheet_name = xls.sheet_names[0]
    sheet_name_arr = sheet_name.split(" ")
    team_name = sheet_name_arr[len(sheet_name_arr) - 1]
    df = xls.parse(sheet_name, index_col=None, na_values=['NA'])
    df['Team'] = team_name
    df.to_csv('test.csv', mode='a', header=False)

# for Filtering Test CSV
with open('test.csv','r') as fin:
    with open('2011Madden.csv','a') as fout:
        writer = csv.writer(fout, delimiter=',')            
        for row in csv.reader(fin, delimiter=','):
            # print(row)
            if (row[1] != 'Name' and len(row[1]) > 0):
                fullName = row[1].split(" ")
                first = ""
                middle = ""
                last = ""

                first = fullName[0]
                if (len(fullName) == 3) :
                    middle = fullName[1]
                    last = fullName[2]
                else:
                    last = fullName[1]

                writer.writerow([row[len(row)-1], middle + last, first, row[2], row[3]])
