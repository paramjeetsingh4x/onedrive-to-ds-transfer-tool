import os
import json
import xmltodict
import subprocess
from pathlib import Path

homeDir = str(Path.home())
batlocation = os.path.join(homeDir, 'Downloads', 'xmlmover.bat')
xmllocation = os.path.join(homeDir, 'Downloads', 'XMLs')
downloadsLoc = os.path.join(homeDir, 'Downloads')
jsonlocation = os.path.join(homeDir, 'Downloads', 'JSONs')
rclonelocation = os.path.join(homeDir, 'Downloads', 'rclone-v1.53.2-windows-amd64')

def fileConverter():
    global xmllocation, jsonlocation
    if not os.path.exists(jsonlocation):
        os.mkdir(jsonlocation)
    for dirName, subDirList, fileList in os.walk(xmllocation):
        for file in fileList:
          filename, extension = os.path.splitext(file)
          for file in filename:
                  with open(os.path.join(xmllocation, '%(filename)s.xml' % locals()),'r',encoding = 'utf-8') as xml_file:
                      data_dict = xmltodict.parse(xml_file.read())
                      xml_file.close()
          for file in filename:
                  json_data = json.dumps(data_dict)
                  with open(os.path.join(jsonlocation, '%(filename)s.json' % locals()),'w',encoding = 'utf-8') as json_file:
                      json_file.write(json_data)
                      json_file.close()
          for file in filename:
              if not filename.startswith("API_GP") :
                  with open(os.path.join(jsonlocation, '%(filename)s.json' % locals()),'r',encoding = 'utf-8') as json_file1:
                      jr = json_file1.read()
                      jr = jr.replace('@','')
                      jr = jr.replace('{"testsuites": ','')
                      jr = jr.replace('}}]}}','}}]}')
                  with open(os.path.join(jsonlocation, '%(filename)s.json' % locals()),'w',encoding = 'utf-8') as json_file1:
                      json_file1.write(jr)
                      json_file1.close()
              else:
                  with open(os.path.join(jsonlocation, '%(filename)s.json' % locals()),'r',encoding = 'utf-8') as json_file1:                  
                      jr = json_file1.read()
                      jr = jr.replace('@','')
                      jr = jr.replace('{"testsuites": ','')
                      jr = jr.replace('}]}]}}','}]}]}')
                  with open(os.path.join(jsonlocation, '%(filename)s.json' % locals()),'w',encoding = 'utf-8') as json_file1:
                      json_file1.write(jr)
                      json_file1.close()
    return print("XML to JSON conversion completed !!!")

def createXMLMoverBatFile():
    global batlocation
    myBat = open(os.path.basename(batlocation),'w+')
    myBat.write('''echo off
    mkdir %homepath%\Downloads\XMLs
    cd /d "%homepath%\Downloads\API_Results\"
    for /r %%d in (*) do copy "%%d" "%homepath%\Downloads\XMLs"
    ''')
    myBat.close()
    return print(".Bat File created !!!")

def runXMLMoverBatFile():
    global batlocation
    subprocess.call([os.path.basename(batlocation)])
    return print("All XML files moved !!!")

def apiDataTransfer():
    global rclonelocation
    os.chdir(rclonelocation)
    subprocess.run(["rclone", "copyto", "OneDrive:API_Recovery_Scripts_Results\All_API_Results", "GoogleCloud:env-dgsonedrive-aristocrat-platforms/API_data", "-P"])
    return print("API data transferred successfully to Google Cloud !!!")

def recoveryDataTransfer():
    global rclonelocation
    os.chdir(rclonelocation)
    subprocess.run(["rclone", "copyto", "OneDrive:API_Recovery_Scripts_Results\All_Recovery_Results", "GoogleCloud:env-dgsonedrive-aristocrat-platforms/Recovery_data", "-P"])
    return print("Recovery data transferred successfully to Google Cloud !!!")

def menu():
    try:
        userInput = int(input("Please Select Any Above Option: "))
    except ValueError:
        exit("Oops !!! You Had Enetered Wrong Choice ...")
    else:
        print("\n")
    if(userInput ==1):
        createXMLMoverBatFile()
    elif (userInput==2):
        runXMLMoverBatFile()
    elif (userInput==3):
        fileConverter()
    elif (userInput==4):
        apiDataTransfer()
    elif (userInput==5):
        recoveryDataTransfer()
    else:
        print("Enter correct choice. . . ")


def main():
    homeDir = str(Path.home())
    location1 = os.path.join(homeDir, 'Downloads')
    print(location1)
    choice = input("Do you want to perform any operation ? \"y/n\" : ")
    while (choice.lower()=='y'):
           print("1 : Create a xml mover batch file")
           print("2 : Run the batch file")
           print("3 : Convert all xml files to json files")
           print("4 : Transfer API data files from OneDrive to Google cloud")
           print("5 : Transfer Recovery data files from OneDrive to Google cloud")
           menu()
           choice = input("Do you want to perform any operation ? \"y/n\" : ")
main()
