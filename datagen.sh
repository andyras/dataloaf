#!/bin/bash

xs=(0.1 1.0 2.0)
ys=(0.1 1.0 2.0)

datadir=data2
[ -d ${datadir} ] && rm -rf ${datadir}
mkdir -p ${datadir}

for x in ${xs[@]}
do
  for y in ${ys[@]}
  do
    dir=${datadir}/x${x}_y${y}
    mkdir -p ${dir}
    echo $(echo "${x}*${y}" | bc) > ${dir}/dat.dat
    for ii in {0..10}
    do
      echo ${ii} $(echo "${RANDOM}%10" | bc) >> ${dir}/pts.dat
    done
  done
done
