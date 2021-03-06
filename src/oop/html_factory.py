import madftp
from datetime import datetime

def write_user_html(participant, outdir):
    f = open('{}{}'.format(outdir, participant.html), 'w')
    header = '''<html>
<head>
    <title>''' + participant.html + '''</title>
    <meta http-equiv="refresh" content="20" /></head>
</head>
'''

    body_start = '''
<body>
<h2>''' + participant.html + '''</h2>
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

    for team in participant.teams:
        display = team.name
        if '/' in team.name:
            name = team.split('/', 1)[0]
        f.write('<tr>\n')
        if team.status == 'eliminated':
            f.write('    <td>{} {}*</td>\n'.format(team.seed, display))
        else:
            f.write('    <td>{} {}</td>\n'.format(team.seed, display))

        f.write('    <td align="center">{}</td>\n'.format(team.initial_max))
        f.write('    <td align="center">{}</td>\n'.format(team.current_max))
        f.write('    <td align="center">{}</td>\n'.format(team.total_points))

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


def write_leaderboard_html(outdir, leaderboard):
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
    for participant in leaderboard:
        f.write('<tr>\n')
        if place == 1:
            f.write('    <td align="center">{}</td>\n'.format(place))
        elif participant.total == last_score:
            f.write('    <td align="center"></td>\n')
        else:
            f.write('    <td align="center">{}</td>\n'.format(place))

        f.write('    <td>\n')
        f.write('        <a href="{}.html">{}</a>\n'.format(participant.name, participant.name))
        f.write('    </td>\n')
        last_score = participant.total
        place += 1

        f.write('    <td align="center">{}</td>\n'.format(participant.initial_max))

        f.write('    <td align="center">{}</td>\n'.format(participant.current_max))

        f.write('    <td align="center">{}</td>\n'.format(participant.total))

        f.write('</tr>\n')

    time = datetime.now().strftime('%I:%M %p')
    date = datetime.now().strftime('%m-%d-%Y')
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

