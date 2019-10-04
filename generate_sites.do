#
awk -F, '{printf("'\'%s\':'\n"),$1,$3,$4,$5}' telescopes-opticon.csv

