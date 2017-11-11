import pickle
import os
import sys
import textwrap

def label_file(file):
    name = file.split('.')[0]
    pickle_name = name + "_labeled.data"
    out_dict = pickle.load(open(file, 'rb'))
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
    write_to_pickle(pickle_name, out_dict)


def main():
    if len(sys.argv) > 2:
        directory = sys.argv[2]
        if not directory[-1] == '/':
            directory += '/'
    else:
        directory = 'pdfs_decrypted/'

    ext = sys.argv[1]

    for file in os.listdir(directory):
        if file.split('.')[-1] == ext:
            label = raw_input('Label file ' + file + '? (y/n): ')
            if label.lower() != 'y':
                continue
            label_file(directory+file)

if __name__ == "__main__":
    main()

