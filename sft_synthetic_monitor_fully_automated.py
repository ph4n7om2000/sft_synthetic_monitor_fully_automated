from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import smtplib
from email import message
from datetime import datetime
import time
import os
import subprocess

log_object = open('uat-runlog', 'a')

def send_failure_email():
    from_addr = 'sftalert@yourdomain.com'
    to_addr = 'team1@yourdomain.com'
    to_addr2 = 'team2@yourdomain.com'
    subject = 'SFT Alert!'
    body = 'Login check has failed. Check application availablility ASAP!'
    msg = message.Message()
    msg.add_header('from', from_addr)
    msg.add_header('to', to_addr)
    msg.add_header('subject', subject)
    msg.set_payload(body)
    server = smtplib.SMTP('smtp.yoursmtpserver.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(from_addr, 'yoursmtppassword')
    server.send_message(msg, from_addr=from_addr, to_addrs=[to_addr])
    server.send_message(msg, from_addr=from_addr, to_addrs=[to_addr2])


def monitor():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    s = Service("chromedriver")
    url = "https://uat-sft.yourdomain.com/"
    driver = webdriver.Chrome(options=options, service=s)
    driver.get(url)
    print(driver.title)


    try:
        usernameelement = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )

        time.sleep(10)
        if usernameelement.is_displayed() == True:
                print ("Login page loaded!")
                now = datetime.now()
                log_object.write("Login page loaded at: " + now.strftime("%m/%d/%Y, %H:%M:%S") + "\n")
    
        driver.find_element(By.ID, "username").send_keys("platformuser@yourdomain.com")
        driver.find_element(By.ID, "password").send_keys("platformuserpassword")
        print("Attempting login...")
        now = datetime.now()
        log_object.write("Attempting login at: " + now.strftime("%m/%d/%Y, %H:%M:%S") + "\n")
        driver.find_element(By.ID, "signinButton").click()
        
        time.sleep(10)
        composebuttonelement = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "compose-delivery-link"))
            )
        if composebuttonelement.is_displayed() == True:
                print ("Successfully logged in!")
                now = datetime.now()
                log_object.write("Successfully logged in at: " + now.strftime("%m/%d/%Y, %H:%M:%S") + "\n")

        print ("Opening compose delivery page...")
        now = datetime.now()
        log_object.write("Opening compose delivery page at: " + now.strftime("%m/%d/%Y, %H:%M:%S") + "\n")
        driver.find_element(By.ID, "compose-delivery-link").click()
        
        time.sleep(10)
        divSecureMessageelement = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "divSecureMessage"))
            )
        if divSecureMessageelement.is_displayed() == True:
                print ("Succesfully opened Compose Delivery page!")
                now = datetime.now()
                log_object.write("Opening compose delivery page at: " + now.strftime("%m/%d/%Y, %H:%M:%S") + "\n")
                print ("All checks passed!")
                now = datetime.now()
                log_object.write("All checks passed at: " + now.strftime("%m/%d/%Y, %H:%M:%S") + "\n")
                
        logouturl = "https://uat-sft.yourdomain.com/bds/Logout.do"
        now = datetime.now()
        print ("Successfully logged out!")
        log_object.write("Successfully logged out at: " + now.strftime("%m/%d/%Y, %H:%M:%S") + "\n")
        log_object.write("---------------------------------------------------------------------------------------------------------\n")
        driver.get(logouturl)
        log_object.close()
        if os.path.exists('reboot_flag') == False:
            open('reboot_flag', 'x')
        driver.close()
        return "up"

    except:
        now = datetime.now()
        print ("SFT health check failed! Sending alert...")
        log_object.write("SFT health check failed at: " + now.strftime("%m/%d/%Y, %H:%M:%S") + "\n")
        send_failure_email()
        return "down"

appstatus = monitor()

if appstatus == "down":
    now = datetime.now()
    
    if os.path.exists('reboot_flag') == True:
        log_object.write("Initiated SQL services restart at: " + now.strftime("%m/%d/%Y, %H:%M:%S") + "\n")
        mssql_arguments = '\\sqlserver.yourdomain.com restart mssqlserver'
        subprocess.call(['psService.exe', mssql_arguments])
        time.sleep(60)
        log_object.write("SQL services have been restarted at: " + now.strftime("%m/%d/%Y, %H:%M:%S") + "\n")
        
        log_object.write("Initiated application services restart at: " + now.strftime("%m/%d/%Y, %H:%M:%S") + "\n")  
        tomcat_kill_arguments = '\\applicationserver.yourdomain.com Tomcat9'
        subprocess.call(['pskill.exe', tomcat_kill_arguments])
        time.sleep(60)

        tomcat_start_arguments = '\\applicationserver.yourdomain.com start Tomcat9'
        subprocess.call(['psService.exe', tomcat_start_arguments])
        log_object.write("Application services have been restarted at: " + now.strftime("%m/%d/%Y, %H:%M:%S") + "\n")
        os.remove("reboot_flag")

    else:
        log_object.write("Initiated application services restart at: " + now.strftime("%m/%d/%Y, %H:%M:%S") + "\n")
        tomcat_kill_arguments = '\\applicationserver.yourdomain.com Tomcat9'
        subprocess.call(['pskill.exe', tomcat_kill_arguments])
        time.sleep(60)

        tomcat_start_arguments = '\\applicationserver.yourdomain.com start Tomcat9'
        subprocess.call(['psService.exe', tomcat_start_arguments])
        time.sleep(60)
        log_object.write("Application services have been restarted at: " + now.strftime("%m/%d/%Y, %H:%M:%S") + "\n")
        
        log_object.write("Initiated SQL services restart at: " + now.strftime("%m/%d/%Y, %H:%M:%S") + "\n")
        mssql_arguments = '\\sqlserver.yourdomain.com restart mssqlserver'
        subprocess.call(['psService.exe', mssql_arguments])
        time.sleep(60)
        log_object.write("SQL services have been restarted at: " + now.strftime("%m/%d/%Y, %H:%M:%S") + "\n")
        open('reboot_flag', 'x')
        
        
