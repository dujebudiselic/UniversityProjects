#!/usr/bin/perl

while (defined($redak = <>)) {

    chomp ($redak);
    if ($redak =~ /^JMBAG;/) {
        
    } else {
        ($jmbag, $prezime, $ime, $termin, $zakljucano) = split /;/, $redak;
        ($datum, $pocetak, $kraj, $ucionica) = split / /, $termin;
        ($god, $mj, $dan) = split /-/, $datum;
        ($sat, $min) = split /:/, $pocetak;

        ($datum_zak, $kraj_zak) = split / /, $zakljucano;
        ($god_zak, $mj_zak, $dan_zak) = split /-/, $datum_zak;
        ($sat_zak, $min_zak, $sec_zak) = split /:/, $kraj_zak;

        if ($god != $god_zak){
            print "$jmbag $prezime $ime - PROBLEM: $datum $pocetak --> $datum_zak $kraj_zak\n";
        } elsif ($mj != $mj_zak) {
            print "$jmbag $prezime $ime - PROBLEM: $datum $pocetak --> $datum_zak $kraj_zak\n";
        } elsif ($dan != $dan_zak) {
            print "$jmbag $prezime $ime - PROBLEM: $datum $pocetak --> $datum_zak $kraj_zak\n";
        } else {

            $vrijeme_sek_poc = $sat * 3600 + $min * 60;
            $vrijeme_sek_kraj = $sat_zak * 3600 + $min_zak * 60 + $sec_zak;

            $razlika = $vrijeme_sek_kraj - $vrijeme_sek_poc;

            if ($razlika > 3600 && $razlika >= 0) {
                print "$jmbag $prezime $ime - PROBLEM: $datum $pocetak --> $datum_zak $kraj_zak\n";
            }
        }
    }
    

}