import subprocess
import time

tomcat_kill_arguments = '\\lo3wcbsftapp01.peroot.com Tomcat9'
subprocess.call(['pskill.exe', tomcat_kill_arguments])
time.sleep(60)

tomcat_start_arguments = '\\lo3wcbsftapp01.peroot.com start Tomcat9'
subprocess.call(['psService.exe', tomcat_start_arguments])



mssql_arguments = '\\lo3wcbsftapp01.peroot.com restart MSSQLSERVER'
subprocess.call(['psService.exe', mssql_arguments])




