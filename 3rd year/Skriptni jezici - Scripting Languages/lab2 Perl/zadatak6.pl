#!/usr/bin/perl

use utf8;
use open ':locale';
use locale;

$duljina_prefiks = pop @ARGV;
%broj_rijeci;

while (defined($redak = <>)) {

    chomp ($redak);
    $redak = lc($redak); 
    $redak =~ s/[^[:alpha:]\s]+/ /g; 

    @rijeci = split /\s+/, $redak;
    foreach $rijec (@rijeci) {
        if ($rijec =~ /^(.{$duljina_prefiks})/) {
            $prefiks = $1;
            $broj = $broj_rijeci{$prefiks};
            $broj += 1;
            $broj_rijeci{$prefiks} = $broj;
        } 
    }
    
}

foreach $prefiks (sort keys %broj_rijeci) {
    print "$prefiks : $broj_rijeci{$prefiks}\n";
}