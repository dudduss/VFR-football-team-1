from lxml import html
import requests
import os
import csv

# years = [2011, 2012, 2013, 2014, 2015, 2016]
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

		url = 'http://www.spotrac.com/nfl/rankings/' + str(year) + '/average/' + team + '/'
		page = requests.get(url)
		tree = html.fromstring(page.content)

		players = tree.xpath('//a[@class="team-name"]/text()')
		salaries = tree.xpath('//span[@class="info"]/text()')
		positions = tree.xpath('//span[@class="rank-position"]/text()')

		numberSalaries = []

		#Converting string salaries to number salaries
		for salary in salaries:
			s = salary.replace("$","")
			s = s.replace(",","")
			s = s.replace(" ","")
			k = int(s)
			numberSalaries.append(k)

		filename = str(year) + ".csv"


		# os.makedirs(os.path.dirname(filename), exist_ok=True)

		with open(filename, 'a') as csvfile:
			
			filewriter = csv.writer(csvfile, delimiter = ',')

			# print(len(players))
			for i in range(len(players)):

				fullName = players[i].split(" ")
				first = ""
				middle = ""
				last = ""

				first = fullName[0]
				if (len(fullName) == 3) :
					middle = fullName[1]
					last = fullName[2]
				else :
					last = fullName[1]
				

				# print(first)
				# print(last)
				if (positions[i] in positionsDictionary) :
					filewriter.writerow([middle + last, first, positionsDictionary[positions[i]], numberSalaries[i], teamsDictionary[team]])






# Old analysis by position

"""
for year in years:
	for position in positions:

		# http://www.spotrac.com/nfl/rankings/2015/average/quarterback/veteran/
		
		# Send request and get page source from requested site
		url = 'http://www.spotrac.com/nfl/rankings/' + str(year) + '/average/' + position[0] + '/'
		# print(url)
		page = requests.get(url)
		tree = html.fromstring(page.content)

		# print(page)

		# finds specific CSS headers that come before required information (player names, salaries in this case)
		players = tree.xpath('//a[@class="team-name"]/text()')
		salaries = tree.xpath('//span[@class="info"]/text()')


		print(players)
		print(salaries)

		numberSalaries = []

		#Converting string salaries to number salaries
		for salary in salaries:
			s = salary.replace("$","")
			s = s.replace(",","")
			s = s.replace(" ","")
			k = int(s)
			numberSalaries.append(k)

		# Writing to a file--creates if it deosn't exist
		filename = str(year) + "/" + position[0] + ".csv"
		os.makedirs(os.path.dirname(filename), exist_ok=True)
		with open(filename, 'w+') as csvfile:
			
			filewriter = csv.writer(csvfile, delimiter = ',')

			print(len(players))
			for i in range(len(players)):
				first, last = players[i].split(" ")
				print(first)
				print(last)
				filewriter.writerow([last, first, numberSalaries[i], position[1]])

"""
