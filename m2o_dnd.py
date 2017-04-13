#!/usr/bin/python
"""
Parallel download m2o archives.
"""

from multiprocessing.dummy import Pool as ThreadPool
from subprocess import call
from os import listdir
from os import rename

wget = "/usr/bin/wget"
base_url = "http://download.m2o.it/reloaded/"

def download(episode):
    url = base_url + "/" + episode["program"] + "/" + \
          episode["program"] + "_" + episode["date"] + "." + episode["extension"]
    call([wget, "-N", "-q", url])

# function to be mapped over
def downloadParallel(program, start_month, start_year, threads=2, extension="mp3"):
    pool = ThreadPool(threads)
    episodes = []
    for year in range(start_year, 18):
        for month in range(start_month, 13):
            for day in range(1, 32):
                date = "_".join([str(day).zfill(2),
                                 str(month).zfill(2),
                                 str(year).zfill(2)])
                episode = {"program":program, "date":date, "extension":extension}
                episodes.append(episode)
    pool.map(download, episodes)
    pool.close()
    pool.join()


def fix_naming(program, extension):
    files_list = listdir(".")
    for filename in files_list:
        if program in filename and filename.endswith(extension): 
            day, month, year = filename[len(program)+1:].split(".")[0].split("_")
            new_filename = "_".join([program, "20"+year, month, day]) + "." + extension
            rename(filename, new_filename)

programs = [
    "prezioso_in_action"
]

if __name__ == "__main__":
    for program in programs:
        downloadParallel(program, 0, 10, 60, "mp3")
        fix_naming(program, "mp3")
