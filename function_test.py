import smtplib
from email import message
import os
import time
import subprocess

""" def test_function():
    try:

        sum_value = 5 / 0
        print(sum_value)
        return "up"

    except:

        return "down"




appstatus = test_function()
print(appstatus)
open('reboot_flag_test', 'x') """

arguments = "\\localhost Stretchly"


subprocess.call(['pskill.exe', arguments])
time.sleep(10)
""" os.popen('PsService.exe \\lo3wcbsftapp01.peroot.com start Tomcat9')
time.sleep(10)
status = os.popen('PsService.exe \\lo3wcbsftapp01.peroot.com query Tomcat9')
print(status) """

