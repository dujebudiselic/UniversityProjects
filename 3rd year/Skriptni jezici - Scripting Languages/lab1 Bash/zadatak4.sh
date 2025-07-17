#!/bin/bash
#./zadatak4.sh Slike

if [ "$#" -ne 1 ]; then
  echo "Krivi broj argumenta"
  exit 1
fi

if [ ! -d "$1" ]; then
  echo "Upišite ime direktorija u kojemu se nalaze slike"
  exit 1
fi

direktorij="$1"
#echo $direktorij

fotografije=( $(ls "$direktorij" | sort -k1,1 -k2,2 -t '_') )
mjeseci_godina=()

for slika in "${fotografije[@]}"; do
  mjesec_godina=$(echo "$slika" | sed -E 's/^([0-9]{4})([0-9]{2})[0-9]{2}_.*/\2-\1/')
  postoji_datum=false
  for i in "${mjeseci_godina[@]}"; do
    if [[ "$i" == "$mjesec_godina" ]]; then
      postoji_datum=true
      break  
    fi
  done

  if [ "$postoji_datum" = false ]; then
    mjeseci_godina+=("$mjesec_godina")
  fi
done

#echo ${mjeseci_godina[@]}

for mjesec_godina in "${mjeseci_godina[@]}"; do
  echo "$mjesec_godina :"
  echo "----------"
  numeracija=1
  broj_foto=0
  for slika in "${fotografije[@]}"; do
    trenutni_mjesec_godina=$(echo "$slika" | sed -E 's/^([0-9]{4})([0-9]{2})[0-9]{2}_.*/\2-\1/')
    if [ "$trenutni_mjesec_godina" == "$mjesec_godina" ]; then
      echo "  $numeracija. $slika"
      numeracija=$((numeracija + 1))
      broj_foto=$((broj_foto + 1))
    fi
  done
  echo "--- Ukupno: $broj_foto slika -----"
  echo
done
