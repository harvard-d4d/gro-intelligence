import urllib2
import os
import sys
import argparse
import logging
import subprocess

LOCUST_URL = 'http://www.fao.org/ag/locusts/common/ecg/562/en/'

class Decrypter(object):

    def __init__(self, password, base_url, tmp_name):
        self.url = base_url
        self.password = password
        self.tmp = tmp_name

    def decrypt(self, url_ext, dest):
        response = urllib2.urlopen(self.url+url_ext)

        with open(self.tmp, 'wb+') as input_file:
            input_file.write(response.read())

        enc = os.path.join('.', self.tmp)
        dec = os.path.join('.', dest, url_ext)
        subprocess.call(['./decryptclean.sh', self.password, enc, dec])


def main(argv):

    base_url = LOCUST_URL if argv.url == None else argv.url
    dest = 'pdfs_decrypted' if argv.dir == None else argv.dir
    imin = argv.min
    imax = argv.max

    decrypter = Decrypter('', base_url, "tmp") 

    files = ['DL'+str(i)+'e.pdf' for i in xrange(imin, imax+1)]

    if not os.path.exists(dest):
        os.makedirs(dest)

    for file in files:
        try:
            print("Downloading " + file + "...")
            decrypter.decrypt(file, dest)
        except Exception as e:
            logging.exception(file + " failed")

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Get locust PDFs")
    parser.add_argument('min', type=int, help='min issue number')
    parser.add_argument('max', type=int, help='max issue number')
    parser.add_argument('-u', '--url', help='base url for finding issues')
    parser.add_argument('-d', '--dir', help='destination directory for files')

    main(parser.parse_args())
