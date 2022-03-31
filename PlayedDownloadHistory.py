# -*- coding: utf-8 -*-
# ==================================================================
#   OvercastAnalyse - Tools for analysing your overcast data.  
#
#   Copyright 2022 Philip Dell - https://github.com/pIlIp-d
#   MIT License
# ==================================================================

import argparse, os

from bs4 import BeautifulSoup as bs
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

def parse_args():
    all_args = argparse.ArgumentParser(prog='OvercastAnalyse', usage='%(prog)s [options]', description='Creates Plot of Overcast Statistik opml file.')
    all_args.add_argument("-p", "--path", required=False, help="path to overcast.opml file", default="."+os.path.sep+"overcast.opml")
    all_args.add_argument("-d", "--days", required=False, type=int, default=7, help="days to be summed together for each dataPoint")
    return vars(all_args.parse_args())

def print_help():
    print("for more help add option --help")

def get_time_list(file_path):
    time = []
    if not os.path.exists(file_path):
        print(file_path+" doesn't exist.")
        print_help()
        quit(-1)
    for feed in bs(open(file_path, "r"), 'html.parser').find_all("outline",{"type": "rss"}):
        f = feed.find_all("outline")
        for pod in f:
            if pod.get("played") != None or pod.get("progress") != None:
                time.append(dt.datetime.strptime(pod.get("userupdateddate")[:-15],'%Y-%m-%d'))
    return sorted(time)

def create_data_frame(time_list, days_to_sum_over):
    data_frame = pd.to_datetime(pd.DataFrame(time_list, columns = ['Time'])['Time'])
    #sum datapoints over time=days_to_sum_over to int wich represents y-values
    return data_frame.groupby(data_frame.dt.floor(str(days_to_sum_over)+'d')).size().reset_index(name='count')

def create_axis():
    fig, ax = plt.subplots(figsize=(15,7))
    fig.canvas.set_window_title('Overcast Analyser')
    #set x ticks to show every month and year in seperate rows
    ax.xaxis.set_major_locator(mpl.dates.YearLocator())
    ax.xaxis.set_minor_locator(mpl.dates.MonthLocator())
    ax.xaxis.set_major_formatter(mpl.dates.DateFormatter("\n%Y"))
    ax.xaxis.set_minor_formatter(mpl.dates.DateFormatter("%b"))
    #only intergers on y-axis
    ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(integer=True))
    #titles
    plt.title("Played Overcast Downloads")
    ax.set_ylabel("Downloads")
    #position
    plt.setp(ax.get_xticklabels(), rotation=0, ha="center")
    return ax

if __name__ == '__main__':
    args = parse_args()
    df = create_data_frame(get_time_list(args['path']),args['days'])
    df.plot(ax=create_axis(), x = "Time", y='count')

    plt.show()
