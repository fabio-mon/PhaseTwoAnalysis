/* reimplemented from
 * ntupler.cpp
 *
 *  Created on: 24 Aug 2016
 *      Author: jkiesele
 */

#include "interface/photonvalidator.h"
#include "interface/scaleFactors.h"
//dirty hack
#include "TDirectory.h"
#include "TH1F.h"
#include "TLorentzVector.h"
#include "TCanvas.h"

void photonvalidator::analyze(size_t childid /* this info can be used for printouts */){

        d_ana::dBranchHandler<Electron> elecs(tree(),"Electron");
        d_ana::dBranchHandler<HepMCEvent>  event(tree(),"Event");
        d_ana::dBranchHandler<GenParticle> genpart(tree(),"Particle");
        d_ana::dBranchHandler<Jet>         genjet(tree(),"GenJet");
        d_ana::dBranchHandler<Jet>         jet(tree(),"JetPUPPI");
        d_ana::dBranchHandler<Jet>         taujet(tree(),"Jet");
        d_ana::dBranchHandler<Muon>        muontight(tree(),"MuonTight");
        d_ana::dBranchHandler<Photon>      photon(tree(),"Photon");
        d_ana::dBranchHandler<MissingET>   met(tree(),"MissingET");
        d_ana::dBranchHandler<MissingET>   puppimet(tree(),"PuppiMissingET");
        d_ana::dBranchHandler<MissingET>   genpumet(tree(),"GenPileUpMissingET");
        d_ana::dBranchHandler<MissingET>   genmet(tree(),"GenMissingET");


        size_t nevents=tree()->entries();
        if(isTestMode())
                nevents/=100;


        //create output
        TString chilidstr="";
        chilidstr+=childid;
        TFile * outfile= new TFile(getOutDir()+"/p2val_"+(TString)getLegendName()+"_"+chilidstr+".root","RECREATE");
        TDirectory *counterdir = outfile->mkdir("weightCounter");
        counterdir->cd();
        TH1F * h_event_weight = new TH1F("Event_weight","Event_weight",1,0,1);

        outfile->cd();
        TDirectory *photondir = outfile->mkdir("photon");
	photondir->cd();
        TH1F * h_photon_all_pt = new TH1F("h_photon_all_pt","Photon PT",200,0,200);
        TH1F * h_photon_all_eta = new TH1F("h_photon_all_eta","Photon eta",200,-5,5);
        TH1F * h_photon_all_phi = new TH1F("h_photon_all_phi","Photon phi",200,-3.5,3.5);
        TH1F * h_photon_all_E = new TH1F("h_photon_all_E","Photon energy",200,0,200);
        TH1F * h_photon_all_tof = new TH1F("h_photon_all_tof","Photon tof",200,0,10);
        TH1F * h_photon_all_emE_o_hE = new TH1F("h_photon_all_emE_o_hE","Photon em/hadronic energy in ECAL",200,0,10);
        TH1F * h_photon_all_IsolationVar = new TH1F("h_photon_all_IsolationVar","Photon IsolationVar",100,0,20);
        TH1F * h_photon_all_IsolationVarRhoCorr = new TH1F("h_photon_all_IsolationVarRhoCorr","Photon IsolationVarRhoCorr",100,0,20);
        TH1F * h_photon_all_SumPtCharged = new TH1F("h_photon_all_SumPtCharged","Photon SumPtCharged",100,0,20);
        TH1F * h_photon_all_SumPtNeutral = new TH1F("h_photon_all_SumPtNeutral","Photon SumPtNeutral",100,0,20);
        TH1F * h_photon_all_SumPtChargedPU = new TH1F("h_photon_all_SumPtChargedPU","Photon SumPtChargedPU",100,0,20);
        TH1F * h_photon_all_SumPt = new TH1F("h_photon_all_SumPt","Photon SumPt",100,0,20);

/*        TH1F * h_muontight_iso_pt = new TH1F("h_muontight_iso_pt","Muon PT",200,0,200);
        TH1F * h_muontight_iso_eta = new TH1F("h_muontight_iso_eta","Muon eta",200,-5,5);
        TH1F * h_muontight_iso_phi = new TH1F("h_muontight_iso_phi","Muon phi",200,-3.5,3.5);

        TH2F * h_muontight_all_IsolationVarRhoCorr_pt = new TH2F ("h_muontight_all_IsolationVarRhoCorr_pt","",200,0,20,200,0,20);
*/
        outfile->cd();
        TDirectory *zmmdir = outfile->mkdir("zmm");
        zmmdir->cd();
        TH1F * h_zmm_m1_pt = new TH1F("h_zmm_m1_pt","Muon PT 1",200,0,200);
        TH1F * h_zmm_m2_pt = new TH1F("h_zmm_m2_pt","Muon PT 2",200,0,200);
        TH1F * h_zmm_mass  = new TH1F("h_zmm_mass","ZMM mass",200,60,120);
        TH1F * h_zmm_met_pt = new TH1F("h_zmm_met_pt","MET ZMM sel",200,0,200);
        TH1F * h_zmm_puppimet_pt = new TH1F("h_zmm_puppimet_pt","MET no sel",200,0,200);
        TH1F * h_zmm_genpumet_pt = new TH1F("h_zmm_genpumet_pt","MET no sel",200,0,200);
        TH1F * h_zmm_genmet_pt = new TH1F("h_zmm_genmet_pt","MET no sel",200,0,200);

        TDirectory *metdir = outfile->mkdir("met");
        metdir->cd();
        TH1F * h_met_pt = new TH1F("h_met_pt","MET no sel",200,0,200);
        TH1F * h_puppimet_pt = new TH1F("h_puppimet_pt","MET no sel",200,0,200);
        TH1F * h_genpumet_pt = new TH1F("h_genpumet_pt","MET no sel",200,0,200);
        TH1F * h_genmet_pt = new TH1F("h_genmet_pt","MET no sel",200,0,200);

        //load effective corrections for delphes samples vs fullSim
        scaleFactors
                tightelecsf,medelecsf,looseelecsf,
                tightmuonsf,loosemuonsf,
                jetsf,
                tightphotonsf,loosephotonsf,
                metsf;

        TString basepath=getenv("CMSSW_BASE");
        basepath+="/src/PhaseTwoAnalysis/delphesInterface/ntupler/data/";

        tightelecsf.loadTH2D  (basepath+"ElectronTight_PTEta.root","FullSimOverDelphes");
        medelecsf.loadTH2D    (basepath+"ElectronMedium_PTEta.root","FullSimOverDelphes");
        //looseelecsf.loadTH2D  (cmsswbase+"bla.root","histo");
        //
        tightmuonsf.loadTH2D  (basepath+"MuonTight_PTEta.root","FullSimOverDelphes");
        //loosemuonsf.loadTH2D  (cmsswbase+"bla.root","histo");
        //
        //jetsf.loadTH2D        (cmsswbase+"bla.root","histo");
        //
        tightphotonsf.loadTH2D(basepath+"PhotonTight_PTEta.root","FullSimOverDelphes");
        //loosephotonsf.loadTH2D(cmsswbase+"bla.root","histo");
        //
        //metsf.loadTH2D        (cmsswbase+"bla.root","histo");

        for(size_t eventno=0;eventno<nevents;eventno++){
                /*
                 * The following two lines report the status and set the event link
                 * Do not remove!
                 */
                reportStatus(eventno,nevents);
                tree()->setEntry(eventno);

                if(event.size()<1)continue;

                h_event_weight->Fill(0.,(double)event.at(0)->Weight);

                // No selection
                h_met_pt->Fill(met.at(0)->MET);
                h_puppimet_pt->Fill(puppimet.at(0)->MET);
                h_genpumet_pt->Fill(genpumet.at(0)->MET);
                h_genmet_pt->Fill(genmet.at(0)->MET);

                // Playing at genlevel



                // Lets look for muons  
                Double_t maxpt1=0, maxpt2=0;
                size_t index1=0, index2=0;
                size_t ngoodmuons=0;

                for(size_t i=0;i<photon.size();i++){
                        h_photon_all_pt->Fill(photon.at(i)->PT);
                        h_photon_all_eta->Fill(photon.at(i)->Eta);
                        h_photon_all_phi->Fill(photon.at(i)->Phi);
                        h_photon_all_E->Fill(photon.at(i)->E);
                        h_photon_all_tof->Fill(photon.at(i)->T);
                        h_photon_all_emE_o_hE->Fill(photon.at(i)->EhadOverEem);
                        h_photon_all_IsolationVar->Fill(photon.at(i)->IsolationVar);
                        h_photon_all_IsolationVarRhoCorr->Fill(photon.at(i)->IsolationVarRhoCorr);
                        h_photon_all_SumPtCharged->Fill(photon.at(i)->SumPtCharged);
                        h_photon_all_SumPtNeutral->Fill(photon.at(i)->SumPtNeutral);
                        h_photon_all_SumPtChargedPU->Fill(photon.at(i)->SumPtChargedPU);
                        h_photon_all_SumPt->Fill(photon.at(i)->SumPt);
/*                  
                        h_photon_all_IsolationVarRhoCorr_pt ->Fill(photon.at(i)->IsolationVar,photon.at(i)->PT);

                        if(photon.at(i)->IsolationVarRhoCorr<0.1) { // this is just a guess  
                                h_photon_iso_pt->Fill(photon.at(i)->PT);
                                h_photon_iso_eta->Fill(photon.at(i)->Eta);
                                h_photon_iso_phi->Fill(photon.at(i)->Phi);                

                                if(muontight.at(i)->PT>maxpt1) { maxpt2=maxpt1; index2=index1; maxpt1=muontight.at(i)->PT; index1=i;}
                                else if (muontight.at(i)->PT>maxpt2) {maxpt2=muontight.at(i)->PT; index2=i;} 
                                ngoodmuons++;
                        }
                }
                if(ngoodmuons>=2) {
                        if( muontight.at(index1)->PT>20 && muontight.at(index2)->PT > 20 && 
                                        (muontight.at(index1)->Charge!=muontight.at(index2)->Charge) ) { 
                        h_zmm_m1_pt->Fill(muontight.at(index1)->PT);
                        h_zmm_m2_pt->Fill(muontight.at(index2)->PT);

                        TLorentzVector m1, m2;
                        m1.SetPtEtaPhiM(muontight.at(index1)->PT,muontight.at(index1)->Eta,muontight.at(index1)->Phi,0.105); 
                        m2.SetPtEtaPhiM(muontight.at(index2)->PT,muontight.at(index2)->Eta,muontight.at(index2)->Phi,0.105);

                        h_zmm_mass->Fill( (m1+m2).M() );

                        h_zmm_met_pt->Fill(met.at(0)->MET);
                        h_zmm_puppimet_pt->Fill(puppimet.at(0)->MET);
                        h_zmm_genpumet_pt->Fill(genpumet.at(0)->MET);
                        h_zmm_genmet_pt->Fill(genmet.at(0)->MET);


//                        Double_t mass2=2*muontight.at(index1)->PT*muontight.at(index2)->PT*( cosh(muontight.at(index1)->Eta-muontight.at(index2)->Eta) - cos(muontight.at(index1)->Phi-muontight.at(index2)->Phi) );
//                        std::cout<<muontight.at(index1)->PT<<"   "<<m1.Pt()<<std::endl;
//                        std::cout<<sqrt(mass2)<<"   "<<(m1+m2).M()<<std::endl;

                  }*/
                }
        }   

TCanvas c1;
if(getPlotMode())
{
	h_photon_all_pt->Draw();	
	c1.Print(getPlotDir()+h_photon_all_pt->GetName()+".png","png");
	c1.Print(getPlotDir()+h_photon_all_pt->GetName()+".pdf","pdf");
	h_photon_all_eta    ->Draw();
	c1.Print(getPlotDir()+h_photon_all_eta->GetName()+".png","png");
	c1.Print(getPlotDir()+h_photon_all_eta->GetName()+".pdf","pdf");
	h_photon_all_phi    ->Draw();
	c1.Print(getPlotDir()+h_photon_all_phi->GetName()+".png","png");
	c1.Print(getPlotDir()+h_photon_all_phi->GetName()+".pdf","pdf");
	h_photon_all_E    ->Draw();
	c1.Print(getPlotDir()+h_photon_all_E->GetName()+".png","png");
	c1.Print(getPlotDir()+h_photon_all_E->GetName()+".pdf","pdf");
	h_photon_all_tof    ->Draw();
	c1.Print(getPlotDir()+h_photon_all_tof->GetName()+".png","png");
	c1.Print(getPlotDir()+h_photon_all_tof->GetName()+".pdf","pdf");
	h_photon_all_emE_o_hE    ->Draw();
	c1.Print(getPlotDir()+h_photon_all_emE_o_hE->GetName()+".png","png");
	c1.Print(getPlotDir()+h_photon_all_emE_o_hE->GetName()+".pdf","pdf");
	h_photon_all_IsolationVar        ->Draw();
	c1.Print(getPlotDir()+h_photon_all_IsolationVar->GetName()+".png","png");
	c1.Print(getPlotDir()+h_photon_all_IsolationVar->GetName()+".pdf","pdf");
	h_photon_all_IsolationVarRhoCorr ->Draw();
	c1.Print(getPlotDir()+h_photon_all_IsolationVarRhoCorr->GetName()+".png","png");
	c1.Print(getPlotDir()+h_photon_all_IsolationVarRhoCorr->GetName()+".pdf","pdf");
	h_photon_all_SumPtCharged        ->Draw();
	c1.Print(getPlotDir()+h_photon_all_SumPtCharged->GetName()+".png","png");
	c1.Print(getPlotDir()+h_photon_all_SumPtCharged->GetName()+".pdf","pdf");
	h_photon_all_SumPtNeutral        ->Draw();
	c1.Print(getPlotDir()+h_photon_all_SumPtNeutral->GetName()+".png","png");
	c1.Print(getPlotDir()+h_photon_all_SumPtNeutral->GetName()+".pdf","pdf");
	h_photon_all_SumPtChargedPU      ->Draw();
	c1.Print(getPlotDir()+h_photon_all_SumPtChargedPU->GetName()+".png","png");
	c1.Print(getPlotDir()+h_photon_all_SumPtChargedPU->GetName()+".pdf","pdf");
	h_photon_all_SumPt               ->Draw();
	c1.Print(getPlotDir()+h_photon_all_SumPt ->GetName()+".png","png");
	c1.Print(getPlotDir()+h_photon_all_SumPt ->GetName()+".pdf","pdf");
}



counterdir->cd();
h_event_weight->Write();

photondir->cd();
h_photon_all_pt->Write();
h_photon_all_eta    ->Write();
h_photon_all_phi    ->Write();
h_photon_all_E    ->Write();
h_photon_all_tof    ->Write();
h_photon_all_emE_o_hE    ->Write();
h_photon_all_IsolationVar        ->Write();
h_photon_all_IsolationVarRhoCorr ->Write();
h_photon_all_SumPtCharged        ->Write();
h_photon_all_SumPtNeutral        ->Write();
h_photon_all_SumPtChargedPU      ->Write();
h_photon_all_SumPt               ->Write();


/*
h_photon_all_IsolationVarRhoCorr_pt->Write();

h_photon_iso_pt->Write();
h_photon_iso_eta    ->Write();
h_photon_iso_phi    ->Write();
*/
zmmdir->cd();
h_zmm_m1_pt->Write();
h_zmm_m2_pt->Write();
h_zmm_mass->Write();
h_zmm_met_pt->Write();
h_zmm_puppimet_pt->Write();
h_zmm_genpumet_pt->Write();
h_zmm_genmet_pt->Write();

metdir->cd();
h_met_pt->Write();
h_puppimet_pt->Write();
h_genpumet_pt->Write();
h_genmet_pt->Write();

outfile->Close();
/*
 * Must be called in the end, takes care of thread-safe writeout and
 * call-back to the parent process
 */
processEndFunction();
}



void photonvalidator::postProcess(){

        /* empty */

}



