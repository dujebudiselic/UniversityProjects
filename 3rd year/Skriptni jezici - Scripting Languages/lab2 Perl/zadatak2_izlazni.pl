#!/usr/bin/perl

$poruka = 0;
%broj_mailova;

while(defined($redak = <>)) {
    chomp($redak);

    if ($redak =~ /^\s+$/){
        $poruka = 0;
    }

    if ($redak =~ /^From nobody .*/) {
        $poruka = 1;
    }

    if ($poruka && $redak =~ /^From:\s*(.+)/) {
        $adresa_elektronicke_poste = $1;
        #print "$adresa_elektronicke_poste\n";
        if ($adresa_elektronicke_poste =~ /<(.+@.+?)>/){
            $mail = $1;
            #print "$mail\n";
            $broj = $broj_mailova{$mail};
            $broj += 1;
            $broj_mailova{$mail} = $broj;
        }

    }

}

@sort_broj_mailova = sort {$broj_mailova{$a} <=> $broj_mailova{$b}} keys % broj_mailova;

foreach $mail (@sort_broj_mailova) {
    $zvijezdice = '*' x $broj_mailova{$mail};
    printf "    %s: %s (%d)\n", $mail, $zvijezdice, $broj_mailova{$mail};
}