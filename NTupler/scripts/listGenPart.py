import FWCore.ParameterSet.Config as cms
process = cms.Process("DumpGP")

from Configuration.AlCa.autoCond import autoCond
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = '93X_upgrade2023_realistic_v2'
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/GluGluHToGG_M-125_13TeV_powheg_pythia8/MINIAODSIM/25nsFlat10to25TSG_76X_mcRun2_asymptotic_v12-v1/00000/0C6C1B51-9198-E511-B305-002590747D94.root'
    ),
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(20)
)

process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.printTree = cms.EDAnalyzer("ParticleListDrawer",
  maxEventsToPrint = cms.untracked.int32(100),
  printVertex = cms.untracked.bool(False),
  printOnlyHardInteraction = cms.untracked.bool(False), # Print only status=3 particles. This will not work for Pythia8, which does not have any such particles.
#  src = cms.InputTag("genParticles")
  src = cms.InputTag("prunedGenParticles")
)

process.p = cms.Path(
    process.printTree
)
