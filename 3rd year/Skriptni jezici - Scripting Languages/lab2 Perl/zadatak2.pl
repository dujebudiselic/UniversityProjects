#!/usr/bin/perl

print "Unesite niz brojeva: ";
chomp($niz = <STDIN>);

@brojevi = split /\s+/, $niz;

$zbroj = 0;
foreach $x (@brojevi) {
    $zbroj += $x
}

$n = @brojevi;
$prosjek = $zbroj / $n;

print "Aritmetička sredina je: $prosjek\n";
