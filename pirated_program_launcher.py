'''
OPERATING SYSTEM : WINDOWS only
Basically disables the wifi before launching the pirated program and then enables automatically
Requirements:
    Device Administrator Access
    Python installed in the system
    environment variable with value of path of pirated program set
Tips:
    1. You can replace the path variable in script below to full path of pirated program's .exe file as well.
    2. If you are building exe out of it replace 4 parameter of run_this_script_as_admin (i.e __file__ ) to ""
'''
import os
import time
import ctypes, sys
import threading

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_this_script_as_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

def wifi_enable():
    os.system("netsh interface set interface Wi-Fi enabled")

def wifi_disable():
    os.system("netsh interface set interface Wi-Fi disabled")

def launch(path):
    os.system(path)

def main():
    wifi_disable()
    time.sleep(3)
    threading._start_new_thread(launch, (path,))
    time.sleep(10)
    wifi_enable()

if __name__ == "__main__":
    path = os.getenv("PIRATED_PROGRAM")
    if is_admin():
        main()
    else:
        run_this_script_as_admin()
