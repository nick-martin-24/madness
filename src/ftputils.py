from ftplib import FTP
import glob
import os

user = os.environ['gp_user']
password = os.environ['gp_pass']
site = os.environ['gp_site']

def setup():
    ftp = ftplib.FTP(site, user, password)
    d = 'golfpools.net/{}/ocdebaucheery/'.format(dt.now().year)
    try:
        ftp.mkd(d)
    except ftplib.error_perm:
        print('FTP directory {} already exists!'.format(d))

    teams = '{}/teams'.format(d)
    try:
        ftp.mkd(teams)
    except ftplib.error_perm:
        print('FTP directory {} already exists!'.format(teams))
    ftp.quit()

def upload_file_to_ftp(path, filename, destination):
    ftp = ftplib.FTP(site, user, password)
    ftp.cwd(destination)
    file = open(path + '/' + filename, 'rb')
    ftp.storbinary('STOR ' + filename, file)
    file.close()
    ftp.quit()
