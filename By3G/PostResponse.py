
import requests
import sys
 
API_ENDPOINT = "http://164.115.43.87:8080/postholodata"
 
API_KEY = sys.argv[1]+"@"+sys.argv[2];

data = {'auth':API_KEY }
 

r = requests.post(url = API_ENDPOINT, data = data)
 
pastebin_url = r.text
print("The pastebin URL is:%s"%pastebin_url)
