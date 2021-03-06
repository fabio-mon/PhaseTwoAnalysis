/*
 * ntupler.cpp
 *
 *  Created on: 24 Aug 2016
 *      Author: jkiesele
 */

#include "interface/ntupler.h"
#include "interface/scaleFactors.h"
//dirty hack
#include "../../../NTupler/src/MiniEvent.cc"
#include "TDirectory.h"
//#include "/interface/basicAnalyzer.h"
#include "TH1F.h"

void ntupler::analyze(size_t childid /* this info can be used for printouts */)
{
  d_ana::dBranchHandler<Electron> elecs(tree(),"Electron");
  d_ana::dBranchHandler<HepMCEvent>  event(tree(),"Event");
  d_ana::dBranchHandler<GenParticle> genpart(tree(),"Particle");
  d_ana::dBranchHandler<Jet>         genjet(tree(),"GenJet");
  d_ana::dBranchHandler<Jet>         jet(tree(),"JetPUPPI");
  d_ana::dBranchHandler<Jet>         taujet(tree(),"Jet");
  d_ana::dBranchHandler<Muon>        muontight(tree(),"MuonTight");
  d_ana::dBranchHandler<Photon>      photonloose(tree(),"PhotonLoose");
  d_ana::dBranchHandler<Photon>      photontight(tree(),"PhotonTight");
  d_ana::dBranchHandler<MissingET>   met(tree(),"PuppiMissingET");
  d_ana::dBranchHandler<Rho>         rho(tree(),"Rho");
  d_ana::dBranchHandler<ScalarHT>    mht(tree(),"ScalarHT");
  size_t nevents=tree()->entries();
  if(isTestMode())
    nevents/=100;

  //create output
  TString chilidstr="";
  chilidstr+=childid;
  TFile * outfile= new TFile(getOutDir()+"/p2ntuple_"+(TString)getLegendName()+"_"+chilidstr+".root","RECREATE");
  TDirectory *counterdir = outfile->mkdir("weightCounter");
  counterdir->cd();
  TH1F * h_event_weight = new TH1F("Event_weight","Event_weight",1,0,1);

  outfile->cd();
  TDirectory *ntupledir = outfile->mkdir("ntuple");
  ntupledir->cd();

  MiniEvent_t ev_;
  TTree * t_event_        = new TTree("Event","Event");
  TTree * t_genParts_     = new TTree("Particle","Particle");
  TTree * t_genPhotons_   = new TTree("GenPhoton","GenPhoton");
  TTree * t_vertices_     = new TTree("Vertex","Vertex");
  TTree * t_genJets_      = new TTree("GenJet","GenJet");
  TTree * t_looseElecs_   = new TTree("ElectronLoose","ElectronLoose");
  TTree * t_mediumElecs_  = new TTree("ElectronMedium","ElectronMedium");
  TTree * t_tightElecs_   = new TTree("ElectronTight","ElectronTight");
  TTree * t_looseMuons_   = new TTree("MuonLoose","MuonLoose");
  TTree * t_tightMuons_   = new TTree("MuonTight","MuonTight");
  TTree * t_allTaus_   = new TTree("TauAll","TauAll");
  TTree * t_puppiJets_    = new TTree("JetPUPPI","JetPUPPI");
  TTree * t_puppiMET_     = new TTree("PuppiMissingET","PuppiMissingET");
  TTree * t_loosePhotons_ = new TTree("PhotonLoose","PhotonLoose");
  TTree * t_tightPhotons_ = new TTree("PhotonTight","PhotonTight");
  TTree * t_scalarHT_     = new TTree("ScalarHT","ScalarHT");
  createMiniEventTree(t_event_, t_genParts_, t_vertices_, t_genJets_, t_genPhotons_, t_looseElecs_,
			t_mediumElecs_,t_tightElecs_, t_looseMuons_, t_tightMuons_, t_allTaus_, t_puppiJets_, t_puppiMET_, t_loosePhotons_,
		      t_tightPhotons_, ev_);

  Int_t nmht;
  Float_t ht[MiniEvent_t::maxpart];
  t_scalarHT_->Branch("MHT_size",       &nmht,    "MHT_size/I");
  t_scalarHT_->Branch("MHT",            ht,      "MHT[ScalarHT_size]/F");

  
  //load effective corrections for delphes samples vs fullSim
  scaleFactors
    tightelecsf,medelecsf,looseelecsf,
    tightmuonsf,loosemuonsf,
    jetsf,
    tightphotonsf,loosephotonsf,
    metsf;

  TString basepath=getenv("CMSSW_BASE");
  basepath+="/src/PhaseTwoAnalysis/delphesInterface/ntupler/data/";
  
  tightelecsf.loadTH2D  (basepath+"ElectronTight_PTabsEta.root","FullSimOverDelphes");
  medelecsf.loadTH2D    (basepath+"ElectronMedium_PTabsEta.root","FullSimOverDelphes");
  //looseelecsf.loadTH2D  (cmsswbase+"bla.root","histo");
  tightmuonsf.loadTH2D  (basepath+"MuonTight_PTabsEta.root","FullSimOverDelphes");
  //loosemuonsf.loadTH2D  (cmsswbase+"bla.root","histo");
  //jetsf.loadTH2D        (cmsswbase+"bla.root","histo");
  tightphotonsf.loadTH2D(basepath+"PhotonTight_PTabsEta.root","FullSimOverDelphes");
  //loosephotonsf.loadTH2D(cmsswbase+"bla.root","histo");
  //metsf.loadTH2D        (cmsswbase+"bla.root","histo");

  //get skim option
  bool doSkim=getSkimOpt();
  int nLepmin=getnLepmin();
  int nPhmin=getnPhmin();
  int nJetmin=getnJetmin();
  for(size_t eventno=0;eventno<nevents;eventno++)
  {
    /*
     * The following two lines report the status and set the event link
     * Do not remove!
     */
    reportStatus(eventno,nevents);
    tree()->setEntry(eventno);
    
    if(event.size()<1)continue;
    
    //std::cout<<"rho="<<rho.Rho<<"in range "

    //template object d_ana::dBranchHandler<HepMCEvent> is a vector --> event is a vector of 1 entry
    h_event_weight->Fill(0.,(double)event.at(0)->Weight);
    
    std::vector<GenParticle*>selectedgenpart;
    std::vector<GenParticle*>selectedgenphoton;
    //std::cout<<std::endl;
    for(size_t i=0;i<genpart.size();i++)
    {
      //std::cout<<"i="<<i<<"\tPID="<<genpart.at(i)->PID<<"\tStatus="<<genpart.at(i)->Status<<"\t1stmother="<<genpart.at(i)->M1<<"\tlastmother="<<genpart.at(i)->M2<<"\t1stdaug="<<genpart.at(i)->D1<<"\tlastdaug="<<genpart.at(i)->D2<<"\tPT="<<genpart.at(i)->PT<<std::endl;
      int pid= fabs(genpart.at(i)->PID);
      if(genpart.at(i)->PT<15 && pid!=25) continue;
      if(pid==22)
	selectedgenphoton.push_back(genpart.at(i));	
      if( (pid>18  && pid < 23) ||  pid > 25 ) continue;
      selectedgenpart.push_back(genpart.at(i));
    }

    std::vector<Jet*>selectedgenjet;
    for(size_t i=0;i<genjet.size();i++)
    {
      //if( genjet.at(i)->PT<20 ) continue;
      selectedgenjet.push_back(genjet.at(i));
    }

    
    
    std::vector<Photon*>selectedtightphotons;
    for(size_t i=0;i<photontight.size();i++)
    {
      if(photontight.at(i)->PT<20) continue;
      //std::cout<<"photontight (eta,phi)=("<<photontight.at(i)->Eta<<","<<photontight.at(i)->Phi<<")\tPt="<<photontight.at(i)->PT<<"\tIsolation/E="<< photontight.at(i)->IsolationVarRhoCorr/photontight.at(i)->E <<std::endl;
      
      //if(photon.at(i)->IsolationVarRhoCorr / photon.at(i)->E > 0.25) continue;
      selectedtightphotons.push_back(photontight.at(i));
    }
    
    std::vector<Photon*>selectedloosephotons;
    for(size_t i=0;i<photonloose.size();i++)
    {
      if(photonloose.at(i)->PT<20) continue;
      //std::cout<<"photonloose (eta,phi)=("<<photonloose.at(i)->Eta<<","<<photonloose.at(i)->Phi<<")\tPt="<<photonloose.at(i)->PT<<"\tIsolation/E="<< photonloose.at(i)->IsolationVarRhoCorr/photonloose.at(i)->E <<std::endl;
     
      //if(photon.at(i)->IsolationVarRhoCorr / photon.at(i)->E > 0.25) continue;
      selectedloosephotons.push_back(photonloose.at(i));
    }
    
    if(doSkim && selectedtightphotons.size()<nPhmin && selectedloosephotons.size()<nPhmin)  continue;
	
    std::vector<Electron*> selectedelectrons;
    for(size_t i=0;i<elecs.size();i++)
    {
      if(elecs.at(i)->PT<10) continue;
      selectedelectrons.push_back(elecs.at(i));
    }

    std::vector<Muon*> selectedMuons;
    for(size_t i=0;i<muontight.size();i++)
    {
      if(muontight.at(i)->PT<5) continue;
      selectedMuons.push_back(muontight.at(i));
    }

    if( doSkim && (selectedelectrons.size()+selectedMuons.size())<nLepmin )
      continue;

    std::vector<Jet*>selectedjets;
    for(size_t i=0;i<jet.size();i++)
    {
      if(jet.at(i)->PT<20)continue;
      selectedjets.push_back(jet.at(i));
    }

    if( doSkim && selectedjets.size()<nJetmin )
      continue;

    std::vector<Jet*>selectedtaujets;
    for(size_t i=0;i<taujet.size();i++)
    {
      if(taujet.at(i)->PT<10)continue;
      //std::cout<<taujet.at(i)->PT<<"\t("<<taujet.at(i)->Eta<<","<<taujet.at(i)->Phi<<")"<<std::endl;
      if(taujet.at(i)->TauTag!=1) continue;
      selectedtaujets.push_back(taujet.at(i));
    }
    //std::cout<<"--------------------------------------------"<<std::endl;

    ev_.event = event.at(0)->Number;

    ev_.g_nw = 1;
    ev_.g_w[0] = event.at(0)->Weight;

    ev_.ngl=0;
    for(size_t i=0;i<selectedgenpart.size();i++)
    {
      if(ev_.ngl>=MiniEvent_t::maxpart)break;
      ev_.gl_pid[ev_.ngl]=selectedgenpart.at(i)->PID;
      ev_.gl_ch[ev_.ngl]=selectedgenpart.at(i)->Charge;
      ev_.gl_st[ev_.ngl]=selectedgenpart.at(i)->Status;
      ev_.gl_p[ev_.ngl]=selectedgenpart.at(i)->P;
      ev_.gl_pz[ev_.ngl]=selectedgenpart.at(i)->Pz;
      ev_.gl_pt[ev_.ngl]=selectedgenpart.at(i)->PT;
      ev_.gl_eta[ev_.ngl]=selectedgenpart.at(i)->Eta;
      ev_.gl_phi[ev_.ngl]=selectedgenpart.at(i)->Phi;
      ev_.gl_mass[ev_.ngl]=selectedgenpart.at(i)->Mass;
      ev_.ngl++;
    }

    ev_.ngp=0;
    for(size_t i=0;i<selectedgenphoton.size();i++)
    {
      if(ev_.ngp>=MiniEvent_t::maxpart)break;
      ev_.gp_st[ev_.ngp]=selectedgenphoton.at(i)->Status;
      ev_.gp_p[ev_.ngp]=selectedgenphoton.at(i)->P;
      ev_.gp_pz[ev_.ngp]=selectedgenphoton.at(i)->Pz;
      ev_.gp_pt[ev_.ngp]=selectedgenphoton.at(i)->PT;
      ev_.gp_eta[ev_.ngp]=selectedgenphoton.at(i)->Eta;
      ev_.gp_phi[ev_.ngp]=selectedgenphoton.at(i)->Phi;
      ev_.gp_nrj[ev_.ngp]=selectedgenphoton.at(i)->E;
      ev_.ngp++;
    }

    ev_.ngj=0;
    for(size_t i=0;i<selectedgenjet.size();i++)
    {
      if(ev_.ngj>=MiniEvent_t::maxpart)break;
      ev_.gj_pt[ev_.ngj]=selectedgenjet.at(i)->PT;
      ev_.gj_eta[ev_.ngj]=selectedgenjet.at(i)->Eta;
      ev_.gj_phi[ev_.ngj]=selectedgenjet.at(i)->Phi;
      ev_.gj_mass[ev_.ngj]=selectedgenjet.at(i)->Mass;
      ev_.ngj++;
    }


    ev_.nlp=0;
    for(size_t i=0;i<selectedloosephotons.size();i++)
    {
      if(ev_.nlp>=MiniEvent_t::maxpart)break;
      //std::cout<<"photon (eta,phi)=("<<ev_.lp_eta[ev_.nlp]<<","<<ev_.lp_phi[ev_.nlp]<<")"<<std::endl;
      ev_.lp_eta[ev_.nlp]=selectedloosephotons.at(i)->Eta;
      ev_.lp_pt [ev_.nlp]=selectedloosephotons.at(i)->PT;
      ev_.lp_phi[ev_.nlp]=selectedloosephotons.at(i)->Phi;
      ev_.lp_nrj[ev_.nlp]=selectedloosephotons.at(i)->E;
      ev_.lp_iso_rhocorr[ev_.nlp]=selectedloosephotons.at(i)->IsolationVarRhoCorr;
      ev_.lp_sf[ev_.nlp]=loosephotonsf.getSF(fabs(selectedloosephotons.at(i)->Eta),selectedloosephotons.at(i)->PT);
      ev_.nlp++;
    }

    ev_.ntp=0;
    for(size_t i=0;i<selectedtightphotons.size();i++)
    {
      if(ev_.ntp>=MiniEvent_t::maxpart)break;
      //std::cout<<"photon (eta,phi)=("<<ev_.tp_eta[ev_.ntp]<<","<<ev_.tp_phi[ev_.ntp]<<")"<<std::endl;
      ev_.tp_eta[ev_.ntp]=selectedtightphotons.at(i)->Eta;
      ev_.tp_pt [ev_.ntp]=selectedtightphotons.at(i)->PT;
      ev_.tp_phi[ev_.ntp]=selectedtightphotons.at(i)->Phi;
      ev_.tp_nrj[ev_.ntp]=selectedtightphotons.at(i)->E;
      ev_.tp_iso_rhocorr[ev_.ntp]=selectedtightphotons.at(i)->IsolationVarRhoCorr;
      ev_.tp_sf[ev_.ntp]=tightphotonsf.getSF(fabs(selectedtightphotons.at(i)->Eta),selectedtightphotons.at(i)->PT);
      ev_.ntp++;
    }

    ev_.ntm=0;
    for(size_t i=0;i<selectedMuons.size();i++)
    {
      if(ev_.ntm>=MiniEvent_t::maxpart)break;
      ev_.tm_pt    [ev_.ntm]=selectedMuons.at(i)->PT;
      ev_.tm_eta   [ev_.ntm]=selectedMuons.at(i)->Eta;
      ev_.tm_phi   [ev_.ntm]=selectedMuons.at(i)->Phi;
      ev_.tm_mass  [ev_.ntm]=0.105;
      ev_.tm_relIso[ev_.ntm]=selectedMuons.at(i)->IsolationVarRhoCorr; // /selectedMuons.at(i)->PT;
      ev_.tm_sf    [ev_.ntm]=tightmuonsf.getSF(fabs(selectedMuons.at(i)->Eta),selectedMuons.at(i)->PT);
      //ev_.tm_g     [ev_.ntm] =selectedMuons.at(i)->Particle.PID;
      ev_.ntm++;
    }

    ev_.nte=0;
    ev_.nme=0;
    for(size_t i=0;i<selectedelectrons.size();i++)
    {
      if(ev_.nme>=MiniEvent_t::maxpart)break;
      ev_.me_pt    [ev_.nme] =selectedelectrons.at(i)->PT;
      ev_.me_eta   [ev_.nme]=selectedelectrons.at(i)->Eta;
      ev_.me_phi   [ev_.nme]=selectedelectrons.at(i)->Phi;
      ev_.me_mass  [ev_.nme]=0.00051;
      ev_.me_relIso[ev_.nme]=selectedelectrons.at(i)->IsolationVarRhoCorr; //  /selectedelectrons.at(i)->PT ;
      ev_.me_sf[ev_.nme]=medelecsf.getSF(fabs(selectedelectrons.at(i)->Eta),selectedelectrons.at(i)->PT);
      ev_.nme++;

      ev_.te_pt    [ev_.nte] =selectedelectrons.at(i)->PT;
      ev_.te_eta   [ev_.nte]=selectedelectrons.at(i)->Eta;
      ev_.te_phi   [ev_.nte]=selectedelectrons.at(i)->Phi;
      ev_.te_mass  [ev_.nte]=0.00051;
      ev_.te_relIso[ev_.nte]=selectedelectrons.at(i)->IsolationVarRhoCorr; //  /selectedelectrons.at(i)->PT ;
      ev_.te_sf[ev_.nte]=tightelecsf.getSF(fabs(selectedelectrons.at(i)->Eta),selectedelectrons.at(i)->PT);
      ev_.nte++;
    }

    ev_.ntau=0;
    for(size_t i=0;i<selectedtaujets.size();i++)
    {
      if(ev_.ntau>=MiniEvent_t::maxjets)break;
      ev_.tau_pt  [ev_.ntau] =selectedtaujets.at(i)->PT;
      ev_.tau_eta [ev_.ntau]=selectedtaujets.at(i)->Eta;
      ev_.tau_phi [ev_.ntau]=selectedtaujets.at(i)->Phi;
      ev_.tau_mass[ev_.ntau]=selectedtaujets.at(i)->Mass;
      ev_.tau_ch[ev_.ntau]=selectedtaujets.at(i)->Charge;
      ev_.tau_dm[ev_.ntau]=selectedtaujets.at(i)->Flavor; // not defined
      ev_.tau_chargedIso[ev_.ntau]=0; // not defined
      ev_.tau_sf[ev_.ntau]= 1; // jetsf.getSF(fabs(selectedtaujets.at(i)->Eta),selectedtaujets.at(i)->PT);
      ev_.ntau++;
    }

    ev_.nj=0;
    //std::cout<<"--------------------------------------------"<<std::endl;
    for(size_t i=0;i<selectedjets.size();i++)
    {
      if(ev_.nj>=MiniEvent_t::maxjets)break;
      ev_.j_pt  [ev_.nj] =selectedjets.at(i)->PT;
      ev_.j_eta [ev_.nj]=selectedjets.at(i)->Eta;
      ev_.j_phi [ev_.nj]=selectedjets.at(i)->Phi;
      ev_.j_mass[ev_.nj]=selectedjets.at(i)->Mass;
      
      ev_.j_hadflav[ev_.nj]=selectedjets.at(i)->Flavor;
      
      //std::cout<<"JETID="<<ev_.j_id[ev_.nj]<<"\tGENJET="<<ev_.j_g[ev_.nj]<<"\tPARTONFLAVOR="<<ev_.j_flav[ev_.nj]<<"\thadrFLAVOR="<<ev_.j_hadflav[ev_.nj]<<"\tGenPartonPID="<< ev_.j_pid[ev_.nj]<<std::endl;
      //std::cout<<"(eta,phi)=("<<ev_.j_eta[ev_.nj]<<","<<ev_.j_phi[ev_.nj]<<")\tPT="<<ev_.j_pt  [ev_.nj]<<std::endl;
      ev_.j_deepcsv[ev_.nj] = selectedjets.at(i)->BTag;
      ev_.j_mvav2[ev_.nj]   = selectedjets.at(i)->BTag;
      ev_.j_sf[ev_.nj]=jetsf.getSF(fabs(selectedjets.at(i)->Eta),selectedjets.at(i)->PT);
      ev_.nj++;
    }
    //std::cout<<"--------------------------------------------"<<std::endl;    
    //std::cout<<"--------------------------------------------"<<std::endl;
    ev_.nmet=0;
    for(size_t i=0;i<met.size();i++)
    {
      if(ev_.nmet>=MiniEvent_t::maxpart) break;
      ev_.met_eta[ev_.nmet]=met.at(i)->Eta ;
      ev_.met_pt [ev_.nmet]=met.at(i)->MET ;
      ev_.met_phi[ev_.nmet]=met.at(i)->Phi ;
      ev_.met_sf[ev_.nmet]=metsf.getSF(0,met.at(i)->MET);
      ev_.nmet++;
    }

    nmht=0;
    for(size_t i=0;i<mht.size();i++)
    {
      if(nmht>=MiniEvent_t::maxpart) break;
      ht[nmht]=mht.at(i)->HT ;
      nmht++;
    }


    //----------------------------------------------------------------------------------------------------------------------
    //std::cout<<"alabarda spaziale"<<std::endl;
    //std::cout<<"muon"<<ev_.ntm<<"\tele"<<ev_.nte<<"\ttightph"<<ev_.ntp<<"\tloosph"<<ev_.nlp<<"\tjet"<<ev_.nj<<std::endl;
    //----------------------------------------------------------------------------------------------------------------------
    //if( (doSkim && (ev_.ntm+ev_.nte)>=nLepmin && (ev_.ntp>=nPhmin || ev_.nlp>=nPhmin) && ev_.nj>=nJetmin) || (!doSkim) ) -->already done above
    {	 
      //----------------------------------------------------------------------------------------------------------------------      
      //std::cout<<"passato"<<std::endl;
      //----------------------------------------------------------------------------------------------------------------------
      t_event_->Fill();
      t_genParts_->Fill();
      t_genPhotons_->Fill();
      t_vertices_->Fill();
      //t_genJets_->Fill();
      t_looseElecs_->Fill();
      t_mediumElecs_->Fill();
      t_tightElecs_->Fill();
      t_looseMuons_->Fill();
      t_tightMuons_->Fill();
      t_allTaus_->Fill();
      t_puppiJets_->Fill();
      t_puppiMET_->Fill();
      t_scalarHT_->Fill();
      t_loosePhotons_->Fill();
      t_tightPhotons_->Fill();
    }
  }

  counterdir->cd();
  h_event_weight->Write();

  ntupledir->cd();
  t_event_        ->Write();
  t_genParts_     ->Write();
  t_genPhotons_   ->Write();
  t_vertices_     ->Write();
  //t_genJets_      ->Write();
  t_looseElecs_   ->Write();
  t_mediumElecs_  ->Write();
  t_tightElecs_   ->Write();
  t_looseMuons_   ->Write();
  t_tightMuons_   ->Write();
  t_allTaus_      ->Write();
  t_puppiJets_    ->Write();
  t_puppiMET_     ->Write();
  t_scalarHT_     ->Write();
  t_loosePhotons_ ->Write();
  t_tightPhotons_ ->Write();
  
  outfile->Close();
  /*
   * Must be called in the end, takes care of thread-safe writeout and
   * call-back to the parent process
   */
  processEndFunction();
}



void ntupler::postProcess(){

	/* empty */

}



