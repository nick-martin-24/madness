#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 17:19:53 2019

@author: nickmartin
"""
import datetime
import collections
from ftplib import FTP




def process_group(group, field, outdir, ftpdir):
    for member in group:
        group[member]['initial max'] = 0
        group[member]['current max'] = 0
        group[member]['total'] = 0
        for team in group[member]['teams']:
            if '/' in team:
                team = team.split('/', 1)[0]
            print(team)
            group[member][team] = field[team]
            group[member]['total'] += field[team]['total points']
            group[member]['initial max'] += field[team]['initial max']
            group[member]['current max'] += field[team]['current max']
        generate_and_upload_user_html(group[member], outdir, ftpdir)
    group = collections.OrderedDict(sorted(group.items(), key=lambda x: x[1]['total'], reverse=True))

    return group



