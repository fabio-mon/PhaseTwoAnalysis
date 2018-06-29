#!/bin/bash
workdir=$PWD
proxy_name=$1
echo $workdir
export XRD_NETWORKSTACK=IPv4
cd /afs/cern.ch/user/f/fmonti/work/myPhaseTwoAnalysis/CMSSW_9_3_2/src/PhaseTwoAnalysis/delphesInterface/
eval `scram runtime -sh`
source env.sh
echo $PWD
cd $workdir
#export X509_USER_PROXY=./x509up_u80927
export X509_USER_PROXY=/afs/cern.ch/user/f/fmonti/work/myPhaseTwoAnalysis/CMSSW_9_3_2/src/PhaseTwoAnalysis/delphesInterface/ntupler/proxy/$proxy_name

/afs/cern.ch/user/f/fmonti/work/myPhaseTwoAnalysis/CMSSW_9_3_2/src/PhaseTwoAnalysis/delphesInterface/ntupler/ntupler /afs/cern.ch/user/f/fmonti/work/myPhaseTwoAnalysis/CMSSW_9_3_2/src/PhaseTwoAnalysis/delphesInterface/ntupler/config/dumpdelphes_GJet_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_200PU_skim2G2J_newntuples_lxbatchtest.txt

cp -r out/* /eos/user/f/fmonti/HHGGBB/data/DelphesDump_lxbatchtest/