#!/bin/bash
PPOLDDIR=`pwd`

echo $PPOLDDIR
cd delphes
pwd
source DelphesEnv.sh
./configure
sed -i -e 's/c++0x/c++1y/g' Makefile
make -j4  
cd $PPOLDDIR
source env.sh

cd $DANALYSISPATH
pwd
make -j3
cd $PPOLDDIR/ntupler
pwd
make -j3
cd -
