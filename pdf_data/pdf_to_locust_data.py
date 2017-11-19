import sys
import os
import subprocess
import pickle
import pdf2txt as P2T
import textwrap

# usage: python pdf_to_locust_data.py TARGET_DIRECTORY/

def txt_to_dict(fname):
    str = reduce(lambda a, l: a + l.replace("\n", " "), open(fname, 'rb'))
    arr = str.split("\xe2")
    dict = {}

    for idx, item in enumerate(arr[:-1]):
        if "SITUATION" in item:
            try:
                country, situation, forecast = map(lambda x: x.strip(), arr[idx-1:idx+2]);
                country = country.rsplit("  ", 1)[1].strip()
                countryName = country.rsplit("REGION")
                if len(countryName) > 1:
                    country = countryName[1].strip()
                if country != '':
                    dict[country] = (situation, forecast)
            except:
                pass
    return dict

def convert_file(name):
    locust, text, pdf = map(lambda x: name + x, [".locustData", ".txt", ".pdf"])

    print("Converting " + name + " to locustData...")

    P2T.main(["", "-o", text, pdf])
    out_dict = txt_to_dict(text)
    os.remove(text)
    pickle.dump(out_dict, open(locust, 'wb'))

def main():
    directory = "pdfs_decrypted/"
    for file in os.listdir(directory):
        if file[-4:] == ".pdf":
            convert_file(directory + file[:-4])

if __name__ == "__main__":
    main()
