import get_pdfs
import pdf_to_locust_data
import clean_locustdata
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="Get locust PDFs")
    parser.add_argument('min', type=int, help='min issue number')
    parser.add_argument('max', type=int, help='max issue number')
    parser.add_argument('-u', '--url', help='base url for finding issues')
    parser.add_argument('-d', '--dir', help='destination directory for files')
    get_pdfs.main(parser.parse_args())
    pdf_to_locust_data.main()
    clean_locustdata.main()
    print("Done.")

if __name__ == "__main__":
    main()