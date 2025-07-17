#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Unesite 1 argument"
    exit 1
fi

if [ ! -r "$1" ]; then
    echo "Unesite datoteku s podacima"
    exit 1
fi

datoteka="$1"

sed -E 's/^.*:x:.*:.*:.* ([a-zA-z]+):.*$/\1/' "$datoteka" | sort | uniq -c | sort -nr