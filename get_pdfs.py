import urllib2
import os
import sys
import argparse
import PyPDF2 as pypdf

LOCUST_URL = 'http://www.fao.org/ag/locusts/common/ecg/562/en/'

class massDecrypter(object):

    def __init__(self, password, base_url, tmp_name):
        self.url = base_url
        self.password = password
        self.tmp = tmp_name

    def decrypt_pdf(self, url_ext, dest):
        if not os.path.exists(dest):
            os.makedirs(dest)
        response = urllib2.urlopen(self.url+url_ext)
        with open(self.tmp, 'ab+') as input_file, \
            open(dest+url_ext, 'wb') as output_file:
                input_file.write(response.read())
                reader = pypdf.PdfFileReader(input_file)
                if reader.isEncrypted:
                    reader.decrypt(self.password)
        
                writer = pypdf.PdfFileWriter()
    
                for i in range(reader.getNumPages()):
                    writer.addPage(reader.getPage(i))

                writer.write(output_file)

        os.remove(self.tmp)


def main(argv):

    base_url = LOCUST_URL if argv.url == None else arv.url
    dest = 'pdfs_decrypted/' if argv.dest == None else arv.dest
    imin = argv.issue_min[0]
    imax = argv.issue_max[0]

    g = massDecrypter('', base_url, "tmp") 

    files = ['DL'+str(i)+'e.pdf' for i in xrange(imin, imax+1)]

    for f in files:
        try:
            g.decrypt_pdf(f, dest)
        except:
            print(f+" failed")

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Get locust PDFs")
    parser.add_argument('min', type=int, help='min issue number')
    parser.add_argument('max', type=int, help='max issue number')
    parser.add_argument('-u', '--url', help='base url for finding issues')
    parser.add_argument('-d', '--dir', help='destination directory for files')

    main(parser.parse_args())
