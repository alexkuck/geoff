#!/bin/bash
BLAT=30
BLON=60
mkdir temp
wget http://download.geonames.org/export/dump/cities15000.zip -P temp
unzip temp/cities15000.zip -d temp/

echo -e "\nprocessing downloaded data ......"

echo "cleaning city data .............."
python3 process/clean.py -i temp/cities15000.txt -o temp/cleaned

echo "sorting cities by population ...."
python3 process/sort.py -i temp/cleaned -o temp/sorted

echo "bucketing cities ................ blat, blon == $BLAT, $BLON "
python3 process/bucket.py -i temp/sorted -o temp/bucketed -m $BLAT -n $BLON

echo "chopping cities by population ..."
python3 process/chop.py -i temp/bucketed -o temp/chopped

D_DIR="processed_data"
S_DIR=$D_DIR/small
M_DIR=$D_DIR/medium
L_DIR=$D_DIR/large
ALL_DIR=$D_DIR/all

mkdir -p "$S_DIR"
mkdir -p "$M_DIR"
mkdir -p "$L_DIR"
mkdir -p "$ALL_DIR"

echo "caching small city list ........."
python3 process/cache.py -i temp/chopped_S -o $S_DIR/cities -c $S_DIR/cache -m $BLAT -n $BLON -d 1

echo "caching medium city list ........ [may take a while]"
python3 process/cache.py -i temp/chopped_M -o $M_DIR/cities -c $M_DIR/cache -m $BLAT -n $BLON -d 1

echo "caching large city list ......... [may take a while]"
python3 process/cache.py -i temp/chopped_L -o $L_DIR/cities -c $L_DIR/cache -m $BLAT -n $BLON -d 1

echo "caching all city list ........... [may take a while]"
python3 process/cache.py -i temp/chopped_ALL -o $ALL_DIR/cities -c $ALL_DIR/cache -m $BLAT -n $BLON -d 1

echo "remove temporary files .........."
rm -rf temp

echo -e "DONE!\n"
