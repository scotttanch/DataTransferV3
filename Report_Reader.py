import transfer_tools as tls
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from datetime import timedelta as td
import pandas as pd

report_folder = "D:\\Coding\\GPR_DATA\\4G_Reports"
file_paths = tls.full_stack(report_folder,"txt")

class Session_Report:
    def __init__(self,file_path):
        self.name = file_path.split('\\')[-1].split(".")[0]
        self.creation_date = self.name.split('_')[1]
        self.creation_time = self.name.split('_')[2]
        self.time_string = self.creation_date+"-2022::"+self.creation_time
        self.creation_date = datetime.strptime(self.time_string,"%m-%d-%Y::%H-%M")
        with open(self.name+'.txt', 'r') as f:
            self.data = f.readlines()[1:]

        tmp = []
        for line in self.data:
            tmp.append(float(line.split(',')[4]))
        self.avg_Bit = np.mean(tmp)
        self.std_Bit = np.std(tmp)

        tmp = []
        for line in self.data:
            tmp.append(float(line.split(',')[2]))
        self.avg_TwT = np.mean(tmp)*(10**-9)
        self.std_TwT = np.std(tmp)*(10**-9)
        
        tmp = []
        for line in self.data:
            tmp.append(float(line.split(',')[3]))
        self.avg_TwTP = np.mean(tmp)*(10**-9)
        self.std_TwTP = np.std(tmp)*(10**-9)
    
    def print(self):
        print("Report: ", self.name)
        print("Created on: ",self.creation_date," at ",self.creation_time)
        print("Average Acknowledgement time: ",self.avg_TwT," (s)")
        print("Average Processing time: ",self.avg_TwTP," (s)")
        print("Average Bit Rate: ",self.avg_Bit,"+\-",self.std_Bit,"(Mb/s)")

reports = []
for file in file_paths:
    reports.append(Session_Report(file))
reports.sort(key=lambda x: x.creation_date)

Bit_rates = []
Bit_stds = []
ACK_Times = []
Proc_Times = []
Dates = []

for report in reports:
    Dates.append(report.creation_date)
    Bit_rates.append(report.avg_Bit)
    Bit_stds.append(report.std_Bit)
    ACK_Times.append(report.avg_TwT)
    Proc_Times.append(report.avg_TwTP)

ticks = pd.date_range(min(Dates),max(Dates),6)
labels = []
for date in ticks:
    string = str(date.month) + "/" + str(date.day) + " " + str(date.hour) + ":" + str(date.minute)
    labels.append(string)

# Response Time subplot
plt.subplot(2,1,2)
plt.plot(Dates,ACK_Times)
plt.plot(Dates,Proc_Times)
plt.legend(["ACK","Processed"])
plt.title("Response and Processing Times")
plt.ylabel("Time (s)")
plt.xticks(ticks,labels,rotation=15)
#Subplot Annotations
plt.axvline(x = Dates[ACK_Times.index(max(ACK_Times))],color='r',linestyle='--')
line_text = Dates[ACK_Times.index(max(ACK_Times))].time()
ACK_Label = str(round(max(ACK_Times),2))+"(s)"
Proc_Label = str(round(max(Proc_Times),2))+"(s)"
plt.text(Dates[ACK_Times.index(max(ACK_Times))]-td(hours=1),max(ACK_Times)-0.75,ACK_Label,horizontalalignment='right')
plt.text(Dates[ACK_Times.index(max(ACK_Times))]-td(hours=1),max(Proc_Times)-0.75,Proc_Label,horizontalalignment='right')

# Bit Rate Subplot
plt.subplot(2,1,1)
plt.plot(Dates,Bit_rates)
plt.title("Bit Rate Sampled Every Half Hour")
plt.ylabel("Bit Rate (Mb/s)")
plt.xticks([])
#Subplot Annotations
plt.axvline(x = Dates[ACK_Times.index(max(ACK_Times))],color='r',linestyle='--')
line_text = Dates[ACK_Times.index(max(ACK_Times))].time()
plt.text(Dates[ACK_Times.index(max(ACK_Times))]+td(hours=1),0.0025,line_text,color='r')

# Show the plot
plt.show()

            
        
