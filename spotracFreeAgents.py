from lxml import html
import requests
import os
import csv

# years = [2011, 2012, 2013, 2014, 2015, 2016]
# years = [2011, 2012, 2014, 2015, 2016]
years = [2016]
positions = [['quarterback' , 'QB'],
			 ['wide-receiver', 'WR'],
			 ['tight-end', 'TE'],
			 ['fullback', 'FB'],
			 ['tackle', 'T'],
			 ['left-tackle', 'LT'],
			 ['right-tackle', 'RT'],
			 ['guard', 'G'],
			 ['center', 'C'],
			 ['defensive-line', 'DL'],
			 ['defensive-end', 'DE'],
			 ['defensive-tackle', 'DT'],
			 ['linebacker', 'LB'],
			 ['outside-linebacker', 'OLB'],
			 ['inside-linebacker', 'ILB'],
			 ['cornerback', 'CB'],
			 ['safety', 'S']]

positionsDictionary = {
	'Quarterback' : 'QB',
	'Wide Receiver' : 'WR',
	'Tight End' : 'TE',
	'Running Back' : 'RB',
	'Fullback' : 'FB',
	'Tackle' : 'T',
	'Left Tackle' : 'LT',
	'Right Tackle' : 'RT',
	'Guard' : 'G',
	'Center' : 'C',
	'Defensive Line' : 'DL',
	'Defensive End' : 'DE',
	'Defensive Tackle' : 'DT',
	'Linebacker' : 'LB',
	'Outside Linebacker' : 'OLB',
	'Inside Linebacker' : 'ILB',
	'Cornerback' : 'CB',
	'Safety' : 'S',
	'Free Safety' : 'S',
	'Strong Safety' : 'S',
	'Kicker' : 'K',
	'Punter' : 'P',
	'Long Snapper' : 'LS',
	'Punt Returner' : 'PR',
	'Kick Returner' : 'KR'

}

teams = ['buffalo-bills', 'miami-dolphins', 'new-england-patriots', 'new-york-jets', 
		 'baltimore-ravens', 'cincinnati-bengals', 'cleveland-browns', 'pittsburgh-steelers',
		 'houston-texans', 'indianapolis-colts', 'jacksonville-jaguars', 'tennessee-titans', 
		 'denver-broncos', 'kansas-city-chiefs', 'oakland-raiders', 'san-diego-chargers',
		 'dallas-cowboys', 'new-york-giants', 'philadelphia-eagles', 'washington-redskins',
		 'chicago-bears', 'detroit-lions', 'green-bay-packers', 'minnesota-vikings', 
		 'atlanta-falcons', 'carolina-panthers', 'new-orleans-saints', 'tampa-bay-buccaneers',
		 'arizona-cardinals', 'los-angeles-rams', 'seattle-seahawks', 'san-francisco-49ers'
		]

teamsDictionary =  {
	'buffalo-bills' : 'BUF', 'miami-dolphins' : 'MIA', 'new-england-patriots' : 'NE', 'new-york-jets' : 'NYJ', 
	'baltimore-ravens' : 'BAL', 'cincinnati-bengals' : 'CIN', 'cleveland-browns' : 'CLE', 'pittsburgh-steelers' : 'PIT',
	'houston-texans' : 'HOU', 'indianapolis-colts' : 'IND', 'jacksonville-jaguars' : 'JAX', 'tennessee-titans' : 'TEN', 
	'denver-broncos' : 'DEN', 'kansas-city-chiefs' : 'KC', 'oakland-raiders' : 'OAK', 'san-diego-chargers' : 'SD',
	'dallas-cowboys' : 'DAL', 'new-york-giants' : 'NYG', 'philadelphia-eagles' : 'PHI', 'washington-redskins' : 'WAS',
	'chicago-bears' : 'CHI', 'detroit-lions' : 'DET', 'green-bay-packers' : 'GB', 'minnesota-vikings' : 'MIN', 
	'atlanta-falcons' : 'ATL', 'carolina-panthers' : 'CAR', 'new-orleans-saints' : 'NO', 'tampa-bay-buccaneers' : 'TB',
	'arizona-cardinals' : 'AZ', 'los-angeles-rams' : 'LA', 'seattle-seahawks' : 'SEA', 'san-francisco-49ers' : 'SF'

}

for year in years:
	for team in teams:

	#Send request
		url = 'http://www.spotrac.com/nfl/free-agents/' + str(year) + '/' + team + '/'
		# print(url)

		page = requests.get(url)
		tree = html.fromstring(page.content)


		players = tree.xpath('//tr/td//text()')
		lst = list(range(len(players)))
		# print(len(players))
		# print(players)

		# print(players)
		salaries = []
		numberSalaries = []
		names = []
		positions = []
		teams = []
		for i in lst:
			if players[i] in positionsDictionary.values():
				if players[i+3] in teamsDictionary.values():
					if  len(players[i+6]) > 2:
						names.append(players[i-1])
						salaries.append(players[i+6])
						positions.append(players[i])
						teams.append(players[i+3])

		#Converting string salaries to number salaries
		for salary in salaries:
			s = salary.replace("$","")
			s = s.replace(",","")
			s = s.replace(" ","")
			k = int(s)
			numberSalaries.append(k)

		# print(len(numberSalaries))


		with open(str(year) + ".csv", 'a') as csvfile:
			filewriter = csv.writer(csvfile, delimiter = ',')
			for i in range(len(names)):
				filewriter.writerow([names[i], numberSalaries[i], teams[i], positions[i]])




"""
for year in years:
	for position in positions:

		
		# Send request and get page source from requested site
		page = requests.get('http://www.spotrac.com/nfl/free-agents/' + str(year) + '/' + position[0] + '/')
		tree = html.fromstring(page.content)
		

		# finds specific CSS headers that come before required information (player names, salaries in this case)
		players = tree.xpath('//tr/td//text()')
		lst = list(range(len(players)))
		
		# using the full array players we iterate through it to isolate certain data columns
		names = []
		for i in lst:
			if players[i] == 'QB' or players[i] == 'WR' or players[i] == 'TE' or players[i] == 'FB' or players[i] == 'T' or players[i] == 'LT' or players[i] == 'RT' or players[i] == 'G' or players[i] == 'C' or players[i] == 'DL' or players[i] == 'DE' or players[i] == 'DT' or players[i] == 'LB' or players[i] == 'OLB' or players[i] == 'ILB' or players[i] == 'CB' or players[i] == 'S':
				names.append(players[i-1])
				i += 1
			else:
				i += 1
		
		teams = []
		for j in lst:
			if players[j] == 'QB' or players[j] == 'WR' or players[j] == 'TE' or players[j] == 'FB' or players[j] == 'T' or players[j] == 'LT' or players[j] == 'RT' or players[j] == 'G' or players[j] == 'C' or players[j] == 'DL' or players[j] == 'DE' or players[j] == 'DT' or players[j] == 'LB' or players[j] == 'OLB' or players[j] == 'ILB' or players[j] == 'CB' or players[j] == 'S':
				teams.append(players[j+3])
				j += 1
			else:
				j += 1

		salaries = []
		for k in lst:
			if players[k] == 'QB' or players[k] == 'WR' or players[k] == 'TE' or players[k] == 'FB' or players[k] == 'T' or players[k] == 'LT' or players[k] == 'RT' or players[k] == 'G' or players[k] == 'C' or players[k] == 'DL' or players[k] == 'DE' or players[k] == 'DT' or players[k] == 'LB' or players[k] == 'OLB' or players[k] == 'ILB' or players[k] == 'CB' or players[k] == 'S':
				salaries.append(players[k+6])
				k += 1
			else:
				k += 1


		# Writing to a file--creates if it deosn't exist
		with open(str(year) + "/" + position[0] + ".csv", 'w+') as csvfile:
			filewriter = csv.writer(csvfile, delimiter = ',')
			for i in range(len(names)):
				filewriter.writerow([names[i], salaries[i], teams[i], position[1]])


# Name, Avg Salary, Team that he went to
# loop throught and get the correct ones
# write a csv file for each position per year

"""









