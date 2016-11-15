from prettytable import PrettyTable

import http.client
import json
import sys


def get_league_table(league_name):
	connection = http.client.HTTPConnection('api.football-data.org')
	headers = { 'X-Auth-Token': '8b1b8ec671d745a0b7265401137fcf0e', 'X-Response-Control': 'minified' }
	connection.request('GET', '/v1/competitions/', None, headers )
	response = json.loads(connection.getresponse().read().decode())
	flag = False
	for i in response:
		if( i['league'] == league_name):
			league_id = str(i['id'])
			flag = True
			break
	else:
		print("Invalid League Code.. Please refer the Below List")
	
	if flag:
		connection.request('GET', '/v1/competitions/'+ league_id +'/leagueTable', None, headers )
		response = json.loads(connection.getresponse().read().decode())
		t = PrettyTable(['Team' ,'Games','GF','GA','GD', 'Points'])
		
		for i in response['standing']:
			t.add_row([ i['team'], i['playedGames'], i['goals'], i['goalsAgainst'], i['goalDifference'], i['points'] ])
		print (t)

def main():	
	if( sys.argv[1] == "League"):
		LeagueName = sys.argv[2]

		if( LeagueName is None ):
			print ("No league name entered !")
		else:
			get_league_table(LeagueName)

	else :
		print ("Invalid Argument: "+ sys.argv[1])


if __name__ == "__main__":
	main()