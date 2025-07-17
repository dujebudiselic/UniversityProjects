#!/bin/bash

proba="Ovo je proba"
echo $proba
echo

lista_datoteka=(*)
echo ${lista_datoteka[@]}
echo

proba3="${proba}. ${proba}. ${proba}."
echo $proba3
echo

a=4
b=3
c=7
d=$(((a + 4)*b%c))
echo $a $b $c $d
echo

broj_rijeci=$(cat *.txt | wc -w)
echo $broj_rijeci
echo

ls ~