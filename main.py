import csv
from datetime import datetime
import matplotlib.pyplot as plt

filename = "data/Selma Indiana 2010-2020.csv"
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)

    dates, highs, lows, parcs = [], [], [], []

    years = []
    for row in reader:
        current_date = datetime.strptime(row[2], "%Y-%m-%d")
        if current_date.year in years:
            continue
        if current_date.month == 10:
            if current_date.day == 2 or current_date.day == 3:
                try:
                    high = int(row[9])
                    low = int(row[10])
                    parc = float(row[5]) * 100
                except ValueError:
                    print(f"Missing data for {current_date}")
                else:
                    years.append(current_date.year)
                    dates.append(current_date)
                    highs.append(high)
                    lows.append(low)
                    parcs.append(parc)

    # Making the highs and lows into a graph.

    plt.style.use('seaborn')
    fig, ax = plt.subplots()
    ax.plot(dates, highs, c='red', alpha=0.5)
    ax.plot(dates, lows, c='blue', alpha=0.5)
    ax.set_ylabel("Temperature (F) [Red High/Blue Low]", fontsize=16)

    # Fill in between the two lines
    plt.fill_between(dates, highs, lows, facecolor='blue', alpha=0.1)

    # Adding Precipitation line graph
    ax2 = ax.twinx()
    ax2.set_ylabel("Precipitation (Percent) [Yellow]", fontsize=16)
    ax2.plot(dates, parcs, c="yellow", alpha=0.5)


    # Format the plot and show.
    plt.title("High/Low Temperatures on October 2nd/3rd for each year.\nSelma, IN", fontsize=20)
    plt.xlabel("", fontsize=16)
    fig.autofmt_xdate()
    plt.tick_params(axis='both', which='major', labelsize=16)

    plt.show()
