#!/usr/bin/env python3
import os, json, requests, urllib.parse

CONTACTS_URL = os.environ.get('LUCOS_CONTACTS', "https://contacts.l42.eu/")
LUCOS_HEADERS={'AUTHORIZATION':"key "+os.environ.get('LUCOS_CONTACTS_API_KEY')}


# Search for an existing match in lucos, based on the order of items in the accounts arround
#
# Returns the agentid as a string, if a match is found.  Otherwise returns None
def matchContact(accounts, primaryName):
	for account in accounts:
		resp = requests.get(CONTACTS_URL+"identify", headers=LUCOS_HEADERS, params=account, allow_redirects=False)
		if resp.status_code == 302:
			return resp.headers['Location'].replace("/agents/","")
		if resp.status_code == 409:
			print("Conflict for "+primaryName+" - "+account['type'])
		if resp.status_code >= 500:
			resp.raise_for_status()
	return None

def newContact(name):
	resp = requests.post(CONTACTS_URL+"agents/add", headers=LUCOS_HEADERS, allow_redirects=False, data={'name': name})
	if resp.status_code == 302:
		return resp.headers['Location'].replace("/agents/","")
	raise Exception("Unexpected status code "+str(resp.status_code)+" "+resp.reason+": "+resp.text)



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

				accounts = [
					{
						"type":"facebook",
						"userid":userid,
					},
					{
						"type":"name",
						"name": name,
					}
				]
				agentid = matchContact(accounts, name)
				if not agentid:
					agentid = newContact(name)
				print(" --- " + str(agentid))
				resp = requests.post(CONTACTS_URL+'agents/'+agentid+"/accounts", headers=LUCOS_HEADERS, allow_redirects=False, json=accounts)
				resp.raise_for_status()