import FWCore.ParameterSet.Config as cms

#---------------------------------------------------------------------------------------------------
#                                           M A I N
#---------------------------------------------------------------------------------------------------
# create the process
process = cms.Process('FILEFI')

# say how many events to process (-1 means no limit)
process.maxEvents = cms.untracked.PSet(
  input = cms.untracked.int32(10)
)

#>> input source

process.source = cms.Source(
  "PoolSource",
  fileNames = cms.untracked.vstring('root://grid143.kfki.hu//store/mc/RunIISpring15DR74/TTbarDMJets_pseudoscalar_Mchi-1_Mphi-100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/AODSIM/Asympt25ns_MCRUN2_74_V9-v1/40000/04E00947-462F-E511-8F5A-0025905A6104.root')
)
process.source.inputCommands = cms.untracked.vstring(
  "keep *",
  "drop *_MEtoEDMConverter_*_*",
  "drop L1GlobalTriggerObjectMapRecord_hltL1GtObjectMap__HLT"
)

#>> configurations

# determine the global tag to use
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.GlobalTag.globaltag = 'MCRUN2_74_V9A'

# define meta data for this production
process.configurationMetadata = cms.untracked.PSet(
  name       = cms.untracked.string('BambuProd'),
  version    = cms.untracked.string('Mit_043'),
  annotation = cms.untracked.string('AODSIM')
)

#>> standard sequences

# load some standard sequences we will need
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.EventContent.EventContent_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('RecoVertex.PrimaryVertexProducer.OfflinePrimaryVertices_cfi')
process.load('TrackingTools.TransientTrack.TransientTrackBuilder_cfi')

# define sequence for ProductNotFound
process.options = cms.untracked.PSet(
  Rethrow = cms.untracked.vstring('ProductNotFound'),
  fileMode = cms.untracked.string('NOMERGE'),
  wantSummary = cms.untracked.bool(False)
)

# Import/Load the filler so all is already available for config changes
from MitProd.TreeFiller.MitTreeFiller_cfi import MitTreeFiller
process.load('MitProd.TreeFiller.MitTreeFiller_cfi')

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#
#                               R E C O  S E Q U E N C E
#
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

## Load stablePart producers
from MitEdm.Producers.conversionElectronsStable_cfi import electronsStable
process.load('MitEdm.Producers.conversionElectronsStable_cfi')

# Load Mit Mvf Conversion producer
# MultiVertexFitter is currently broken
#from MitProd.TreeFiller.conversionProducer_cff import conversionProducer, addConversionFiller
#process.load('MitProd.TreeFiller.conversionProducer_cff')
#addConversionFiller(MitTreeFiller)

# Electron likelihood-based id
from RecoEgamma.ElectronIdentification.ElectronMVAValueMapProducer_cfi import electronMVAValueMapProducer
process.load('RecoEgamma.ElectronIdentification.ElectronMVAValueMapProducer_cfi')
MitTreeFiller.Electrons.eIDLikelihoodName = 'electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15Trig50nsV1Values'

# Load basic particle flow collections
# Used for rho calculation
from CommonTools.ParticleFlow.goodOfflinePrimaryVertices_cfi import goodOfflinePrimaryVertices
from CommonTools.ParticleFlow.pfParticleSelection_cff import pfParticleSelectionSequence, pfPileUp, pfNoPileUp, pfPileUpIso, pfNoPileUpIso
from CommonTools.ParticleFlow.pfPhotons_cff import pfPhotonSequence
from CommonTools.ParticleFlow.pfElectrons_cff import pfElectronSequence
from CommonTools.ParticleFlow.pfMuons_cff import pfMuonSequence
from CommonTools.ParticleFlow.TopProjectors.pfNoMuon_cfi import pfNoMuon
from CommonTools.ParticleFlow.TopProjectors.pfNoElectron_cfi import pfNoElectron

process.load('CommonTools.ParticleFlow.goodOfflinePrimaryVertices_cfi')
process.load('CommonTools.ParticleFlow.pfParticleSelection_cff')
process.load('CommonTools.ParticleFlow.pfPhotons_cff')
process.load('CommonTools.ParticleFlow.pfElectrons_cff')
process.load('CommonTools.ParticleFlow.pfMuons_cff')
process.load('CommonTools.ParticleFlow.TopProjectors.pfNoMuon_cfi')
process.load('CommonTools.ParticleFlow.TopProjectors.pfNoElectron_cfi')

# Loading PFProducer to get the ptrs
from RecoParticleFlow.PFProducer.pfLinker_cff import particleFlowPtrs
process.load('RecoParticleFlow.PFProducer.pfLinker_cff')

# Load PUPPI
from MitProd.TreeFiller.PuppiSetup_cff import puppiSequence
process.load('MitProd.TreeFiller.PuppiSetup_cff')

# recluster fat jets, btag subjets
from MitProd.TreeFiller.utils.makeFatJets import initFatJets,makeFatJets
pfbrecoSequence = initFatJets(process, isData = False)
ak8chsSequence = makeFatJets(process, isData = False, algoLabel = 'AK', jetRadius = 0.8)
ak8puppiSequence = makeFatJets(process, isData = False, algoLabel = 'AK', jetRadius = 0.8, pfCandidates = 'puppiNoLepPlusLep')
ca15chsSequence = makeFatJets(process, isData = False, algoLabel = 'CA', jetRadius = 1.5)
ca15puppiSequence = makeFatJets(process, isData = False, algoLabel = 'CA', jetRadius = 1.5, pfCandidates = 'puppiNoLepPlusLep')

# unload unwanted PAT stuff
delattr(process, 'pfNoTauPFBRECOPFlow')
delattr(process, 'loadRecoTauTagMVAsFromPrepDBPFlow')

pfPileUp.PFCandidates = 'particleFlowPtrs'
pfNoPileUp.bottomCollection = 'particleFlowPtrs'
pfPileUpIso.PFCandidates = 'particleFlowPtrs'
pfNoPileUpIso.bottomCollection='particleFlowPtrs'

pfPileUp.Enable = True
pfPileUp.Vertices = 'goodOfflinePrimaryVertices'
pfPileUp.checkClosestZVertex = cms.bool(False)

# PUPPI jets
from RecoJets.JetProducers.ak4PFJetsPuppi_cfi import ak4PFJetsPuppi
process.load('RecoJets.JetProducers.ak4PFJetsPuppi_cfi')

ak4PFJetsPuppi.src = cms.InputTag('puppiNoLepPlusLep')
ak4PFJetsPuppi.doAreaFastjet = True

# Load FastJet L1 corrections
#from MitProd.TreeFiller.FastJetCorrection_cff import l1FastJetSequence
#process.load('MitProd.TreeFiller.FastJetCorrection_cff')

# Setup jet corrections
process.load('JetMETCorrections.Configuration.JetCorrectionServices_cff')

# Load btagging
from MitProd.TreeFiller.utils.setupBTag import setupBTag
ak4PFBTagSequence = setupBTag(process, 'ak4PFJets', 'AKt4PF')
ak4PFCHSBTagSequence = setupBTag(process, 'ak4PFJetsCHS', 'AKt4PFCHS')
ak4PFPuppiBTagSequence = setupBTag(process, 'ak4PFJetsPuppi', 'AKt4PFPuppi')

# Load HPS tau reconstruction (tau in AOD is older than the latest reco in release)
from RecoTauTag.Configuration.RecoPFTauTag_cff import PFTau
process.load('RecoTauTag.Configuration.RecoPFTauTag_cff')

#> Setup the met filters
from MitProd.TreeFiller.metFilters_cff import metFilters
process.load('MitProd.TreeFiller.metFilters_cff')

#> The bambu reco sequence
recoSequence = cms.Sequence(
  electronsStable *
  electronMVAValueMapProducer *
  #  conversionProducer *
  goodOfflinePrimaryVertices *
  particleFlowPtrs *
  pfParticleSelectionSequence *
  pfPhotonSequence *
  pfMuonSequence *
  pfNoMuon *
  pfElectronSequence *
  pfNoElectron *
  PFTau *
  puppiSequence *
  ak4PFJetsPuppi *
#  l1FastJetSequence *
  ak4PFBTagSequence *
  ak4PFCHSBTagSequence *
  ak4PFPuppiBTagSequence *
  pfbrecoSequence*
  ak8chsSequence*
  ak8puppiSequence*
  ca15chsSequence*
  ca15puppiSequence*
  metFilters
)

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#
#                               G E N  S E Q U E N C E
#
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

# Import/Load genjets
from RecoJets.Configuration.GenJetParticles_cff import genJetParticles
process.load('RecoJets.Configuration.GenJetParticles_cff')
from RecoJets.Configuration.RecoGenJets_cff import ak4GenJets, ak8GenJets
process.load('RecoJets.Configuration.RecoGenJets_cff')

genSequence = cms.Sequence(
  genJetParticles *
  ak4GenJets *
  ak8GenJets
)

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#
#                               B A M B U  S E Q U E N C E
#
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

# remember the bambu sequence has been imported and loaded already in the beginning

# configure the filler
MitTreeFiller.TreeWriter.fileName = 'bambu-output-file-tmp'
MitTreeFiller.PileupInfo.active = True
MitTreeFiller.MCParticles.active = True
MitTreeFiller.MCEventInfo.active = True
MitTreeFiller.MCVertexes.active = True
MitTreeFiller.EvtSelData.HBHENoiseFilterName = 'HBHENoiseFilterResultProducer:HBHENoiseFilterResultRun1'

# define fill bambu filler sequence

bambuFillerSequence = cms.Sequence(
  MitTreeFiller
)

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#
#                               C M S S W  P A T H
#
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

process.path = cms.Path(
  recoSequence *
  genSequence *
  bambuFillerSequence
)
