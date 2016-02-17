import csv, getopt, sys
import operator

def parse_args(argv):
    input_name = ''
    output_name = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["inputfile=","outputfile="])
    except getopt.GetoptError:
        print('chop.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('chop.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--inputfile"):
            input_name = arg
        elif opt in ("-o", "--outputfile"):
            output_name = arg
    return input_name, output_name


def chop(input_name, output_name):
    if output_name == "":
        print('Please define output file name using -o flag')
        sys.exit(2)

    small_name = output_name + "_S"
    medium_name = output_name + "_M"
    large_name = output_name + "_L"
    all_name = output_name + "_ALL"

    with open(input_name) as input_file:
        with open(small_name, 'w') as small_file:
            with open(medium_name, 'w') as medium_file:
                with open(large_name, 'w') as large_file:
                    with open(all_name, 'w') as all_file:
                        reader = csv.reader(input_file, delimiter='\t')
                        sw   = csv.writer(small_file, delimiter='\t')
                        mw   = csv.writer(medium_file, delimiter='\t')
                        lw   = csv.writer(large_file, delimiter='\t')
                        allw = csv.writer(all_file, delimiter='\t')
                        si = 1000
                        mi = 5000
                        li = 10000

                        for row in reader:
                            if si > 0:
                                sw.writerow(row)
                                si -= 1
                            if mi > 0:
                                mw.writerow(row)
                                mi -= 1
                            if li > 0:
                                lw.writerow(row)
                                li -= 1
                            allw.writerow(row)
                            

if __name__ == "__main__":
    input_name, output_name = parse_args(sys.argv[1:])
    chop(input_name, output_name)
