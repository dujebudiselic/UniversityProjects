#!/usr/bin/perl

%studenti;
$fak = 1;
while (defined($redak = <>)) {

    chomp ($redak);
    if(!($redak =~ /^#/ || $redak =~ /^\s*$/)){
        if($fak){
            #print "$fak\n";
            @faktori = split /;/, $redak;
            $fak = 0;
        } else {
            ($jmbag, $prezime, $ime, @rez) = split /;/, $redak;
            $ukupan_rez = 0;
            foreach $i (0 .. $#faktori) {
                if ($rez[$i] ne '-') {
                    $ukupan_rez += $rez[$i] * $faktori[$i];
                }
            }
            $key = "$prezime" . ";" . "$ime" . ";" . "$jmbag";
            $studenti{$key} = $ukupan_rez;
        }
    
    }

}

#print "stud %studenti\n";
@sort_studenti = sort { $studenti{$b} <=> $studenti{$a} } keys %studenti;
#print "stud @sort_studenti\n";

print "Lista po rangu:\n";
print "-------------------\n";
$rank = 1;
foreach $student (@sort_studenti) {
    ($prezime, $ime, $jmbag) = split /;/, $student;
    printf "  %d. %s, %s (%s) : %.2f\n", $rank, $prezime, $ime, $jmbag, $studenti{$student};
    $rank += 1;
    
}

