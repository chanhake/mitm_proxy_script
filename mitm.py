#####
# Name: Grade Changer
# Authors: Chandler Hake, Ethan Banks
# Version: 2
# Description: This script is used with MITMproxy and can change
# Canvas grades to whatever you wish (in this case 1000)
#####
import mitmproxy
from mitmproxy import ctx
import json

#Changes grades on Canvas
def response(flow: mitmproxy.http.HTTPFlow) -> None:
	flag = 0
	if "fit.instructure.com" in flow.request.url:
		try:
			data = json.loads(flow.response.content)
			#Changes grades in grade tab when reloaded
			data["enrollments"][0]["computed_current_score"] = 1000
			flow.response.content = bytes(json.dumps(data), "utf-8")
		except:
			try:
				data = json.loads(flow.response.content)
				try:
					for i in data:
						try:
							#Changes current score header
							i["grades"]["current_score"] = 1000
						except:
							try:
								#Changes outside current score and stays when reloaded
								i["enrollments"][0]["computed_current_score"] = 1000
								ctx.log.alert("Grade Changed!") 
								flag = 1
							except:
								ctx.log.alert("Nothing Found in this Response!")
				except:
					ctx.log.alert("Nothing Found in this Response!")

				#Only send response when changed
				if flag == 1:
					flow.response.content = bytes(json.dumps(data), "utf-8")
			except:
				ctx.log.alert("Nothing Found in this Response!")

