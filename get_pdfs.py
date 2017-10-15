import urllib2
from PyPDF2 import PdfFileReader, PdfFileWriter


def decrypt_pdf(url, output_path, password):
  response = urllib2.urlopen(url)
  tmp_name = open("tmp.pdf", 'wb')
  tmp_name.write(response.read())
  tmp_name.close()
  with open("tmp.pdf", 'rb') as input_file, \
    open(output_path, 'wb') as output_file:
        reader = PdfFileReader(input_file)
        reader.decrypt(password)
    
        writer = PdfFileWriter()
    
        for i in range(reader.getNumPages()):
            writer.addPage(reader.getPage(i))

        writer.write(output_file)

if __name__ == '__main__':
    URL = 'http://www.fao.org/ag/locusts/common/ecg/562/en/DL346e.pdf'
    decrypt_pdf(URL, 'test.pdf', '')
    
