#!/usr/bin/env bash

red='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${red}START: re-sampleing and cliping${NC}"
for i in $(ls -d *); do
if [[ $i != "process.sh" ]]; then
    cd $i; printf "$i\n"
    for j in *.au ; do
      NAME=$(echo $j | cut -f 1-2 -d '.')
      echo $NAME
      sox -r 22050 $j "$NAME"_clip1.au trim 0 3
      sox -r 22050 $j "$NAME"_clip2.au trim 3 3
      sox -r 22050 $j "$NAME"_clip3.au trim 6 3
      sox -r 22050 $j "$NAME"_clip4.au trim 9 3
      sox -r 22050 $j "$NAME"_clip5.au trim 12 3
      sox -r 22050 $j "$NAME"_clip6.au trim 15 3
      sox -r 22050 $j "$NAME"_clip7.au trim 18 3
      sox -r 22050 $j "$NAME"_clip8.au trim 21 3
      sox -r 22050 $j "$NAME"_clip9.au trim 24 3
      sox -r 22050 $j "$NAME"_clip10.au trim 27 3
    done
    cd ..
fi
done
wait

echo -e "${red}START: make new directories${NC}"
mkdir ../genres_processed
for i in *; do
  if [[ $i != "process.sh" ]]; then
    mkdir ../genres_processed/$i
  fi
done
wait

echo -e "${red}START: move files${NC}"
for i in $(ls -d *); do
if [[ $i != "process.sh" ]]; then
    mv $i/*_clip* ../genres_processed/$i
fi
done
wait