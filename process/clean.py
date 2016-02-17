import csv, getopt, sys

def parse_args(argv):
    input_name = ''
    output_name = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["inputfile=","outputfile="])
    except getopt.GetoptError:
        print('clean.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('clean.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--inputfile"):
            input_name = arg
        elif opt in ("-o", "--outputfile"):
            output_name = arg
    return input_name, output_name


def clean(input_name, output_name):
    with open(input_name) as input_file:
        with open(output_name, 'w') as output_file:

            # remove double quotation marks from input file
            dirty_input_data = input_file.read()
            clean_input_data = dirty_input_data.replace('"', '')

            reader = csv.reader(clean_input_data.splitlines(), delimiter='\t')
            writer = csv.writer(output_file, delimiter='\t')
            for row in reader:
                write_row(writer, row)


def write_row(w, l):
    staging = []
    staging.append(l[0])    # geonameid
    staging.append(l[1])    # city name (utf8)
    staging.append(l[8])    # country code
    staging.append(l[10])   # admin1 code 
    staging.append(l[14])   # population
    staging.append(l[4])    # lat
    staging.append(l[5])    # lon
    staging.append(l[18])   # modification date
    w.writerow(staging)


if __name__ == "__main__":
    input_name, output_name = parse_args(sys.argv[1:])
    clean(input_name, output_name)

'''
from:
http://download.geonames.org/export/dump/

[00] geonameid         : integer id of record in geonames database
[01] name              : name of geographical point (utf8) varchar(200)
[02] asciiname         : name of geographical point in plain ascii characters, varchar(200)
[03] alternatenames    : alternatenames, comma separated, ascii names automatically transliterated, convenience attribute from alternatename table, varchar(10000)
[04] latitude          : latitude in decimal degrees (wgs84)
[05] longitude         : longitude in decimal degrees (wgs84)
[06] feature class     : see http://www.geonames.org/export/codes.html, char(1)
[07] feature code      : see http://www.geonames.org/export/codes.html, varchar(10)
[08] country code      : ISO-3166 2-letter country code, 2 characters
[09] cc2               : alternate country codes, comma separated, ISO-3166 2-letter country code, 200 characters
[10] admin1 code       : fipscode (subject to change to iso code), see exceptions below, see file admin1Codes.txt for display names of this code; varchar(20)
[11] admin2 code       : code for the second administrative division, a county in the US, see file admin2Codes.txt; varchar(80) 
[12] admin3 code       : code for third level administrative division, varchar(20)
[13] admin4 code       : code for fourth level administrative division, varchar(20)
[14] population        : bigint (8 byte int) 
[15] elevation         : in meters, integer
[16] dem               : digital elevation model, srtm3 or gtopo30, average elevation of 3''x3'' (ca 90mx90m) or 30''x30'' (ca 900mx900m) area in meters, integer. srtm processed by cgiar/ciat.
[17] timezone          : the timezone id (see file timeZone.txt) varchar(40)
[18] modification date : date of last modification in yyyy-MM-dd format
'''
