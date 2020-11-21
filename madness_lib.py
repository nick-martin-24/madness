#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 17:19:53 2019

@author: nickmartin
"""
import datetime
import collections
from ftplib import FTP

ftp_user = '2096943'
ftp_password = 'Bonner10!'
ftp_site = 'golfpools.net'


def upload_file_to_ftp(path, filename, destination):
    ftp = FTP(ftp_site, ftp_user, ftp_password)
    ftp.cwd(destination)
    file = open(path + filename, 'rb')
    ftp.storbinary('STOR ' + filename, file)
    file.close()
    ftp.quit()


def create_ftp_dirs(ftp_dir, ftp_teams):
    ftp = FTP(ftp_site, ftp_user, ftp_password)
    ftp.mkd(ftp_dir)
    ftp.mkd(ftp_teams)
    ftp.quit()


def generate_field(games, field, multiplier, first_four):
    for i in range(0, len(games)):
        #        print(i)
        #       if games[i]['game']['bracketRound'] == first_four:
        #            continue

        for team in ['home', 'away']:
            #            print(team)
            if '/' in team:
                team = team.split('/', 1)[0]
            data = games[i]['game'][team]
            name = data['names']['short']
            if name == '':
                continue

            if games[i]['game']['bracketRound'] == 'First Round'\
                    or games[i]['game']['bracketRound'] == first_four:  # initialize team
                field[name] = {}
                field[name]['total points'] = 0
                field[name]['seed'] = int(data['seed'])
                #                print('value: {}; type: {}'.format(data['seed'],type(data['seed'])))
                field[name]['initial max'] = field[name]['seed'] * sum(multiplier.values())
                field[name]['current max'] = field[name]['initial max']
                field[name]['status'] = 'active'

            if games[i]['game']['gameState'] == 'final':
                if data['winner']:  # add points to total
                    field[name]['total points'] += field[name]['seed'] * multiplier[games[i]['game']['bracketRound']]

                else:  # change status, update current max
                    field[name]['status'] = 'eliminated'
                    field[name]['current max'] = field[name]['total points']

    return field


def create_group(group):
    group['Brad'] = {}
    group['Brad']['html'] = 'Brad'
    group['Brad']['teams'] = ['Texas Tech', 'Kansas', 'VCU', 'Florida', 'Vermont']

    group['Mark'] = {}
    group['Mark']['html'] = 'Mark'
    group['Mark']['teams'] = ['Tennessee', 'Wisconsin', 'Baylor', 'Murray State', 'Yale']

    group['Chris'] = {}
    group['Chris']['html'] = 'Chris'
    group['Chris']['teams'] = ['Gonzaga', 'Kansas St.', 'UCF', 'New Mexico St.', 'Northeastern']

    group['Dan'] = {}
    group['Dan']['html'] = 'Dan'
    group['Dan']['teams'] = ['Mich. St. ', 'Maryland', 'Utah State', 'St. Mary\'s (Cal.)', 'Montana']

    group['Ken'] = {}
    group['Ken']['html'] = 'Ken'
    group['Ken']['teams'] = ['Purdue', 'Buffalo', 'Oklahoma', 'Arizona St.', 'Northern Kentucky']

    group['Nick the Younger'] = {}
    group['Nick the Younger']['html'] = 'Nick the Younger'
    group['Nick the Younger']['teams'] = ['North Carolina', 'Villanova', 'Washington', 'Minnesota', 'Georgia State']

    group['Nick the Elder'] = {}
    group['Nick the Elder']['html'] = 'Nick the Elder'
    group['Nick the Elder']['teams'] = ['Michigan', 'Iowa State', 'Nevada', 'Oregon', 'Old Dominion']

    group['Patrick'] = {}
    group['Patrick']['html'] = 'Patrick'
    group['Patrick']['teams'] = ['Virginia', 'Florida State', 'Cincinnati', 'Seton Hall', 'Abilene Christian']

    group['Paul'] = {}
    group['Paul']['html'] = 'Paul'
    group['Paul']['teams'] = ['LSU', 'Mississippi St.', 'Mississippi', 'Liberty', 'Bradley']

    group['Robbie'] = {}
    group['Robbie']['html'] = 'Robbie'
    group['Robbie']['teams'] = ['Duke', 'Virginia Tech', 'Syracuse', 'Belmont', 'UC Irvine']

    group['Stephen'] = {}
    group['Stephen']['html'] = 'Stephen'
    group['Stephen']['teams'] = ['Kentucky', 'Auburn', 'Louisville', 'Ohio St. ', 'Saint Louis']

    group['Zeke'] = {}
    group['Zeke']['html'] = 'Zeke'
    group['Zeke']['teams'] = ['Houston', 'Marquette', 'Wofford', 'Iowa', 'Colgate']

    return group


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


def generate_and_upload_user_html(person, outdir, ftpdir):
    f = open('{}{}.html'.format(outdir, person['html']), 'w')
    header = '''<html>
<head>
    <title>''' + person['html'] + '''</title>
    <meta http-equiv="refresh" content="20" /></head>
</head>
'''

    body_start = '''
<body>
<h2>''' + person['html'] + '''</h2>
'''

    table_start = '''
<table border="3" cellspacing="1" cellpadding="1">
<caption>Roster</caption>
        
<tr>
    <td><b>Team</b></td>
    <td><b>Initial Max Points</b></td>
    <td><b>Current Max Points</b></td>
    <td><b>Total Points</b></td>
</tr>
'''

    f.write(header)
    f.write(body_start)
    f.write(table_start)

    for team in person['teams']:
        display = team
        if '/' in team:
            team = team.split('/', 1)[0]
        f.write('<tr>\n')
        if person[team]['status'] == 'eliminated':
            f.write('    <td>{} {}*</td>\n'.format(person[team]['seed'], display))
        else:
            f.write('    <td>{} {}</td>\n'.format(person[team]['seed'], display))

        f.write('    <td align="center">{}</td>\n'.format(person[team]['initial max']))
        f.write('    <td align="center">{}</td>\n'.format(person[team]['current max']))
        f.write('    <td align="center">{}</td>\n'.format(person[team]['total points']))

        f.write('</tr>\n')

    table_end = '''
</table>
'''

    asterisk = '''
    * = team has been eliminated
    '''

    leaderboard_link = '''
<br><a href="leaderboard.html">Back to Leaderboard</a>
'''

    body_end = '''
</body>
</html>
'''

    f.write(table_end)
    f.write(asterisk)
    f.write(leaderboard_link)
    f.write(body_end)

    f.close()

    upload_file_to_ftp(outdir, person['html'] + '.html', ftpdir)


def generate_leaderboard_html(outdir, leaderboard, ftpdir):
    filename = outdir + 'leaderboard.html'
    f = open(filename, 'w')
    header = '''<!DOCTYPE html>
<html>


<head>
<title>2019 OC Debauchery March Madness Tournament</title>
<meta http-equiv="refresh" content="20" />
</head>


<h1 align="center">2019 OC Debauchery March Madness Tournament</h1>


<table summary="leaderboard" align="center" bgcolor="white" border="3" cellspacing="1" cellpadding="1" style="display:inline-block; margin:auto">
<tr>
<td colspan="5" align="center">Leaderboard</td>
</tr>

<tr>
    <td>Place</td>
    <td>Player</td>
    <td>Initial Max</td>
    <td>Current Max</td>
    <td>Total Points</td>
</tr>
'''
    f.write(header)

    place = 1
    last_score = -999
    for person in leaderboard:
        f.write('<tr>\n')
        if place == 1:
            f.write('    <td align="center">{}</td>\n'.format(place))
        elif leaderboard[person]['total'] == last_score:
            f.write('    <td align="center"></td>\n')
        else:
            f.write('    <td align="center">{}</td>\n'.format(place))

        f.write('    <td>\n')
        f.write('        <a href="{}.html">{}</a>\n'.format(person, person))
        f.write('    </td>\n')
        last_score = leaderboard[person]['total']
        place += 1

        f.write('    <td align="center">{}</td>\n'.format(leaderboard[person]['initial max']))

        f.write('    <td align="center">{}</td>\n'.format(leaderboard[person]['current max']))

        f.write('    <td align="center">{}</td>\n'.format(leaderboard[person]['total']))

        f.write('</tr>\n')

    time = datetime.datetime.now().strftime('%I:%M %p')
    date = datetime.datetime.now().strftime('%m-%d-%Y')
    timestamp = '''
<tr>
    <td colspan="5" align="center">Last updated at ''' + time + ''' on ''' + date + '''</td>
</tr>
    '''

    footer = '''
</table>
</body>
</html>
'''

    f.write(timestamp)
    f.write(footer)

    f.close()

    upload_file_to_ftp(outdir, 'leaderboard.html', ftpdir)
