#!/bin/bash
#./zadatak3.sh test3

if [ "$#" -ne 1 ]; then
  echo "Krivi broj argumenta"
  exit 1
fi

if [ ! -d "$1" ]; then
  echo "Upišite ime direktorija u kojemu se nalaze log-datoteke"
  exit 1
fi

direktorij="$1"
#echo $direktorij

for datoteka in $(find "$direktorij" -type f -name "*_log*-02-*.txt"); do
  org_date=$(echo "$datoteka" | sed -En 's/.*([0-9]{4}-[0-9]{2}-[0-9]{2}).*/\1/p')
  date=$(echo "$org_date" | sed -En 's/([0-9]{4})-([0-9]{2})-([0-9]{2})/\3-\2-\1/p')
  
  echo "datum: $date"
  echo "--------------------------------------------------"
  sed -En 's/.*"(GET|POST|HEAD) ([^"]+ HTTP\/[0-9\.]+)".*/\1 \2/p' "$datoteka" | sort | uniq -c | sort -nr | sed 's/\([0-9]\+\) \(.*\)/\1 : \2/'
  echo
done
