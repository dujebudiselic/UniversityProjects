#!/usr/bin/perl

print "Unesite niz znakova: ";
chomp($niz = <STDIN>);

print "Unesite broj ponavljanja: ";
chomp($n = <STDIN>);

foreach (1..$n) { 
    print "$niz\n";
}
