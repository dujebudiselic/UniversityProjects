#!/usr/bin/perl

%podaci;
%mj_pret = (Jan => '01', Feb => '02', Mar => '03', Apr => '04', May => '05', Jun => '06', Jul => '07', Aug => '08', Sep => '09', Oct => '10', Nov => '11', Dec => '12');

while (defined($redak = <>)) {

    chomp ($redak);

    if ($redak =~ /\[(\d{2})\/(\w{3})\/(\d{4}):(\d{2}):/) {
        ($dan, $mj, $god, $sat) = ($1, $2, $3, $4);

        $mjesec = $mj_pret{$mj};
        $datum = "$god" . "-" . "$mjesec" . "-" . "$dan";

        $broj = $podaci{$datum}{$sat};
        $broj += 1;
        $podaci{$datum}{$sat} = $broj;
    }
}

foreach $datum (sort keys %podaci) {
    print " Datum : $datum\n";
    print " sat : broj pristupa\n";
    print "-------------------------------\n";

    foreach $sat (0..23) {
        if ($sat < 10) {
            $x = "0" . "$sat";
            if (defined($podaci{$datum}{$x})) {
                $broj = $podaci{$datum}{$x};
            } else {
                $broj = 0;
            }
            print "   $x : $broj\n";
        } else{
            if (defined($podaci{$datum}{$sat})) {
                $broj = $podaci{$datum}{$sat};
            } else {
                $broj = 0;
            }
            print "   $sat : $broj\n";
        }
    }
}
