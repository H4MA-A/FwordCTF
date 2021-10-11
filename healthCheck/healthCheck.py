from pwn import *
from os import listdir
from os.path import isfile, join
from discord_webhook import DiscordWebhook
import json, logging, requests, schedule, time 


def check(task):
	if task["type"] == "web":
		link = task['server']+":"+task["port"]
		try:
			r = requests.get(link)
			if r.status_code == 200:
				if task["out"] in r.text:
					return 1
				else:
					return 0
			else:
				return 0
		except:
			return 0
	elif task["type"] == "service":
		try:
			r = remote(task["server"],task["port"])
			r.send(task["int"])
			data = r.recv()
			if data in task["out"]:
				return 1
			return 0
		except:
			return 0
	pass
def jsonParser(path):
	onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
	for f in onlyfiles:
		jsonFile = json.load(open(join(path, f)))
		if check(jsonFile):
			logging.info(jsonFile["name"]+" is running with no problems")
		else:
			message = "@everyone \n**" + jsonFile["name"] + " is Down** \ncategory: " + jsonFile["type"] + "\nLink: " + jsonFile["server"] + ":" + jsonFile["port"]
			try:
				webhook = DiscordWebhook(url='###DISCORD_WEBHOOK###', content=message)
				response = webhook.execute() 
			except:
				logging.info("problem with the webhook")
				print("[-] problem with the webhook")
	return 0
def launch():
	jsonParser("./tasks")
	return 1


schedule.every(180).seconds.do(launch)
while 1:
	schedule.run_pending()
	time.sleep(10)