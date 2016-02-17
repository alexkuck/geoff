import csv, getopt, sys

def parse_args(argv):
    input_name = ''
    output_name = ''
    blat = 90 / 3
    blon = blat * 2
    try:
        arg_str = "h:i:o:m:n:"
        arg_list = ["help", "inputfile=","outputfile=", "blat=", "blon="]
        opts, args = getopt.getopt(argv, arg_str, arg_list)
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-i", "--inputfile"):
            input_name = arg
        elif opt in ("-o", "--outputfile"):
            output_name = arg
        elif opt in ("-m"):
            blat = int(arg)
        elif opt in ("-n"):
            blon = int(arg)
        else:
            usage()
            sys.exit(2)

    return input_name, output_name, blat, blon

def usage():
    help_str = 'bucket.py -i <inputfile> -o <outputfile> -m <blat> -n <blon>'
    print(help_str)


def bucket(input_name, output_name, blat, blon):
    # blat and blon == buckets per direction per quadrant
    # you can play with these numbers, but keep them clean divisibles

    with open(input_name) as input_file:
        with open(output_name, 'w') as output_file:
            reader = csv.reader(input_file, delimiter='\t')
            writer = csv.writer(output_file, delimiter='\t')

            for row in reader:
                lat = float(row[5])
                lon = float(row[6])
                i = get_index(blat, blon, lat, lon)
                write_row(writer, i, row)


def get_index(blat, blon, lat, lon):
    blat_deg = 90 / blat        # degrees per latitude bucket
    blon_deg = 180 / blon       # degrees per longitude bucket
    alat = int(abs(lat))        # adjusted lat of city
    alon = int(abs(lon))        # adjusted lon of city
    
    m = alat / blat_deg         # index latitude bucket
    n = alon / blon_deg         # index longitude bucket
    qi = m*blon + n             # quadrant index of city lat, lon

    bpq = blat * blon           # buckets per quadrant
    quad = get_quad(lat, lon)   # quadrant city resides in
    index = qi + quad * bpq     # global index of city lat, lon

    return int(index)
    
def get_quad(lat, lon):
    if lat > 0:
        if lon > 0:
            return 0    # north west
        return 3        # south west
    if lon > 0:
        return 1        # north east
    return 2            # sound east

def write_row(w, i, row):
    staging = []
    staging.append(str(i))
    staging.extend(row)
    w.writerow(staging)


if __name__ == "__main__":
    input_name, output_name, blat, blon = parse_args(sys.argv[1:])
    bucket(input_name, output_name, blat, blon)
