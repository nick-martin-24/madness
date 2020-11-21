from tournament import Tournament
import html_factory
import madftp

t = Tournament()
html_factory.write_leaderboard_html(t.dirs['output'], t.group, t.dirs['ftp'])
madftp.upload_file_to_ftp(t.dirs['output'], t.files['leaderboard-html'].split('/')[-1], t.dirs['ftp'])

