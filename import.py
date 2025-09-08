#!/usr/bin/env python3
import os, json, requests, urllib.parse

CONTACTS_URL = os.environ.get('LUCOS_CONTACTS', "https://contacts.l42.eu/")
LUCOS_HEADERS={'AUTHORIZATION':"key "+os.environ.get('KEY_LUCOS_CONTACTS')}

for filename in os.listdir('data'):
	with open('data/'+filename) as fp:
		data = json.load(fp)
		for month in data['data']['viewer']['all_friends_by_birthday_month']['edges']:
			print(month['node']['month_name_in_iso8601'])
			for person_edge in month['node']['friends']['edges']:
				person = person_edge['node']
				name = person['name']
				userid = person['id']
				username = person['profile_url'].rsplit('/', 1)[-1]
				day_of_birth = person['birthdate']['day']
				month_of_birth = person['birthdate']['month']
				year_of_birth = person['birthdate']['year']
				print("  - "+name+" ("+username+"/"+userid+") "+str(day_of_birth)+"/"+str(month_of_birth)+"/"+str(year_of_birth))

				data = {"identifiers":[
					{
						"type":"facebook",
						"userid":userid,
						"username": username,
					},
					{
						"type":"name",
						"name": name,
					}
				],
				"date_of_birth":{
					'day': day_of_birth,
					'month': month_of_birth,
					'year': year_of_birth,
				}}
				resp = requests.post(CONTACTS_URL+'people/import', headers=LUCOS_HEADERS, allow_redirects=False, json=data)
				resp.raise_for_status()