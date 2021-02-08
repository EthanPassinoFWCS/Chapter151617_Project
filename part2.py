import csv
from datetime import datetime
import matplotlib.pyplot as plt
from os import path
from os import mkdir
import numpy as np

filename = "";
check_dates = []

print("Hello. You must get the data to be ran through to run this visual. Here is how to do that.")
print("Visit this website: https://www.ncdc.noaa.gov/cdo-web/datatools/findstation")
print("Select Dataset which should be 'Daily Summaries'")
print("Select Date range of your choice.")
print("In 'Data Categories' make sure you check box 'Air Temperature' and 'Precipitation'")
print("Select one of the stations on the map that is closest to the location where you want the data from.")
print("If there is not much coverage then you might want to choose a different station to get more data.")
print("Once you have found a station that you want choose click 'ADD TO CART'")
print("After this in the top right click on the 'Cart (Free Data)', this will take you to get the data.")
print("For 'Select the Output Format' make sure that you select 'Custom GHCN-Daily CSV'.")
print("Check to make sure that your date range is correct and the items in your cart is correct and at the bottom click the orange 'CONTINUE' button.")
print("Go to the Select Data Types and select precipitation and air temperature. Make sure they are selected and click on 'CONTINUE'.")
print("After this verify you got the right information, then give your email. Then select 'SUBMIT ORDER'.")
print("Now after a bit of time there will be an email that contains the data, download it.")
print("Please save it in the 'data' folder that this program is in.")
print("Once you have finished type 'ready' and if you want to quit type 'q'.")
if not path.exists("data"):
    mkdir("data")
    print("The data folder did not exist so we create one.")
contin = '';
while(True):
    contin = input("");
    if contin.lower() == "ready":
        break;
    if contin.lower() == "q":
        exit(-1)

while(True):
    filename = input("What is the name of the file that you put in the 'data' folder (don't give the extension)? If you want to exit type 'q'. ")
    if filename.lower() == "q":
        exit(-1)
    if path.exists(f"data/{filename}.csv"):
        print("Thanks.")
        break
    else:
        print("Invalid file name. Please try again. If you did not put a file in there read the instructions and do as instructed.")

while(True):
    dat = input("Please give us each date that you want data from. Please give it in this format: mm-dd (in numbers). Please type q to stop giving dates. If you give none we will exit the program.")
    if dat.lower() == "q":
        if len(check_dates) == 0:
            exit(-1)
        break
    try:
        check_dates.append(datetime.strptime(dat, "%m-%d"))
    except ValueError:
        print("That failed because you did not give it in the correct format. Please try again.")
        continue


with open(f"data/{filename}.csv") as f:
    reader = csv.reader(f)
    header_row = next(reader)
    maxtemp_index = header_row.index("TMAX")
    mintemp_index = header_row.index("TMIN")
    date_index = header_row.index("DATE")
    station_index = header_row.index("STATION")
    name_index = header_row.index("NAME")
    prec_index = header_row.index("PRCP")

    dates, highs, lows, precs = [], [], [], []
    ran = False

    for row in reader:
        ran = False
        current_date = datetime.strptime(row[date_index], "%Y-%m-%d")
        try:
            high = int(row[maxtemp_index])
            low = int(row[mintemp_index])
            prec = float(row[prec_index]) * 100
        except ValueError:
            continue
        for check_date in check_dates:
            if current_date.month == check_date.month and current_date.day == check_date.day:
                ran = True
                break
        if not ran:
            continue
        dates.append(current_date)
        highs.append(high)
        lows.append(low)
        precs.append(prec)
date_fix = [f"{date.year}" for date in dates]
x = np.arange(len(date_fix))
width=0.15

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, highs, width, color='r', label="Highs (F)")
rects2 = ax.bar(x + width/2, lows, width, color='b', label="Lows (F)")
rects3 = ax.bar((x + width/2) + width, precs, width, color='y', label="Precipitation (Percent)")
ax.set_ylabel("")
ax.set_xlabel("Dates")
ax.set_xticks(x)
ax.set_xticklabels(date_fix)
ax.legend()

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 3, height),
                    xytext=(0, 3),
                    textcoords='offset points',
                    ha='center', va='bottom')
autolabel(rects1)
autolabel(rects2)
autolabel(rects3)
fig.tight_layout()
plt.show()
