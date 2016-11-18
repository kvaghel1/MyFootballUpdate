from prettytable import PrettyTable

import http.client
import json
import sys
import datetime

def get_league_id(league_name):
	connection = http.client.HTTPConnection('api.football-data.org')
	headers = { 'X-Auth-Token': '8b1b8ec671d745a0b7265401137fcf0e', 'X-Response-Control': 'minified' }
	connection.request('GET', '/v1/competitions/', None, headers )
	response = json.loads(connection.getresponse().read().decode())
	flag = False

	for i in response:
		if( i['league'] == league_name.upper()):
			league_id = str(i['id'])
			return league_id
	else:
		print ("Invalid League Name: Please refer the below list- \n"+"ID: league(Description)" )
		list_of_competitions = "424: EC(European Championships France 2016) \n" \
		+ "426: PL(Premier League 2016/17) \n" +\
		 "427: ELC(Championship 2016/17) \n" + \
		 "428: EL1(League One 2016/17) \n" +\
		"430: BL1(1. Bundesliga 2016/17) \n" +\
		"431: BL2(2. Bundesliga 2016/17) \n" +\
		"432: DFB(DFB-Pokal 2016/17) \n" +\
		"433: DED(Eredivisie 2016/17) \n" +\
		"434: FL1(Ligue 1 2016/17) \n" +\
		"435: FL2(Ligue 2 2016/17) \n" +\
		"436: PD(Primera Division 2016/17) \n"+\
		"437: SD(Liga Adelante 2016/17)\n" +\
		"438: SA(Serie A 2016/17) \n"+\
		"439: PPL(Primeira Liga 2016/17) \n"+\
		"440: CL(Champions League 2016/17) \n" 
		print(list_of_competitions)


def show_next_game(league_name):
	league_id = get_league_id(league_name)

	connection = http.client.HTTPConnection('api.football-data.org')
	headers = { 'X-Auth-Token': '8b1b8ec671d745a0b7265401137fcf0e', 'X-Response-Control': 'minified' }

	connection.request('GET', '/v1/competitions/'+str(league_id)+'/fixtures', None, headers )
	
	response = json.loads(connection.getresponse().read().decode())
	
	for i in response['fixtures']:
		if(i['status'] == "TIMED"):
			print (i['homeTeamName'] + " v/s " + i['awayTeamName'] + " "+i['date'] + "\n" )




def show_league_table(league_name):
	league_id = get_league_id(league_name)
	if( league_id is not None):
		connection = http.client.HTTPConnection('api.football-data.org')
		headers = { 'X-Auth-Token': '8b1b8ec671d745a0b7265401137fcf0e', 'X-Response-Control': 'minified' }

		connection.request('GET', '/v1/competitions/'+ league_id +'/leagueTable', None, headers )
		response = json.loads(connection.getresponse().read().decode())
		t = PrettyTable(['Team' ,'Games','GF','GA','GD', 'Points'])
		
		for i in response['standing']:
			t.add_row([ i['team'], i['playedGames'], i['goals'], i['goalsAgainst'], i['goalDifference'], i['points'] ])
		print (t)

def main():
	if (len(sys.argv) == 1):
		print ("No argument Entered !")

	elif( sys.argv[1].upper() == "LEAGUE"):
		LeagueName = sys.argv[2]

		if( LeagueName is None ):
			print ("No league name entered !")
		else:
			show_league_table(LeagueName)
	elif( sys.argv[1].upper() == "NEXTWEEK"):
		LeagueName = sys.argv[2]

		if( LeagueName is None):
			print("No league entered !")
		else:
			show_next_game(LeagueName)

	else :
		print ("Invalid Argument: "+ sys.argv[1])


if __name__ == "__main__":
	main()
