#!/bin/bash

grep -Ei 'banana|jabuka|jagoda|dinja|lubenica' namirnice.txt
echo

grep -Ei -v 'banana|jabuka|jagoda|dinja|lubenica' namirnice.txt
echo

grep -E -r '\<[A-Z]{3}[0-9]{6}\>' ~/projekti/
echo

find . -type f -mtime +7 -mtime -14 -ls
echo

for i in {1..15}; do echo $i; done
echo

kraj=15
for i in $(seq 1 $kraj); do echo $i; done
# -bash: 1..15: command not found
for i in $(1..$kraj); do echo $i; done

