
# import ctypes
# import sys
# import requests
# import win32api
# from datetime import datetime

# def timeSyncronisationAvecBinance():
#     binance_url = 'https://api.binance.com/api/v3/time'
#     response = requests.get(binance_url).json()

#     # Get the current server time from the response
#     server_time = response['serverTime']

#     # Convert server time to datetime object
#     server_datetime = datetime.fromtimestamp(server_time / 1000.0)

#     # Set the system time to the current server time
#     win32api.SetSystemTime(server_datetime.year, server_datetime.month, server_datetime.weekday(), server_datetime.day, server_datetime.hour, server_datetime.minute, server_datetime.second, 0)

#     # Print the current system time
#     import time
#     print('System time:', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))


# def run_as_admin(argv=None, debug=False):
#     if argv is None:
#         argv = sys.argv
#     # Demande à l'utilisateur s'il souhaite exécuter en tant qu'administrateur
#     params = '/k ' + ' '.join(argv)
#     if debug:
#         print(params)
#     ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)

# if __name__=='__main__':
#     run_as_admin()
#     timeSyncronisationAvecBinance()


import ctypes
import datetime
import sys
import requests
import time

def timeSyncronisationAvecBinance():
    binance_url = 'https://api.binance.com/api/v3/time'
    response = requests.get(binance_url).json()

    # Get the current server time from the response
    server_time = response['serverTime']

    # Convert server time to milliseconds
    server_time_ms = server_time

    # Get the current local time
    local_time = int(time.time() * 1000)

    # Calculate the time difference between server and local time
    time_diff_ms = server_time_ms - local_time

    # Adjust the local time by adding the time difference
    adjusted_time_ms = local_time + time_diff_ms

    # Convert the adjusted time to seconds
    adjusted_time = adjusted_time_ms / 1000.0

    # Construct the SYSTEMTIME structure
    class SYSTEMTIME(ctypes.Structure):
        _fields_ = [
            ("wYear", ctypes.c_uint16),
            ("wMonth", ctypes.c_uint16),
            ("wDayOfWeek", ctypes.c_uint16),
            ("wDay", ctypes.c_uint16),
            ("wHour", ctypes.c_uint16),
            ("wMinute", ctypes.c_uint16),
            ("wSecond", ctypes.c_uint16),
            ("wMilliseconds", ctypes.c_uint16)
        ]

    # Create an instance of the SYSTEMTIME structure
    system_time = SYSTEMTIME()

    # Set the values of the structure
    adjusted_datetime = datetime.datetime.fromtimestamp(adjusted_time)
    system_time.wYear = adjusted_datetime.year
    system_time.wMonth = adjusted_datetime.month
    system_time.wDayOfWeek = adjusted_datetime.weekday()
    system_time.wDay = adjusted_datetime.day
    system_time.wHour = adjusted_datetime.hour
    system_time.wMinute = adjusted_datetime.minute
    system_time.wSecond = adjusted_datetime.second
    system_time.wMilliseconds = 0

    # Set the system time using the SYSTEMTIME structure
    ctypes.windll.kernel32.SetSystemTime(ctypes.byref(system_time))

    # Print the current system time
    print('System time:', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

def run_as_admin(argv=None, debug=False):
    if argv is None:
        argv = sys.argv
    # Prompt the user to run as administrator
    params = '/k ' + ' '.join(argv)
    if debug:
        print(params)
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)

if __name__ == '__main__':
    run_as_admin()
    timeSyncronisationAvecBinance()



