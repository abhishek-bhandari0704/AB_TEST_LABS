import requests
from datetime import datetime, timedelta
import time
from jira.client import JIRA
import json
import pandas as pd
import xlsxwriter


jira_server = 'https://***/jira/'
jira_server = {'server': jira_server}
jira = JIRA(options=jira_server, basic_auth=('abhishek.bhandari@***.com', '****'))
j_ticket_assign=''

'''Parameters'''
project_key='ADVTESTAU'
build='Cadence - 05/04/2022 #Build 2022.FS2.12.1'
#build='System Admin (sa) user lock'
Epic_Name='FR: '+build
no_of_tasks_epic=['HRM','FIN','FRWK','PB','Architecture_Activities','Build_Promotion_Activities']
#no_of_tasks_epic=['FIN','Build_Promotion_Activities']
#no_of_tasks_epic=['HRM','FIN','PB']
#no_of_sub_tasks=['Pipeline Analysis','No of Test Cases Impacted']
no_of_sub_tasks=['REG:Pipeline-Execution','REG:Failure-Analysis','REG:Manual-Validation','STQA:Pipeline-Execution','STQA:Failure-Analysis','STQA:Manual-Validation']
#no_of_sub_tasks=['REG:Pipeline-Execution','REG:Failure-Analysis','REG:Manual-Validation']


'''Creating Epic'''
try:
 print("Creating feature Epic")
 epic_new_issue = jira.create_issue(project=project_key, summary=str(Epic_Name),description=str(Epic_Name), issuetype={'name': 'Epic'},customfield_10851=str(Epic_Name))
 print("Feature Epic: ",epic_new_issue.key)
except:
  print("Epic creation failed")
  exit()



'''Creating Task and Subtasks'''
for x in no_of_tasks_epic:
 try:    
    print(x)
    task_new_issue = jira.create_issue(project=project_key, summary=str(x+' - '+build),description=str(x+' - '+build), issuetype={'name': 'Task'},customfield_10850=str(epic_new_issue.key))
    print("Task Key: ",task_new_issue.key)
    if x in('HRM','FIN','FRWK','PB'):
    #if x in ('FIN','HRM','PB'):
        for y in no_of_sub_tasks:
            print(y)
            new_issue = jira.create_issue(project=project_key,parent={'key': task_new_issue.key}, summary=str(y+' - '+build),description=str(y+' - '+build), issuetype={'name': 'Analyze'})
            print("Subtask Key: ",new_issue.key)  
 except:
    print("Issue creation failed")
    continue

exit()

'''Cadence issue creation completed'''


df = pd.read_excel("TestSet.xlsx")
print(df)

results=[]

for row in df.itertuples():
 print(row.Project,row.Summary,row.Description)
 try:
  print(" in the try block")
  new_issue = jira.create_issue(project=row.Project, summary=str(row.Summary),description=str(row.Description), issuetype={'name': 'Test Set'},customfield_14474="S",customfield_14475="S")
  print(new_issue.key)
  Link_Url='https://***/jira/rest/raven/1.0/api/testset/'+new_issue.key+'/test/'
  print(Link_Url)
  payload = json.dumps({"add": [str(row.LinkID).strip()]})
  payload_test = json.dumps({"add": ["adv-123"]})
  print(payload,payload_test)
  headers = {'Content-Type': 'application/json'}
  response = requests.request("POST", Link_Url, auth=('abhishek.bhandari@***.com', '***'), headers=headers, data=payload)
  results.append([row.Project,row.Summary,row.Description,str(new_issue.key),str(row.LinkID),"Success"])

 except Exception as e:
  print("in exception block")
  print(" \n\n JIRA Issue creation Failed - Job Cancelled.\n\n")
  results.append([row.Project,row.Summary,row.Description,str(new_issue.key),str(row.LinkID),"Failed"])
  continue


Testset_df=pd.DataFrame(results, columns = ["Project","TS_Summary","TS_Desc","TS_Key","TC_LinkedKey","Status"]) 




''' SAVING data to EXCEL and CSV '''
filename='Testset_Results6.xlsx'
writer = pd.ExcelWriter(filename, engine='xlswriter')
#df1.to_excel(writer,sheet_name = 'Rawdata', index=False)
Testset_df.to_excel(writer,sheet_name = 'TestSet', index=False)
writer.save()

#customfield_15452 -- applicationname
#customfield_14474--S
#customfield_14475--S