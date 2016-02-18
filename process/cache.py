import csv, getopt, sys
import operator
import copy

def parse_args(argv):
    input_name = ''
    output_name = ''
    cache_name = ''
    blat = 30   # default
    blon = 60   # default
    depth = 1   # default
    try:
        arg_str = "h:i:o:c:m:n:d:"
        arg_list = ["help", "inputfile=","outputfile=", "cachefile=", "blat=", "blon=", "depth="]
        opts, args = getopt.getopt(argv, arg_str, arg_list)
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-i", "--inputfile"):
            input_name = arg
        elif opt in ("-o", "--outputfile"):
            output_name = arg
        elif opt in ("-c"):
            cache_name = arg
        elif opt in ("-m"):
            blat = int(arg)
        elif opt in ("-n"):
            blon = int(arg)
        elif opt in ("-d"):
            depth = int(arg)
        else:
            usage()
            sys.exit(2)

    return input_name, output_name, cache_name, blat, blon, depth

def usage():
    help_str = 'cache.py -i <inputfile> -o <outputfile> -c <cachefile> -m <blat> -n <blon> -d <depth>'
    print(help_str)

def cache(input_name, output_name, cache_name, blat, blon, depth):
    with open(input_name) as input_file:
        with open(output_name, 'w') as output_cities:
            with open(cache_name, 'w') as output_cache:
                reader = csv.reader(input_file, delimiter='\t')
                city_list = sorted(reader, key=lambda row: int(row[0]), reverse=False)

                caching = 0
                caching_max = blat * blon * 4
                while (caching < caching_max):
                    nset = neighbors( Bucket(caching, blat, blon), depth )
                    lset = search(city_list, nset)
                    staging = [form(lset)]
                    cache_writer = csv.writer(output_cache, delimiter='\t')
                    cache_writer.writerow(staging)
                    caching += 1
                    # write : index, search city list,
                    # list of line numbers in city data -- empty if no matching cities
                    # eventually add region data to cache

                city_writer = csv.writer(output_cities, delimiter='\t')
                for row in city_list:
                    city_writer.writerow(row)

def form(lset):
    sorted_list = sorted(lset)
    staging = ""
    first = True
    for x in sorted_list:
        if first:
            staging += str(x)
            first = False
        else:
            staging += "," + str(x)
    return staging


def search(city_list, nset):
    lset = set()
    i = 0
    for row in city_list:
        if int(row[0]) in nset:
            lset.add(i)
            try:
                nset.remove(int(row[0])) # only get the first occurence
            except KeyError:
                pass
        i += 1
    return lset

def neighbors(center, depth):
    # center is a bucket
    # depth layers from center to go
    # returns set of region indices
    nset = {center.index}
    while (depth > 0):
        nset_temp = copy.deepcopy(nset)
        for neighbor in nset:
            buck = Bucket( neighbor, center.blat, center.blon )
            nset_temp.add( buck.get_n() )
            nset_temp.add( buck.get_s() )
            nset_temp.add( buck.get_e() )
            nset_temp.add( buck.get_w() )
            nset_temp.add( buck.get_ne() )
            nset_temp.add( buck.get_nw() )
            nset_temp.add( buck.get_se() )
            nset_temp.add( buck.get_sw() )
        nset = nset.union(nset_temp)
        depth -= 1
    return nset

class Bucket:
    def __init__(self, index, blat, blon):
        self.index = index
        self.blat = blat
        self.blon = blon

    def get_quad(self):
        return self.index // self.blat // self.blon

    def same_quad_of(self, maybe_i):
        maybe_buck = Bucket(maybe_i, self.blat, self.blon)
        return self.get_quad() == maybe_buck.get_quad()

    def get_row(self):
        return self.index // self.blon + 1 * self.get_lat_mult()

    def same_row_of(self, maybe_i):
        maybe_buck = Bucket(maybe_i, self.blat, self.blon)
        return self.get_row() == maybe_buck.get_row()

    def get_lat_mult(self):
        q = self.get_quad()
        if q == 0 or q == 1:
            return 1
        else:
            return -1

    def get_lon_mult(self):
        q = self.get_quad()
        if q == 0 or q == 3:
            return 1
        else:
            return -1

    def get_n(self):
        return self.get_vert(True)

    def get_s(self):
        return self.get_vert(False)

    def get_vert(self, north):
        direction = 1
        if north == False:
            direction = -1
        maybe_v = self.index + self.blon * direction * self.get_lat_mult()
        if self.same_quad_of(maybe_v):
            return maybe_v
        else:
            mult = self.get_lat_mult() * self.get_lon_mult()
            qsize = self.blat * self.blon
            v = (self.index - qsize * mult) % (qsize * 4)
            return v

    def get_e(self):
        return self.get_horz(True)

    def get_w(self):
        return self.get_horz(False)

    def get_horz(self, east):
        direction = 1
        if east == False:
            direction = -1
        maybe_h = self.index + 1 * direction * self.get_lon_mult()
        if self.same_row_of(maybe_h):
            return maybe_h
        else:
            mult = self.get_lat_mult() * self.get_lon_mult()
            qsize = self.blat * self.blon
            h = self.index + qsize * mult
            return h

    def get_ne(self):
        return Bucket( self.get_n(), self.blat, self.blon ).get_e()

    def get_nw(self):
        return Bucket( self.get_n(), self.blat, self.blon ).get_w()

    def get_se(self):
        return Bucket( self.get_s(), self.blat, self.blon ).get_e()

    def get_sw(self):
        return Bucket( self.get_s(), self.blat, self.blon ).get_w()



if __name__ == "__main__":
    input_name, output_name, cache_name, blat, blon, depth = parse_args(sys.argv[1:])
    cache(input_name, output_name, cache_name, blat, blon, depth)
    # a = Bucket(int(blat), 2, 3)
    # nset = neighbors(a, 2)
    # print("N = ",nset)
