import requests
import json


test = ''
url1 = "https://***/jira/rest/api/2/issue/" + test
path = ''

payload = json.dumps({
  "fields": {
    "customfield_14474": "test"
  }
})
headers = { 'Content-Type': 'application/json'}


response = requests.request("PUT", url, headers=headers, data=payload,auth=('abhishek.bhandari', '****'))


print(response)

