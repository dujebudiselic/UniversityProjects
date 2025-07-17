#!/bin/bash
#./zadatak6.sh dir1 dir2

if [ "$#" -ne 2 ]; then
    echo "Krivi broj argumenta"
    exit 1
fi

if [ ! -d "$1" ]; then
  echo "Upišite imena direktorija koje želite sinkronizirati"
  exit 1
fi

if [ ! -d "$2" ]; then
  echo "Upišite imena direktorija koje želite sinkronizirati"
  exit 1
fi

direktorij1="$1"
direktorij2="$2"
#echo $direktorij1
#echo $direktorij2

for datoteka1 in $(find "$direktorij1" -type f); do
  datoteka2="$direktorij2/$(echo "$datoteka1" | sed 's/.*\///')"
  if [ -f "$datoteka2" ]; then   
    if [ "$datoteka1" -nt "$datoteka2" ]; then
      echo "$datoteka1 --> $direktorij2"
    fi
  else 
    echo "$datoteka1 --> $direktorij2"
  fi
done

for datoteka2 in $(find "$direktorij2" -type f); do
  datoteka1="$direktorij1/$(echo "$datoteka2" | sed 's/.*\///')"
  if [ -f "$datoteka1" ]; then 
    if [ "$datoteka2" -nt "$datoteka1" ]; then
      echo "$datoteka2 --> $direktorij1"
    fi
  else
    echo "$datoteka2 --> $direktorij1"
  fi
done
