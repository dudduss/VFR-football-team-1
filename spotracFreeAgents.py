from lxml import html
import requests
import os
import csv

years = [2011, 2012, 2013, 2014, 2015, 2016]
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










