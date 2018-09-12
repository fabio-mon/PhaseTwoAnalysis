#!/usr/bin/env python
import os, re
import commands
import math, time
import sys
import argparse
import subprocess

parser = argparse.ArgumentParser(description='This script splits ntupler tasks in multiple jobs and sends them on LXBATCH')

parser.add_argument("-l", "--label",          required=True,     type=str,  help="job label")
parser.add_argument("-e", "--exe",            required=True,     type=str,  help="executable")
parser.add_argument("-i", "--input",          required=True,     type=str,  help="input folder or file (eg: /store/...)")
parser.add_argument("-p", "--proxy",          required=True,     type=str,  help="proxy filename to access grid ")
parser.add_argument("-loc", "--location",          required=True,     type=str,  help="eos location of files ( fnal.gov , cern.ch , desy.de)")
parser.add_argument("-o", "--outputFolder",   required=True,     type=str,  help="folder where to store output files")
#parser.add_argument("-f", "--outputFileName", required=True,     type=str,  help="base name of output files [outputFileName]_i.root")
parser.add_argument("-c", "--configFile",     required=True,     type=str,  help="config file to be run")
#parser.add_argument("-n", "--nJobs",          required=True,     type=int,  help="number of jobs")
#parser.add_argument("-N", "--nEvents",        required=True,     type=int,  help="number of events per job")
parser.add_argument("-q", "--queue",          default="1nd",     type=str,  help="lxbatch queue to use")
parser.add_argument("-s", "--submit",                                       help="submit jobs", action='store_true')
parser.add_argument("-v", "--verbose",                                      help="increase output verbosity", action='store_true')


args = parser.parse_args()


print 
print 'START'
print 

currDir = os.getcwd()

print

try:
   subprocess.check_output(['mkdir','jobs'])
except subprocess.CalledProcessError as e:
   print e.output
try:
   subprocess.check_output(['mkdir','jobs/'+args.label])
except subprocess.CalledProcessError as e:
   print e.output
try:
   subprocess.check_output(['mkdir',args.outputFolder])
except subprocess.CalledProcessError as e:
   print e.output
try:
   subprocess.check_output(['mkdir',args.outputFolder+"/"+args.label+"/"])
except subprocess.CalledProcessError as e:
   print e.output

##### produce list of input files
   os.system("rm inputfilelist.txt")
   os.system("echo empty > inputfilelist.txt")
   if(args.location=="fnal.gov"):
      os.system("eos root://cmseos."+args.location+" ls "+args.input+" > inputfilelist.txt")
   elif(args.location=="cern.ch"):
      os.system("eos ls "+args.input+" > inputfilelist.txt")
   elif(args.location=="desy.de"):
      os.system("gfal-ls srm://dcache-se-cms.desy.de/pnfs/desy.de/cms/tier2"+args.input+" > inputfilelist.txt")

##### loop for creating and sending jobs --> one file per job #####
i=0
with open("inputfilelist.txt") as filelist:
   for filename in filelist:   
      
      filename=filename.replace("\n","")
      ##### creates directory and file list for job #######
      jobDir = currDir+'/jobs/'+args.label+'/job_'+str(i)
      os.system('mkdir '+jobDir)
      os.chdir(jobDir)
   
      ##### copy executable to the jobDir ######
      os.system('cp '+args.exe+' '+jobDir+"/executable.exe")

      ##### copy proxyfile to the jobDir ######
      os.system("cp /tmp/"+args.proxy+' '+jobDir+"/")
   
      ##### creates ntupler config file #######
      with open(args.configFile) as fi:
         contents = fi.read()
         if(args.location=="fnal.gov"):
            replaced_contents = contents.replace("SAMPLESDIR", "root://cmseos."+args.location+"//"+args.input+"/")
         elif(args.location=="cern.ch"):
            replaced_contents = contents.replace("SAMPLESDIR", "/eos/cms/"+args.input+"/")
         elif(args.location=="desy.de"):
            replaced_contents = contents.replace("SAMPLESDIR", "root://cms-xrd-global.cern.ch/"+args.input+"/")
         replaced_contents = replaced_contents.replace("FILENAME", filename)
         replaced_contents = replaced_contents.replace("LABEL", args.label)
         #replaced_contents = replaced_contents.replace('OUTPUT_PATH', str(args.outputFolder+args.label+"/"))
         with open(jobDir+"/config.cfg", "w") as fo:
            fo.write(replaced_contents)
   
      ##### creates jobs #######
      with open('job_'+str(i)+'.sh', 'w') as fout:
         fout.write("#!/bin/sh\n")
         fout.write("echo\n")
         fout.write("echo 'START---------------'\n")
         fout.write("workdir=$PWD\n")
         fout.write("echo 'current dir: ' ${workdir}\n")
         fout.write("export XRD_NETWORKSTACK=IPv4\n")
         fout.write("cd /afs/cern.ch/user/f/fmonti/work/myPhaseTwoAnalysis/CMSSW_9_3_2/src/PhaseTwoAnalysis/delphesInterface/\n")
         fout.write("eval `scram runtime -sh`\n")
         fout.write("source $CMSSW_BASE/src/PhaseTwoAnalysis/delphesInterface/env.sh\n")
         fout.write("cd $workdir\n")
         fout.write("export X509_USER_PROXY="+jobDir+"/"+args.proxy+"\n")
         fout.write("mkdir "+str(args.outputFolder+"/"+args.label)+"\n")
         #fout.write("cd "+str(jobDir)+"\n")
         #fout.write("echo 'current dir: ' ${PWD}\n")
         #fout.write("./executable.exe config.cfg\n")#+args.outputFolder+"/"+args.label+"/"+args.outputFileName+"_"+str(x)+"\n")
         fout.write(jobDir+"/executable.exe "+jobDir+"/config.cfg\n")
         fout.write("ls out/ | grep p2ntuple | grep .root | awk '{print \"mv out/\"$0\" "+args.outputFolder+"/"+args.label+"/"+filename.replace(".root","")+"_\"$0}' | /bin/sh\n")
         #fout.write("mv *.root " +str(args.outputFolder+args.label)+"\n")
         fout.write("echo 'STOP---------------'\n")
         fout.write("echo\n")
         fout.write("echo\n")

      os.system("chmod 755 job_"+str(i)+".sh")
   
      ###### sends bjobs ######
      if args.submit:
         os.system("bsub -q "+args.queue+" job_"+str(i)+".sh")
         print "job nr. " + str(i) + " submitted"
      
      i=i+1

   #os.chdir("../..")
   
print
print "your jobs:"
os.system("bjobs")
print
print 'END'
print
