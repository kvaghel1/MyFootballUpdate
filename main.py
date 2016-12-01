from prettytable import PrettyTable
from datetime import date
import time
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
def to_day_time(a):
	#2016-11-19T12:30:00Z
	day_list = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
	return (str(a[5:7])+ "/" + str(a[8:10]) + " " + day_list[datetime.date(int(a[0:4]),int(a[5:7]),int(a[8:10])).weekday()] + " " + str(int((a[11:13])) - 5 % 24)+str(a[13:16]) )

def get_team_id(team_name):
	team_dict = { 61:"che",
				 	64:"liv",
				  	354:"cry",
				   	62:"eve",
				    322:"hull",
				    65:"mci",
				    66: "mun",
				    343: "mid",
				    340:"sou",
				    70:"stk",
				    71:"sun",
				    72:"swa",
				    73:"tot",
				    346:"wat",
				    563:"whu",
				    74:"wba",
				    338:"lei"
					 }
	for key,value in team_dict.items():
		if value == team_name:
			return key


	
#--team
def show_team(team_name):
	team_id = get_team_id(team_name) 
	connection = http.client.HTTPConnection('api.football-data.org')
	headers = { 'X-Auth-Token': '8b1b8ec671d745a0b7265401137fcf0e', 'X-Response-Control': 'minified' }
	connection.request('GET','/v1/teams/'+str(team_id)+'/fixtures/', None, headers )
	response = json.loads(connection.getresponse().read().decode())
	count = 0
	for i in response["fixtures"]:
	#	print (count)
		if i["status"] == "TIMED":
			match_obj = i
#			print (i["matchday"]," --> ",i)
			t = PrettyTable(['Against','Opp - Position','H/A','Day - Time'])
			if match_obj['homeTeamId'] == team_id:
				t.add_row([match_obj['awayTeamName'], 'XX' , 'H' , to_day_time(match_obj['date'])])
			else:
				t.add_row([match_obj['homeTeamName'], 'XX' , 'A' , to_day_time(match_obj['date'])])

			match_obj = response["fixtures"][count+1]
			if match_obj['homeTeamId'] == team_id:
				t.add_row([match_obj['awayTeamName'], 'XX' , 'H' , to_day_time(match_obj['date'])])
			else:
				t.add_row([match_obj['homeTeamName'], 'XX' , 'A' , to_day_time(match_obj['date'])])

			match_obj = response["fixtures"][count+2]
			if match_obj['homeTeamId'] == team_id:
				t.add_row([match_obj['awayTeamName'], 'XX' , 'H' , to_day_time(match_obj['date'])])
			else:
				t.add_row([match_obj['homeTeamName'], 'XX' , 'A' , to_day_time(match_obj['date'])])

			match_obj = response["fixtures"][count+3]
			if match_obj['homeTeamId'] == team_id:
				t.add_row([match_obj['awayTeamName'], 'XX' , 'H' , to_day_time(match_obj['date'])])
			else:
				t.add_row([match_obj['homeTeamName'], 'XX' , 'A' , to_day_time(match_obj['date'])])

			match_obj = response["fixtures"][count+4]
			if match_obj['homeTeamId'] == team_id:
				t.add_row([match_obj['awayTeamName'], 'XX' , 'H' , to_day_time(match_obj['date'])])
			else:
				t.add_row([match_obj['homeTeamName'], 'XX' , 'A' , to_day_time(match_obj['date'])])
			print (t)
			break
		count+=1

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
