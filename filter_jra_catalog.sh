#! /bin/bash

vitalsDir=$1
windDir=$2

for yyyy in $vitalsDir/*/
do
  for file in $yyyy*
  do
    if [ ! -d "$file" ]
    then
      read -r start1 end1 start2 end2 <<<$(./get_jra_dates.py $file)
      echo $start1
      echo $end1
      echo $start2
      echo $end1
      ./filter-jra.py \
        $windDir/uas_input4MIPs_atmosphericState_OMIP_MRI-JRA55-do-1-3_gn_$start1-$end1.padded.filt.nc \
        $windDir/uas_input4MIPs_atmosphericState_OMIP_MRI-JRA55-do-1-3_gn_$start2-$end2.padded.filt.nc \
        uas \
        $file
      ./filter-jra.py \
        $windDir/vas_input4MIPs_atmosphericState_OMIP_MRI-JRA55-do-1-3_gn_$start1-$end1.padded.filt.nc \
        $windDir/vas_input4MIPs_atmosphericState_OMIP_MRI-JRA55-do-1-3_gn_$start2-$end2.padded.filt.nc \
        vas \
        $file
    fi
  done
done