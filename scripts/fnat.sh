#!/usr/bin/env bash
awk '
{nr = 100000 * $1 + $4}
FILENAME == ARGV[1] && (!(nr in done1)){done1[nr] = 1; counter++; contact[nr] = $1}
FILENAME == ARGV[2] && (!(nr in done2)) {done2[nr] = 1; if(nr in contact) natcounter++}
END
{print natcounter / counter}'

'refe.contacts' 'decoy.contacts'


awk '{nr = 100000 * $1 + $4} FILENAME == refe.contacts && (!(nr in done1)){done1[nr] = 1; counter++; contact[nr] = $1} FILENAME == decoy.contacts && (!(nr in done2)) {done2[nr] = 1; if(nr in contact) natcounter++} END {print natcounter / counter}'
'refe.contacts' 'decoy.contacts'