from datetime import datetime

class App_Logger:

    def __init__(self, file='logFiles.log'):
        self.f_name = file

    def info(self, log_type, log_message):
        now = datetime.now()
        current_time = now.strftime("%d-%m-%Y %H:%M:%S")
        f = open(self.f_name, "a+")
        f.write(current_time + "," + log_type + "," + log_message + "\n")
        f.close()