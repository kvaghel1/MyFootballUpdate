from prettytable import PrettyTable
from datetime import date

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

def get_team_id(team_name):
	connection = http.client.HTTPConnection('api.football-data.org')
	headers = { 'X-Auth-Token': '8b1b8ec671d745a0b7265401137fcf0e', 'X-Response-Control': 'minified' }
	
	#total teams: 1 to 851 	
	for i in range(1,852):
		print (i)
		connection.request('GET', '/v1/teams/'+str(i)+'/', None, headers )
		response = json.loads(connection.getresponse().read().decode())
		print (response)
		if(response['shortName'].upper() == team_name.upper()):
			return i
	
#--team
def show_team(team_name):
	print (get_team_id(team_name))

def to_day_time(a):
	#2016-11-19T12:30:00Z
	day_list = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
	return (day_list[datetime.date(int(a[0:4]),int(a[5:7]),int(a[8:10])).weekday()] + " " + str(int((a[11:13])) - 5 % 24)+str(a[13:16]) )

def show_next_game(league_name):
	league_id = get_league_id(league_name)

	connection = http.client.HTTPConnection('api.football-data.org')
	headers = { 'X-Auth-Token': '8b1b8ec671d745a0b7265401137fcf0e', 'X-Response-Control': 'minified' }

	connection.request('GET', '/v1/competitions/'+str(league_id)+'/fixtures', None, headers )
	
	response = json.loads(connection.getresponse().read().decode())
	t = PrettyTable(['Home Team' ,'Away Team','Day - Time'])
	for i in response['fixtures']:
		if(i['status'] == "TIMED"):
			t.add_row([i['homeTeamName'],  i['awayTeamName'] ,to_day_time(i['date'])] )
	print (t)

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

def show_help():
	help_message = "Please find the following commands for reference: \n"
	t = PrettyTable(["Command" , "Description"])
	t.add_row([ "--nextweek LEAGUE_CODE " , " Show the next fixtures of the league" ])
	t.add_row([ "--league LEAGUE_CODE " , " Show the current league standings of the league" ])
	print (t)


def main():
	if (len(sys.argv) == 1):
		print ("No argument Entered !")
		print ("use --help for the list of command \n")

	elif( sys.argv[1].upper() == "--HELP"):
		show_help()

	elif( sys.argv[1].upper() == "--LEAGUE"):
		if (len(sys.argv) < 3):
			print ("No league name entered !")
			print ("use --help for the list of command\n")
		else:
			LeagueName = sys.argv[2]
			show_league_table(LeagueName)

	elif( sys.argv[1].upper() == "--NEXTWEEK"):
		if (len(sys.argv) < 3):
			print("No league entered !")
			print ("use --help for the list of command\n")
		else:
			LeagueName = sys.argv[2]
			show_next_game(LeagueName)

	elif( sys.argv[1].upper() == "--TEAM"):
		if (len(sys.argv) < 3):
			print("No team entered !")
			print ("use --help for the list of command\n")
		else:
			TeamName = sys.argv[2]
			show_team(TeamName)
	else :
		print ("Invalid Argument: "+ sys.argv[1])
		print ("use --help for the list of command\n")


if __name__ == "__main__":
	main()
