#!/bin/bash
#./zadatak5.sh test5 '*.txt'

if [ "$#" -ne 2 ]; then
    echo "Krivi broj argumenta"
    exit 1
fi

kazalo="$1"
oblik="$2"

echo "Kazalo: $kazalo"
echo "Oblik datoteke: $oblik"

ukupno_redaka=0

for datoteka in $(find "$kazalo" -type f -name "$oblik"); do
    broj_redaka=$(wc -l < "$datoteka") 
    ukupno_redaka=$((ukupno_redaka + broj_redaka))
done

echo "Ukupan broj redaka u datotekama '$oblik' je $ukupno_redaka."
