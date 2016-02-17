import csv, getopt, sys
import operator

def parse_args(argv):
    input_name = ''
    output_name = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["inputfile=","outputfile="])
    except getopt.GetoptError:
        print('sort.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('sort.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--inputfile"):
            input_name = arg
        elif opt in ("-o", "--outputfile"):
            output_name = arg
    return input_name, output_name


def sort(input_name, output_name):
    with open(input_name) as input_file:
        with open(output_name, 'w') as output_file:
            reader = csv.reader(input_file, delimiter='\t')
            sorted_list = sorted(reader, key=lambda row: int(row[4]), reverse=True)
            
            writer = csv.writer(output_file, delimiter='\t')
            for row in sorted_list:
                writer.writerow(row)            


if __name__ == "__main__":
    input_name, output_name = parse_args(sys.argv[1:])
    sort(input_name, output_name)
