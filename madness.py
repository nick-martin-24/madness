#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 12:32:02 2019

@author: nickmartin
"""
import requests
import madness_lib
import time

start = time.time()
outdir = '/Users/nickmartin/personal/madness/'
ftpdir = 'golfpools.net/2019/ocdebauchery/'
link = 'https://data.ncaa.com/casablanca/carmen/brackets/championships/basketball-men/d1/2019/data.json'
f = requests.get(link)
parsed_json = f.json()
games = parsed_json['games']
multiplier = {'First Four&#174;': 0,
              'First Round': 1,
              'Second Round': 2,
              'Sweet 16&#174;': 3,
              'Elite Eight&#174;': 4,
              'FINAL FOUR&#174;': 6,
              'Championship': 10}
first_four = 'First Four&#174;'


field = {}
field = madness_lib.generate_field(games, field, multiplier, first_four)


group = {}
group = madness_lib.create_group(group)

group = madness_lib.process_group(group, field, outdir, ftpdir)

madness_lib.generate_leaderboard_html(outdir, group, ftpdir)

print('Run time: {} seconds'.format(time.time()-start))
