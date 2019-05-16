#! /bin/bash

vitalsDir=$1

mkdir -p vitals

syndat="(^|:).*syndat.*(:|$)"
month="(^|:)[0-9]{2}(:|$)"
for yyyy in $vitalsDir/*/
do
  echo $(basename $yyyy)
  mkdir -p vitals/$(basename $yyyy)
  for mm in $yyyy*/
  do
    if [[ -d "$mm" && $(basename $mm) =~ $month ]]
    then
      for storm in $mm*
      do
        if [[ !( -d "$storm" || $storm =~ $syndat || $(basename $storm) == "*" ) ]]
        then
          cp $storm vitals/$(basename $yyyy)/$(basename $storm)
          awk '{ if ( $1 != "000" ) { print $0; } }' vitals/$(basename $yyyy)/$(basename $storm) > vitals/$(basename $yyyy)/$(basename $storm).tmp
          mv vitals/$(basename $yyyy)/$(basename $storm).tmp vitals/$(basename $yyyy)/$(basename $storm)
          awk -v yyyy=$(basename $yyyy) -v yy=$(basename $yyyy | cut -c3-4) '{ sub(/^yyyy/, yy, $4) }1' vitals/$(basename $yyyy)/$(basename $storm) > vitals/$(basename $yyyy)/$(basename $storm).tmp
          mv vitals/$(basename $yyyy)/$(basename $storm).tmp vitals/$(basename $yyyy)/$(basename $storm)
        fi
      done
    fi
  done
done