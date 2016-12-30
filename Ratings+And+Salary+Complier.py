
# coding: utf-8

# In[28]:

import numpy as np
import regex as re
from datascience import *
import matplotlib
import matplotlib.pyplot as plots
import csv

teamsDictionary =  {
    'Bills' : 'BUF', 'Dolphins' : 'MIA', 'Patriots' : 'NE', 'Jets' : 'NYJ', 
    'Ravens' : 'BAL', 'Bengals' : 'CIN', 'Browns' : 'CLE', 'Steelers' : 'PIT',
    'Texans' : 'HOU', 'Colts' : 'IND', 'Jaguars' : 'JAX', 'Titans' : 'TEN', 
    'Broncos' : 'DEN', 'Chiefs' : 'KC', 'Raiders' : 'OAK', 'Chargers' : 'SD',
    'Cowboys' : 'DAL', 'Giants' : 'NYG', 'Eagles' : 'PHI', 'Redskins' : 'WAS',
    'Bears' : 'CHI', 'Lions' : 'DET', 'Packers' : 'GB', 'Vikings' : 'MIN', 
    'Falcons' : 'ATL', 'Panthers' : 'CAR', 'Saints' : 'NO', 'Buccaneers' : 'TB',
    'Cardinals' : 'AZ', 'Rams' : 'LA', 'Seahawks' : 'SEA', '49ers' : 'SF'
}


# In[13]:

def normalizeName(LastNames, FirstNames):
    fixednames=[]
    # print(LastNames)
    # print(FirstNames)
    for i in range(LastNames.size):
        rawF = FirstNames[i].lower()
        rawL = LastNames[i].lower()

        rawF = re.sub('[^A-Za-z0-9]+', '', rawF)
        rawL = re.sub('[^A-Za-z0-9]+', '', rawL)
        fixednames.append(rawF+rawL)
    return fixednames


# In[14]:

#Removes unnecessary data to expedite runtime, also changes table labels
def fixtable(tab):
    tabcut=tab.select("Team","First Name","Last Name","Position","Overall")
    positionfixed=tabcut.column("Position")
    overalltemp=tabcut.column("Overall")
    for i in range(positionfixed.size):
        if (positionfixed[i]=="FS" or positionfixed[i]=="SS"):
            positionfixed[i]="S"
        elif (positionfixed[i]=="HB"):
            positionfixed[i]="RB"
        elif(positionfixed[i]=="LE" or positionfixed[i]=="RE"):
            positionfixed[i]="DE"
        elif(positionfixed[i]=="LG" or positionfixed[i]=="RG"):
            positionfixed[i]="G"
        elif(positionfixed[i]=="LOLB" or positionfixed[i]=="ROLB"):
            positionfixed[i]="OLB"
        elif(positionfixed[i]=="MLB"):
            positionfixed[i]="ILB"
    tabcut.drop("Position","Overall").with_columns("Position",positionfixed,
                                                  "Overall",overalltemp)
    final=tabcut.where("Position",are.not_equal_to("K")
                ).where("Position",are.not_equal_to("P")
                       ).where("Position",are.not_equal_to("FB"))
    return final


# In[17]:

#Input a table containing separate columns for Last Name, First Name, and Overall ratings,
#And a table of salaries containing First Name, Last Name, Average Salary, Team, and Position. 
#Returns a Table combining both inputed tables. 
def ratings_salary(ratings, salary, year):
    salaryLnamearr=salary.column("Last Name")
    salaryFnamearr=salary.column("First Name")
    salaryarr=salary.column("Average Salary")
    teamarr=salary.column("Team")
    positionarr=salary.column("Position")
    fixednames=normalizeName(salary.column("Last Name"),salary.column("First Name"))
    fixedratingnames=normalizeName(ratings.column("Last Name"),ratings.column("First Name"))
    ratings=ratings.with_column("Fixed Name",fixedratingnames)
    LastName=make_array()
    FirstName=make_array()
    Overall=make_array()
    Salary=make_array()
    Team=make_array()
    Position=make_array()
    missedPlayers = []
    for i in range(salary.num_rows):
        ratingsdata=ratings.where("Fixed Name",are.containing(fixednames[i]))
        ratingsdatapos=ratingsdata.where("Position",are.equal_to(positionarr[i]))
        if (ratingsdata.num_rows==1):
            LastName=np.append(LastName,salaryLnamearr[i])
            FirstName=np.append(FirstName,salaryFnamearr[i])
            Overall=np.append(Overall,ratingsdata.column("Overall")[0])
            Salary=np.append(Salary,salaryarr[i]/1000)
            Team=np.append(Team,teamarr[i])
            Position=np.append(Position,positionarr[i])
        elif (ratingsdatapos.num_rows==1):
            LastName=np.append(LastName,salaryLnamearr[i])
            FirstName=np.append(FirstName,salaryFnamearr[i])
            Overall=np.append(Overall,ratingsdatapos.column("Overall")[0])
            Salary=np.append(Salary,salaryarr[i]/1000)
            Team=np.append(Team,teamarr[i])
            Position=np.append(Position,positionarr[i])
        else:
            missedPlayers.append((fixednames[i]))

    Ratings_Salary=Table().with_columns("Last Name",LastName,"First Name",FirstName,
                                        "Position",Position,
                                       "Overall",Overall,"Salary",Salary,"Team",Team)
    def addyear(tbl,yr):
    	yeararr=make_array()
    	for _ in range(tbl.num_rows):
    		yeararr=np.append(yeararr,yr)
    	return tbl.with_column("Year",yeararr)
    Ratings_Salary=addyear(Ratings_Salary,year)
    return Ratings_Salary




# In[22]:

ratings2016=Table.read_table('Madden Ratings/madden_nfl_17_-_full_player_ratings.csv')
ratings2015=Table.read_table('Madden Ratings/madden_nfl_16_-_full_player_ratings.csv')
ratings2014=Table.read_table('Madden Ratings/madden_nfl_15_-_full_player_ratings.csv')
ratings2013=Table.read_table('Madden Ratings/madden_nfl_25_-_full_player_ratings.csv')
ratings2012=Table.read_table('Madden Ratings/madden_nfl_13_-_full_player_ratings.csv')
ratings2011=Table.read_table('Madden Ratings/madden_nfl_12_-_full_player_ratings.csv')



# In[23]:

ratingsfixed2016=fixtable(ratings2016)
ratingsfixed2015=fixtable(ratings2015)
ratingsfixed2014=fixtable(ratings2014)
ratingsfixed2013=fixtable(ratings2013)
ratingsfixed2012=fixtable(ratings2012)
ratingsfixed2011=fixtable(ratings2011)


# In[24]:

salary2016=Table.read_table('salary-data/2016.csv')
salary2015=Table.read_table('salary-data/2015.csv')
salary2014=Table.read_table('salary-data/2014.csv')
salary2013=Table.read_table('salary-data/2013.csv')
salary2012=Table.read_table('salary-data/2012.csv')
salary2011=Table.read_table('salary-data/2011.csv')


# In[25]:

ratingsandsalary2016=ratings_salary(ratingsfixed2016,salary2016,2016)
ratingsandsalary2015=ratings_salary(ratingsfixed2015,salary2015,2015)
ratingsandsalary2014=ratings_salary(ratingsfixed2014,salary2014,2014)
ratingsandsalary2013=ratings_salary(ratingsfixed2013,salary2013,2013)
ratingsandsalary2012=ratings_salary(ratingsfixed2012,salary2012,2012)
ratingsandsalary2011=ratings_salary(ratingsfixed2011,salary2011,2011)





# print(Projections2016)

projections = [ratingsandsalary2016, ratingsandsalary2015, ratingsandsalary2014, ratingsandsalary2013, ratingsandsalary2012, ratingsandsalary2011]

filename = "ratings-and-salary.csv"
with open(filename, 'w') as csvfile :
    filewriter = csv.writer(csvfile, delimiter = ',')

    filewriter.writerow(["Last Name" , "First Name" , "Position" , "Overall" , "Salary" , "Team","Year" ])

    for projection in projections:
        for row in projection.rows:
            # print(row)
            filewriter.writerow(
                [row[0], row[1], row[2], row[3], row[4], row[5],row[6]])



