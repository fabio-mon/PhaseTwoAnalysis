import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing

options = VarParsing ('python')
options.register('outFileName', 'FullSim_GG_HH_2B2Gamma_GEN_SIM_RECO_PU0_fullProd_200PU.root',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "Output file name"
                 )
options.register('inputFormat', 'PAT',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "format of the input files (PAT or RECO)"
                 )
options.register('skim', True,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.bool,
                 "skim events with one lepton and 2 jets"
                 )
options.register('updateJEC', '',
                 VarParsing.multiplicity.list,
                 VarParsing.varType.string,
                 "Name of the SQLite file (with path and extension) used to update the jet collection to the latest JEC and the era of the new JEC"
                )
options.parseArguments()

if len(options.updateJEC)==0:
    standardjec='PhaseTwoAnalysis/NTupler/data/PhaseIIFall17_V3_MC.db'
    standardjec_tag='PhaseIIFall17_V3_MC'
    options.updateJEC=[standardjec,standardjec_tag]
    

process = cms.Process("MiniAnalysis")

# Geometry, GT, and other standard sequences
process.load('Configuration.Geometry.GeometryExtended2023D17Reco_cff')
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.load("TrackingTools/TransientTrack/TransientTrackBuilder_cfi")
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '93X_upgrade2023_realistic_v2', '')

# Log settings
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
#process.MessageLogger.cerr.threshold = 'INFO'
process.MessageLogger.categories.append('MyAna')
process.MessageLogger.cerr.INFO = cms.untracked.PSet(
        limit = cms.untracked.int32(0)
)

# Input
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(200) ) 

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17MiniAOD/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/MINIAODSIM/PU200_93X_upgrade2023_realistic_v2-v2/150000/32ABF802-5AC0-E711-9C75-44A842CFD60C.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17MiniAOD/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/MINIAODSIM/PU200_93X_upgrade2023_realistic_v2-v2/150000/38578234-1AC0-E711-8A28-6C3BE5B56498.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17MiniAOD/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/MINIAODSIM/PU200_93X_upgrade2023_realistic_v2-v2/150000/3CA0A05A-74C0-E711-8DD2-B499BAAC0612.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17MiniAOD/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/MINIAODSIM/PU200_93X_upgrade2023_realistic_v2-v2/150000/4814068A-C3C0-E711-A347-24B6FDFF1921.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17MiniAOD/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/MINIAODSIM/PU200_93X_upgrade2023_realistic_v2-v2/150000/4A52626B-F1BF-E711-AD91-B499BAAC0612.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17MiniAOD/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/MINIAODSIM/PU200_93X_upgrade2023_realistic_v2-v2/150000/50DC291C-34C0-E711-A57C-001E0B616BB2.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17MiniAOD/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/MINIAODSIM/PU200_93X_upgrade2023_realistic_v2-v2/150000/6657493D-71C0-E711-AF4A-B499BAAC0068.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17MiniAOD/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/MINIAODSIM/PU200_93X_upgrade2023_realistic_v2-v2/150000/C2CB68EB-4FC1-E711-B372-2C768AAF879E.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17MiniAOD/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/MINIAODSIM/PU200_93X_upgrade2023_realistic_v2-v2/150000/D0C8B86E-B2C1-E711-BCEE-484D7E8DF0E0.root'),
    secondaryFileNames = cms.untracked.vstring(
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/0080FB00-25BB-E711-BBE2-0242AC1C0503.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/043256E5-ADBA-E711-AF14-0242AC1C0501.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/0665F575-E4BA-E711-9E11-0242AC1C0502.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/08E28D78-30B9-E711-AF9A-008CFAFBFCF0.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/0A132E65-7FB9-E711-AB10-A0369FD20744.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/0E6A1571-E4BA-E711-B3DD-0242AC1C0500.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/0EFB8E16-3EBB-E711-82CB-0242AC1C0501.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/12FD7A9A-E6BA-E711-B8BC-0242AC1C0503.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/149BEBAA-20BA-E711-9BD5-3417EBE51D1E.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/1A479D44-83B9-E711-9254-10983627C3E8.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/1AD7B1BA-99BA-E711-A9D4-0242AC1C0503.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/1CF56365-E5BA-E711-8FF2-0242AC1C0503.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/22307725-82B9-E711-92E7-F4E9D497BBE0.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/22407BE1-4BBB-E711-BC23-0242AC1C0501.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/224B1B46-2AB9-E711-B64A-008CFAF72A64.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/22D0EE91-07BA-E711-B281-A4BF0112BE32.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/2622323D-3CB9-E711-9A9B-A0369FC522F0.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/2828740D-6AB7-E711-B74B-7CD30ABD2EE8.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/287E1B86-55BA-E711-AD7F-A4BF0112DD8C.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/2EE966AB-88B9-E711-8FA1-3417EBE51D1E.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/30746176-E4BA-E711-B6EC-0242AC1C0500.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/32468AB7-A1BA-E711-AD96-0242AC1C0500.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/34478468-E4BA-E711-BF56-0242AC1C0500.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/365F6023-E7B6-E711-9055-E0071B7AB780.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/36D33646-81B9-E711-849F-7CD30AC0301A.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/3800D728-7FB9-E711-91E4-A0369FC5252C.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/3C9E4978-84B9-E711-985F-A0369FD20DA0.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/3CF43F3C-91BA-E711-BDF4-0242AC1C0503.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/3E1F78A9-E6BA-E711-8542-0242AC1C0501.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/3E3A61D1-89B9-E711-8908-008CFAF5592A.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/4002B100-3CB9-E711-96E3-A0369F6367C2.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/46614C6F-E4BA-E711-B0D7-0242AC1C0502.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/469BB656-3CB9-E711-BD44-00266CF89130.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/46B079A9-D4B9-E711-AB2E-3417EBE51BD1.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/4AEBD953-81B9-E711-BFF7-7CD30AC030A2.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/4CFC807A-E5BA-E711-A3A7-0242AC1C0501.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/4E9F9B16-9AB9-E711-9819-A0369F5BD91C.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/54975289-7BBA-E711-A50E-0242AC1C0501.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/54CAF777-42B9-E711-A5D8-7CD30ABD2EEA.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/5833DA98-16BB-E711-B661-008CFAF29392.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/584BFAF7-10BB-E711-BB41-A4BF0112BCCA.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/5E342A6B-2BB9-E711-B8B2-008CFAF558EE.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/60BC9E82-8DB9-E711-BCAE-10983627C3CE.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/66643D65-E4BA-E711-A187-0242AC1C0501.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/68235236-D3BB-E711-8A5F-0242AC1C0501.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/688DD93D-46B9-E711-9D64-848F69FBC0FD.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/68F56157-E5BA-E711-984F-0242AC1C0500.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/6CC6657A-E4BA-E711-B354-0242AC1C0500.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/6E851B93-8DB9-E711-B1C9-A0369FD20730.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/7206CF38-82B9-E711-ACC9-F04DA27540BB.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/728766AF-7EBA-E711-A760-0242AC1C0505.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/74344330-E5BA-E711-90A1-0242AC1C0500.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/78585536-3BBB-E711-A4DA-0242AC1C0500.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/78DF96A4-E6BA-E711-AA4E-0242AC1C0503.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/7EC29DCE-DCB9-E711-9598-A4BF011257E0.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/80845630-99BA-E711-B5D0-0242AC1C050A.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/82CB1B43-F0BA-E711-B458-0242AC1C0503.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/82DB0D9B-8DB9-E711-8D15-00266CFBE29C.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/8459906D-E4BA-E711-8CA9-0242AC1C0504.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/883BA482-E4BA-E711-B7F0-0242AC1C0505.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/8863CB96-45BA-E711-86E9-A4BF0112DC34.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/8E0A8AD5-E5BA-E711-A622-0242AC1C0500.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/92450B40-D3BB-E711-8D81-0242AC1C0500.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/92B35CDF-E8BA-E711-B204-0242AC1C0501.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/9A0579CD-10BB-E711-8113-001E6779250C.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/9E79A9BC-65BA-E711-A17B-0242AC1C0501.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/A49B7420-7EB9-E711-AE6E-10983627C3DB.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/A6FF2367-E4BA-E711-A73B-0242AC1C0503.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/A85286BB-E7BA-E711-86A6-0242AC1C0500.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/AA953755-8FBA-E711-BBF2-0242AC1C0500.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/AAC26B6F-08B7-E711-983C-0242AC110002.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/ACE1830A-35BB-E711-B46E-0242AC1C0503.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/AEAE6A69-85BA-E711-A073-0242AC1C0500.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/B2A2DF0B-25BB-E711-9FFC-0242AC1C0502.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/B4094369-89B9-E711-9DF5-7CD30AC030A2.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/B4272800-25BB-E711-BB63-0242AC1C0500.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/B629B4E0-0ABA-E711-BFE2-A0369FC522F0.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/B807ACB8-8FBC-E711-B499-008CFAF74780.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/B8BB9435-88B9-E711-99C6-F04DA2753F56.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/C0A1DA2B-67BA-E711-BC1E-0242AC110002.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/C409281B-ECB9-E711-A8F3-A4BF0112BD04.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/C4398166-E4BA-E711-84E6-0242AC1C0502.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/C487B939-82B9-E711-BFA8-00266CFB9008.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/C4ECBA2B-26B8-E711-94DF-7CD30AC031E8.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/C647356B-E4BA-E711-97F0-0242AC1C0503.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/C65B5F64-E4BA-E711-871B-0242AC1C0500.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/C85A9465-E4BA-E711-905A-0242AC1C0502.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/C871FC74-7FB9-E711-A9B5-A0369FC5252C.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/C8A9F56E-E4BA-E711-8756-0242AC1C0500.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/C8ACDF47-DEB9-E711-9C3D-A0369FC5252C.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/C8DEFD5D-41B9-E711-B5C6-008CFAF558EE.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/CAF6620A-6CB8-E711-8D4D-3417EBE2ED22.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/CC9EDB0B-3FB7-E711-AADD-7CD30AC030A2.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/D43BAAFC-3CB9-E711-B807-A0369F63681A.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/D48B04D4-48B8-E711-992C-E0071B749C40.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/D64659C2-9AB6-E711-BC30-008CFAF228FA.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/D67E622D-E5BA-E711-B3FB-0242AC1C0501.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/D8E4884E-7FBC-E711-B6C0-0CC47AF9B32A.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/E088279E-E6BA-E711-ABC1-0242AC1C0503.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/E0E965FD-88BA-E711-A006-0242AC1C0503.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/E437DE3F-E5BA-E711-9A95-0242AC1C0501.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/E4BC3936-88B9-E711-AF4B-3417EBE34E8B.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/E6B2CE69-E4BA-E711-861A-0242AC1C0501.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/E8B8ED2F-D3BB-E711-940A-0242AC1C0502.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/F0A039D7-87BA-E711-B32C-0242AC1C0501.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/F2006E3A-D3BB-E711-8111-0242AC1C0501.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/F2A9C949-D3BB-E711-86C2-0242AC1C0500.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/F690B5A1-87BA-E711-A1C4-0242AC1C0501.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/F6BB41C4-E1B8-E711-AD4F-E0071B6C9DB0.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/FC1074CB-35BC-E711-A3F4-0CC47AF9B1B2.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/FC9DAD1E-E6BA-E711-8FAA-0242AC1C0501.root')
)
if (options.inputFormat.lower() == "reco"):
    process.source.fileNames = cms.untracked.vstring(*(
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/0080FB00-25BB-E711-BBE2-0242AC1C0503.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/043256E5-ADBA-E711-AF14-0242AC1C0501.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/0665F575-E4BA-E711-9E11-0242AC1C0502.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/08E28D78-30B9-E711-AF9A-008CFAFBFCF0.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/0A132E65-7FB9-E711-AB10-A0369FD20744.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/0E6A1571-E4BA-E711-B3DD-0242AC1C0500.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/0EFB8E16-3EBB-E711-82CB-0242AC1C0501.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/12FD7A9A-E6BA-E711-B8BC-0242AC1C0503.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/149BEBAA-20BA-E711-9BD5-3417EBE51D1E.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/1A479D44-83B9-E711-9254-10983627C3E8.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/1AD7B1BA-99BA-E711-A9D4-0242AC1C0503.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/1CF56365-E5BA-E711-8FF2-0242AC1C0503.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/22307725-82B9-E711-92E7-F4E9D497BBE0.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/22407BE1-4BBB-E711-BC23-0242AC1C0501.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/224B1B46-2AB9-E711-B64A-008CFAF72A64.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/22D0EE91-07BA-E711-B281-A4BF0112BE32.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/2622323D-3CB9-E711-9A9B-A0369FC522F0.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/2828740D-6AB7-E711-B74B-7CD30ABD2EE8.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/287E1B86-55BA-E711-AD7F-A4BF0112DD8C.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/2EE966AB-88B9-E711-8FA1-3417EBE51D1E.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/30746176-E4BA-E711-B6EC-0242AC1C0500.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/32468AB7-A1BA-E711-AD96-0242AC1C0500.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/34478468-E4BA-E711-BF56-0242AC1C0500.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/365F6023-E7B6-E711-9055-E0071B7AB780.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/36D33646-81B9-E711-849F-7CD30AC0301A.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/3800D728-7FB9-E711-91E4-A0369FC5252C.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/3C9E4978-84B9-E711-985F-A0369FD20DA0.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/3CF43F3C-91BA-E711-BDF4-0242AC1C0503.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/3E1F78A9-E6BA-E711-8542-0242AC1C0501.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/3E3A61D1-89B9-E711-8908-008CFAF5592A.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/4002B100-3CB9-E711-96E3-A0369F6367C2.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/46614C6F-E4BA-E711-B0D7-0242AC1C0502.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/469BB656-3CB9-E711-BD44-00266CF89130.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/46B079A9-D4B9-E711-AB2E-3417EBE51BD1.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/4AEBD953-81B9-E711-BFF7-7CD30AC030A2.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/4CFC807A-E5BA-E711-A3A7-0242AC1C0501.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/4E9F9B16-9AB9-E711-9819-A0369F5BD91C.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/54975289-7BBA-E711-A50E-0242AC1C0501.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/54CAF777-42B9-E711-A5D8-7CD30ABD2EEA.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/5833DA98-16BB-E711-B661-008CFAF29392.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/584BFAF7-10BB-E711-BB41-A4BF0112BCCA.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/5E342A6B-2BB9-E711-B8B2-008CFAF558EE.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/60BC9E82-8DB9-E711-BCAE-10983627C3CE.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/66643D65-E4BA-E711-A187-0242AC1C0501.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/68235236-D3BB-E711-8A5F-0242AC1C0501.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/688DD93D-46B9-E711-9D64-848F69FBC0FD.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/68F56157-E5BA-E711-984F-0242AC1C0500.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/6CC6657A-E4BA-E711-B354-0242AC1C0500.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/6E851B93-8DB9-E711-B1C9-A0369FD20730.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/7206CF38-82B9-E711-ACC9-F04DA27540BB.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/728766AF-7EBA-E711-A760-0242AC1C0505.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/74344330-E5BA-E711-90A1-0242AC1C0500.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/78585536-3BBB-E711-A4DA-0242AC1C0500.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/78DF96A4-E6BA-E711-AA4E-0242AC1C0503.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/7EC29DCE-DCB9-E711-9598-A4BF011257E0.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/80845630-99BA-E711-B5D0-0242AC1C050A.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/82CB1B43-F0BA-E711-B458-0242AC1C0503.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/82DB0D9B-8DB9-E711-8D15-00266CFBE29C.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/8459906D-E4BA-E711-8CA9-0242AC1C0504.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/883BA482-E4BA-E711-B7F0-0242AC1C0505.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/8863CB96-45BA-E711-86E9-A4BF0112DC34.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/8E0A8AD5-E5BA-E711-A622-0242AC1C0500.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/92450B40-D3BB-E711-8D81-0242AC1C0500.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/92B35CDF-E8BA-E711-B204-0242AC1C0501.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/9A0579CD-10BB-E711-8113-001E6779250C.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/9E79A9BC-65BA-E711-A17B-0242AC1C0501.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/A49B7420-7EB9-E711-AE6E-10983627C3DB.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/A6FF2367-E4BA-E711-A73B-0242AC1C0503.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/A85286BB-E7BA-E711-86A6-0242AC1C0500.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/AA953755-8FBA-E711-BBF2-0242AC1C0500.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/AAC26B6F-08B7-E711-983C-0242AC110002.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/ACE1830A-35BB-E711-B46E-0242AC1C0503.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/AEAE6A69-85BA-E711-A073-0242AC1C0500.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/B2A2DF0B-25BB-E711-9FFC-0242AC1C0502.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/B4094369-89B9-E711-9DF5-7CD30AC030A2.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/B4272800-25BB-E711-BB63-0242AC1C0500.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/B629B4E0-0ABA-E711-BFE2-A0369FC522F0.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/B807ACB8-8FBC-E711-B499-008CFAF74780.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/B8BB9435-88B9-E711-99C6-F04DA2753F56.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/C0A1DA2B-67BA-E711-BC1E-0242AC110002.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/C409281B-ECB9-E711-A8F3-A4BF0112BD04.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/C4398166-E4BA-E711-84E6-0242AC1C0502.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/C487B939-82B9-E711-BFA8-00266CFB9008.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/C4ECBA2B-26B8-E711-94DF-7CD30AC031E8.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/C647356B-E4BA-E711-97F0-0242AC1C0503.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/C65B5F64-E4BA-E711-871B-0242AC1C0500.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/C85A9465-E4BA-E711-905A-0242AC1C0502.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/C871FC74-7FB9-E711-A9B5-A0369FC5252C.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/C8A9F56E-E4BA-E711-8756-0242AC1C0500.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/C8ACDF47-DEB9-E711-9C3D-A0369FC5252C.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/C8DEFD5D-41B9-E711-B5C6-008CFAF558EE.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/CAF6620A-6CB8-E711-8D4D-3417EBE2ED22.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/CC9EDB0B-3FB7-E711-AADD-7CD30AC030A2.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/D43BAAFC-3CB9-E711-B807-A0369F63681A.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/D48B04D4-48B8-E711-992C-E0071B749C40.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/D64659C2-9AB6-E711-BC30-008CFAF228FA.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/D67E622D-E5BA-E711-B3FB-0242AC1C0501.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/D8E4884E-7FBC-E711-B6C0-0CC47AF9B32A.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/E088279E-E6BA-E711-ABC1-0242AC1C0503.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/E0E965FD-88BA-E711-A006-0242AC1C0503.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/E437DE3F-E5BA-E711-9A95-0242AC1C0501.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/E4BC3936-88B9-E711-AF4B-3417EBE34E8B.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/E6B2CE69-E4BA-E711-861A-0242AC1C0501.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/E8B8ED2F-D3BB-E711-940A-0242AC1C0502.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/F0A039D7-87BA-E711-B32C-0242AC1C0501.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/F2006E3A-D3BB-E711-8111-0242AC1C0501.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/F2A9C949-D3BB-E711-86C2-0242AC1C0500.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/F690B5A1-87BA-E711-A1C4-0242AC1C0501.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/F6BB41C4-E1B8-E711-AD4F-E0071B6C9DB0.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/FC1074CB-35BC-E711-A3F4-0CC47AF9B1B2.root',
'root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GluGluToHHTo2B2G_node_SM_14TeV-madgraph/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/150000/FC9DAD1E-E6BA-E711-8FAA-0242AC1C0501.root'))

# HGCAL EGamma ID
if (options.inputFormat.lower() == "reco"):
    process.load("RecoEgamma.Phase2InterimID.phase2EgammaRECO_cff")
else:
    process.load("RecoEgamma.Phase2InterimID.phase2EgammaPAT_cff")

process.options   = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
    allowUnscheduled = cms.untracked.bool(True)
)

# Get new JEC from an SQLite file rather than a GT
if options.updateJEC:
    from CondCore.DBCommon.CondDBSetup_cfi import *
    process.jec = cms.ESSource("PoolDBESSource",CondDBSetup,
                               connect = cms.string('sqlite_fip:'+options.updateJEC[0]),
                               toGet =  cms.VPSet(
            cms.PSet(record = cms.string("JetCorrectionsRecord"),
                     tag = cms.string("JetCorrectorParametersCollection_"+options.updateJEC[1]+"_AK4PFPuppi"),
                     label = cms.untracked.string("AK4PFPuppi"))
            )
                               )
    process.es_prefer_jec = cms.ESPrefer("PoolDBESSource","jec")

process.source.inputCommands = cms.untracked.vstring("keep *")

# Pre-skim weight counter
process.weightCounter = cms.EDAnalyzer('WeightCounter')

# Skim filter
muonLabel = "slimmedMuons"
elecLabel = "phase2Electrons"
photLabel = "phase2Photons"
if (options.inputFormat.lower() == "reco"):
    process.phoForYield = cms.EDProducer("CandViewMerger",
        src = cms.VInputTag(
            cms.InputTag("gedPhotons"),
            cms.InputTag("photonsFromMultiCl")
            )
        )
    photLabel = "phoForYield"
    process.eleForYield = cms.EDProducer("CandViewMerger",
        src = cms.VInputTag(
            cms.InputTag("gedGsfElectrons"),
            cms.InputTag("cleanedEcalDrivenGsfElectronsFromMultiCl")
            )
        )
    elecLabel = "eleForYield"
if options.updateJEC:
    jetLabel = "updatedPatJetsUpdatedJECAK4PFPuppi"
else:    
    jetLabel = "slimmedJets"
if (options.inputFormat.lower() == "reco"):
    muonLabel = "muons"
    if options.updateJEC:
        jetLabel = "ak4PUPPIJetsL1FastL2L3"
    else:    
        jetLabel = "ak4PUPPIJets"
process.selectedMuons = cms.EDFilter("CandPtrSelector",
                                     src = cms.InputTag(muonLabel),
                                     cut = cms.string("pt>10 && abs(eta)<3")
                                     )
process.selectedElectrons = cms.EDFilter("CandPtrSelector",
                                         src = cms.InputTag(elecLabel),
                                         cut = cms.string("pt>10 && abs(eta)<3")
                                         )
process.selectedPhotons = cms.EDFilter("CandPtrSelector",
                                         src = cms.InputTag(photLabel),
                                         cut = cms.string("pt>10 && abs(eta)<3")
                                         )
process.selectedJets = cms.EDFilter("CandPtrSelector",
                                    src = cms.InputTag(jetLabel),
                                    cut = cms.string("pt>20 && abs(eta)<5")
                                    )
process.allLeps = cms.EDProducer("CandViewMerger",
                                 src = cms.VInputTag(
                                                     cms.InputTag("selectedElectrons"),
                                                     cms.InputTag("selectedMuons")
                                                     )
                                 )
process.countLeps = cms.EDFilter("CandViewCountFilter",
                                 src = cms.InputTag("allLeps"),
                                 minNumber = cms.uint32(1)
                                 )
process.countPhotons = cms.EDFilter("CandViewCountFilter",
                                 src = cms.InputTag("selectedPhotons"),
                                 minNumber = cms.uint32(0)
                                 )
process.countJets = cms.EDFilter("CandViewCountFilter",
                                 src = cms.InputTag("selectedJets"),
                                 minNumber = cms.uint32(2)
                                 )
process.preYieldFilter = cms.Sequence(process.selectedMuons+process.selectedElectrons+process.allLeps+process.countLeps+process.selectedPhotons+process.countPhotons+process.selectedJets+process.countJets)


# run Puppi 
process.load('CommonTools/PileupAlgos/Puppi_cff')
process.load('CommonTools/PileupAlgos/PhotonPuppi_cff')
process.load('CommonTools/PileupAlgos/softKiller_cfi')
from CommonTools.PileupAlgos.PhotonPuppi_cff        import setupPuppiPhoton
from PhysicsTools.PatAlgos.slimming.puppiForMET_cff import makePuppies
makePuppies(process)
process.particleFlowNoLep = cms.EDFilter("PdgIdCandViewSelector",
                                    src = cms.InputTag("particleFlow"), 
                                    pdgId = cms.vint32( 1,2,22,111,130,310,2112,211,-211,321,-321,999211,2212,-2212 )
                                    )
process.puppiNoLep = process.puppi.clone(candName = cms.InputTag('particleFlowNoLep'))
process.load("PhysicsTools.PatAlgos.slimming.primaryVertexAssociation_cfi")
process.load("PhysicsTools.PatAlgos.slimming.offlineSlimmedPrimaryVertices_cfi")
process.load("PhysicsTools.PatAlgos.slimming.packedPFCandidates_cfi")

# recluster jets
process.load('RecoJets/Configuration/RecoPFJets_cff')
process.ak4PUPPIJets  = process.ak4PFJets.clone(rParam=0.4, src = cms.InputTag('puppi'))

# recompute MET
process.load('RecoMET.METProducers.PFMET_cfi')
process.puppiMet = process.pfMet.clone()
process.puppiMet.src = cms.InputTag('puppi')

# analysis
moduleName = "MiniFromPat"    
if (options.inputFormat.lower() == "reco"):
    moduleName = "MiniFromReco"
process.ntuple = cms.EDAnalyzer(moduleName)
process.load("PhaseTwoAnalysis.NTupler."+moduleName+"_cfi")
if (options.inputFormat.lower() == "reco"):
    process.ntuple.pfCandsNoLep = "puppiNoLep"
    process.ntuple.met = "puppiMet"
    if options.updateJEC:
        # This will load several ESProducers and EDProducers which make the corrected jet collections
        # In this case the collection will be called ak4PUPPIJetsL1FastL2L3
        process.load('PhaseTwoAnalysis.Jets.JetCorrection_cff')
        process.ntuple.jets = "ak4PUPPIJetsL1FastL2L3"
    else:
        # This simply switches the default AK4PFJetsCHS collection to the ak4PUPPIJets collection now that it has been produced
        process.ntuple.jets = "ak4PUPPIJets"
else:
    if options.updateJEC:
        # The updateJetCollection function will uncorred the jets from MiniAOD and then recorrect them using the current
        #  set of JEC in the event setup
        # The new name of the updated jet collection becomes updatedPatJetsUpdatedJECAK4PFPuppi
        from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection
        updateJetCollection(process,
                            jetSource = cms.InputTag('slimmedJetsPuppi'),
                            postfix = 'UpdatedJECAK4PFPuppi',
                            jetCorrections = ('AK4PFPuppi', ['L1FastJet','L2Relative','L3Absolute'], 'None')
                            )
        process.ntuple.jets = "updatedPatJetsUpdatedJECAK4PFPuppi"

# output
process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string(options.outFileName)
                                   )

# run
if (options.inputFormat.lower() == "reco"):
    process.puSequence = cms.Sequence(process.primaryVertexAssociation * process.pfNoLepPUPPI * process.puppi * process.particleFlowNoLep * process.puppiNoLep * process.offlineSlimmedPrimaryVertices * process.packedPFCandidates * process.muonIsolationPUPPI * process.muonIsolationPUPPINoLep * process.ak4PUPPIJets * process.puppiMet)

if options.skim:
    if (options.inputFormat.lower() == "reco"):
        if options.updateJEC:
            process.p = cms.Path(process.weightCounter * process.phase2Egamma * process.puSequence * process.ak4PFPuppiL1FastL2L3CorrectorChain * process.ak4PUPPIJetsL1FastL2L3 * process.preYieldFilter * process.ntuple)
        else:
            process.p = cms.Path(process.weightCounter * process.phase2Egamma * process.puSequence * process.preYieldFilter * process.ntuple)
    else:
        if options.updateJEC:
            process.p = cms.Path(process.weightCounter*process.phase2Egamma*process.patJetCorrFactorsUpdatedJECAK4PFPuppi * process.updatedPatJetsUpdatedJECAK4PFPuppi *process.preYieldFilter* process.ntuple)
        else:
            process.p = cms.Path(process.weightCounter*process.phase2Egamma*process.preYieldFilter*process.ntuple)
else:
    if (options.inputFormat.lower() == "reco"):
        if options.updateJEC:
            process.p = cms.Path(process.weightCounter * process.puSequence * process.ak4PFPuppiL1FastL2L3CorrectorChain * process.ak4PUPPIJetsL1FastL2L3 * process.phase2Egamma * process.ntuple)
        else:
            process.p = cms.Path(process.weightCounter * process.puSequence * process.phase2Egamma * process.ntuple)
    else:
        if options.updateJEC:
            process.p = cms.Path(process.weightCounter*process.patJetCorrFactorsUpdatedJECAK4PFPuppi * process.updatedPatJetsUpdatedJECAK4PFPuppi * process.phase2Egamma * process.ntuple)
	else:    
            process.p = cms.Path(process.weightCounter*process.phase2Egamma*process.ntuple)
