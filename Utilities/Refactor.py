    
import json
import os
from os import path, mkdir

import requests

filename = "C:\\Test.robot"
dir_path_list = filename.split('\\')
folder = dir_path_list.pop()
fld = folder.split('.robot')[0]
parent_directory = '\\'.join(dir_path_list) + "\\"
tags_count = 0
filename1 = filename.split("\\")[-1]
jfp = []
path_issue = []
test_case_flag = False
#Function to get common section
def get_common_section(file_name):
    common = ''
    myfile = open(file_name, "r")
    for line in myfile.readlines():
        if line.strip().startswith("*") and "test" in line.lower() and "case" in line.lower():
            test_case_flag = True
        if line.strip().startswith("*") and "test" not in line.lower() and "case" not in line.lower():
            test_case_flag = False
        if not (test_case_flag):
            common += line
    return common

#Function to get the test cases
def get_test_cases(file_name):
    tc_name = []
    tags = []
    test_cases = []
    tc_content = []
    content = ''
    tags_line = ''
    tcname = ''
    myfile = open(file_name, "r")
    for line in myfile.readlines():
        line = line.replace("\t", "    ")
        if line.strip().startswith("*") and "test" not in line.lower() and "case" not in line.lower():
            test_case_flag = False
        if (test_case_flag):
            if not line.startswith("  ") and not line.strip().startswith("#"):
                if len(line.strip()) > 0:
                    tc_name.append(line.strip())
                    tcname = line.strip()
                    if len(content) > 0:
                        tc_content.append(content)
                        content = ''
            if line.startswith("  ") or line.strip().startswith("#"):
                global tags_count
                if "[tags]" in line.lower():
                    tags_count += 1
                    tags.append(tcname)
                content += line
        if line.strip().startswith("*") and "test" in line.lower() and "case" in line.lower():
            test_case_flag = True
    if len(content) > 0:
        tc_content.append(content)
        content = ''
        # if len(tags_line.strip()):
        #     # print "No Tags found for the Test Case:" + str(tc_name)
        #     print len(tc_content)
    if len(tags) != len(tc_name):
        for naam in [x for x in tc_name if x not in tags]:
            print "No Tags specified for test case : " + naam
    for i in range(len(tc_name)):
        if len(tc_content) == len(tc_name):
            test_cases.append([tc_name[i], tc_content[i]])
        else:
            test_cases.append([tc_name[i], tc_content[i + 1]])
            # print(len(tc_name), len(tc_content), len(test_cases))
    return test_cases

#Function to update the JIRA-Text1 path

#
def jira_path_update(issue, path1, user, passw):

    url = "https://***/jira/rest/api/2/issue/" + issue
    print(url)

    payload = json.dumps({

        "update": {

            "customfield_14474": [

                {

                    "set": path1

                }

            ]

        }

    })
    headers = {'Content-Type': 'application/json'}
    #payload = '"update": {"customfield_14474": [{"set": "Test Compo"}]}'

    #print payload

    response = requests.request("PUT", url, headers=headers, data=payload, auth=(user, passw))

    print(response)



comm = get_common_section(filename)
test_cases_list = get_test_cases(filename)
# myfile = open(filename, "r")
# line_num = 0
# pattern = "[Tags]"
# for line in myfile.readlines():
#     line_num += 1
#     if line.find(pattern) >= 0:
#         print "Tags found at Line Number" + ":- " + str(line_num)
#     myfile.close()
if len(test_cases_list) > 1:
    if str(tags_count) == str(len(test_cases_list)):
        for test_cases in test_cases_list:
            # file_paths = ''
            file_cont = comm + '\n*** Test Cases ***\n' + test_cases[0] + '\n' + test_cases[1]
            new_file_name = filename.split(".robot")[0] + '_' + test_cases[0] + '.robot'
            dir_path_list1 = new_file_name.split('\\')
            folder1 = dir_path_list1.pop()
            present_directory = '\\'.join(dir_path_list) + "\\" + "Refactored"
            sub_dir = present_directory + "\\" + fld
            jira_file_path = "4.0_Test_Automation" + new_file_name.split("4.0_Test_Automation")[-1]
            jfp.append(jira_file_path + "\n")
            # print jfp
            if not path.exists(present_directory):
                os.mkdir(present_directory)
            if not path.exists(sub_dir):
                mkdir(sub_dir)
            f = open(path.join(sub_dir, folder1), "w")
            f.write(file_cont)
            f.close()
            path_issue.append([test_cases[0], jira_file_path])
        print "\nNo. of Tags found in" + " " + filename1 + "=" + str(tags_count)
        print "No. of Test Cases found in" + " " + filename1 + "=" + str(len(test_cases_list))
        print("Refactor completed")
        print "Please Run Pre-Merge-Checker\n"
    else:
        print "Tags and Test Cases Mismatched"
        print "No. of Tags found in" + " " + filename1 + "=" + str(tags_count)
        print "No. of Test Cases found in" + " " + filename1 + "=" + str(len(test_cases_list))
        print("Refactor Failed.Please update the source file with missing Tags and retry\n")
        exit(1)

#Create a text file and store the file path

f1 = open(path.join(sub_dir, "Jira_Path_" + fld + ".txt"), "w")
f1.writelines(jfp)
f1.close()


#Update the JIRA Text1 custom field-Seed credentials

Option = raw_input('Continue?: If Yes press Y or press N to exit: ')

if Option == 'Y' or Option == 'y':
                                  user1 = raw_input('Enter your CGI USER ID Firstname.Lastname: ')
                                  pass1 = raw_input('Enter your CGI Password: ')
                                  #print(user1, pass1)
                                  for val in path_issue:
                                  # print(val[0] + "    " + val[1])
                                      jira_path_update(val[0], val[1], user1, pass1)
                                  print "JIRA-Path Update Successful"


else:
    print "JIRA-Path Update Pending"
    exit(1)
  

