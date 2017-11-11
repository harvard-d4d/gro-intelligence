import pickle
import glob

def main():

    files = glob.glob('pdfs_decrypted/*.locustData')

    # Some headers got mixed in
    countries = ["Afghanistan","Armenia","Azerbaijan","Bahrain","Bangladesh","Bhutan","Brunei","Cambodia","China","Cyprus","Georgia","India","Indonesia","Iran","Iraq","Israel","Japan","Jordan","Kazakhstan","Kuwait","Kyrgyzstan","Laos","Lebanon","Malaysia","Maldives","Mongolia","Myanmar (Burma)","Nepal","North Korea","Oman","Pakistan","Palestine","Philippines","Qatar","Russia","Saudi Arabia","Singapore","South Korea","Sri Lanka","Syria","Taiwan","Tajikistan","Thailand","Timor-Leste","Turkey","Turkmenistan","United Arab Emirates (UAE)","Uzbekistan","Vietnam","Yemen","Bahrain","Cyprus","Egypt","Iran","Iraq","Israel","Jordan","Kuwait","Lebanon","Oman","Qatar","Saudi Arabia","Syria","Turkey","United Arab Emirates","Yemen","India","Algeria","Angola","Benin","Botswana","Burkina Faso","Burundi","Cabo Verde","Cameroon","Chad","Comoros","Democratic Republic of the Congo","Republic of the Congo","Cote d'Ivoire","Djibouti","Egypt","Equatorial Guinea","Eritrea","Ethiopia","Gabon","Gambia","Ghana","Guinea","Guinea-Bissau","Kenya","Lesotho","Liberia","Libya","Madagascar","Malawi","Mali","Mauritania","Mauritius","Morocco","Mozambique","Namibia","Niger","Nigeria","Rwanda","Sao Tome and Principe","Senegal","Seychelles","Sierra Leone","Somalia","South Africa","South Sudan","Sudan","Swaziland","Tanzania","Togo","Tunisia","Uganda","Zambia","Zimbabwe"]
    countries = list(set(countries))

    for fname in files:
        print 'Cleaning ' + fname + '...'
        # Open locustData file
        raw_name = fname.split('/')[1].split('.locustData')[0]
        issue = fname.split('.')[0].split('DL')[1][:-1]
        f = open(fname)
        test_dict = pickle.load(f)

        # Getting rid of all the \x stuff
        # Gets rid of all the headers and page numbers and random country headers
        bad = {'\xef\xac\x81 ': 'fi','\x80\xa2 ': '','\x80\x93 ': '-','\x0c':''}
        for key in test_dict.keys():
            to_set = ['','']
            ind = 0
            for elem in test_dict[key]:
                run_elem = elem.rstrip()
                for bk in bad.keys():
                    run_elem = run_elem.replace(bk,bad[bk])
                untouched = len(countries)*-1
                boo_count = [run_elem.split('.')[-1].find(item) for item in countries]
                if sum(boo_count) != untouched:
                    run_elem = '.'.join(run_elem.split('.')[:-1]) + '.'
                if 'FORECAST' in run_elem:
                    ind = 1
                if 'D E S E R T  L O C U S T  B U L L E T I N' in run_elem:
                    spl1 = run_elem.split('D E S E R T  L O C U S T  B U L L E T I N')
                    mods = range(0,len(spl1),3) + range(2,len(spl1),3)
                    run_elem = ''.join([spl1[i] for i in mods])
                if 'No. ' in run_elem:
                    is_ind = run_elem.find('No. ')
                    issue = run_elem[is_ind:is_ind+7]
                    run_elem = ''.join(run_elem.split(issue))
                to_set[ind] += run_elem
            test_dict[key] = tuple(to_set)

        # Output to pickle
        newFile = open('pdfs_decrypted/' + raw_name + '.cleanData','w')
        pickle.dump(test_dict, newFile)

if __name__ == "__main__":
    main()
