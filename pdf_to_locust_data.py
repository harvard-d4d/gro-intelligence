import sys
import os
import subprocess
import pickle
import pdf2txt as P2T
import textwrap

# usage: python pdf_to_locust_data.py TARGET_DIRECTORY/

def txt_to_dict(fname):
    str = ""
    with open(fname, 'rb') as f:
        for line in f:
            stripped_line = line.replace("\n", " ")
            str += stripped_line
    arr = str.split("\xe2")
    dict = {}

    for idx, item in enumerate(arr):
        if "SITUATION" in item:
            try:
                situation = item
                forecast = arr[idx+1]
                country = arr[idx-1].rsplit("  ", 1)[1]
                try:
                    country = country.rsplit("REGION")[1]
                except:
                    pass
                if country == '':
                    continue
                country = country.rstrip()
                country = country.lstrip()
                dict[country] = (situation, forecast)
            except:
                pass
    return dict

def pdf_to_txt(infile, outfile):
    P2T.main(["", "-o", outfile, infile])

def write_to_pickle(fname, out_dict):
    with open(fname, 'wb') as f:
        pickle.dump(out_dict, f)
        print "done writing pickle"

def convert_file(file, label):
    name = file[:-4]
    txt_name = name + ".txt"
    pickle_name = name + ".locustData"
    if(label):
        pickle_name += 'Labeled'
        txt_name += 'Labeled'

    print("Converting " + file + " to text...")
    pdf_to_txt(file, txt_name)
    print("Converting " + file + " to locustData...")
    out_dict = txt_to_dict(txt_name)
    if(label):
        for k in out_dict:
            print(textwrap.fill(str(out_dict[k][0]), 60))
            rating = input('rating: ')
            print(textwrap.fill(str(out_dict[k][1]), 60))
            forecast = input('rating: ')
            out_dict[k] = {
                'situation':out_dict[k][0],
                'rating':rating,
                'forecast':out_dict[k][1],
                'forecasted_rating':forecast,
            }
    else:
        out_dict = [{'situation': out_dict[k][0], 'forecast': out_dict[k][1]} for k in out_dict];
    write_to_pickle(pickle_name, out_dict)

def main():
    directory = sys.argv[1]
    label = (len(sys.argv) == 3 and sys.argv[-1] == 'label');

    for file in os.listdir(directory):
        if file[-4:] == ".pdf":
            convert_file(directory + file, label)

if __name__ == "__main__":
    main()
