#include "AnalysisRecord.hh"
#include "Env.hh"

#include "G4AnalysisManager.hh"
#include "G4Event.hh"
#include "G4PrimaryParticle.hh"
#include "G4PrimaryVertex.hh"
#include "G4RunManager.hh"
#include "G4Step.hh"
#include "G4SystemOfUnits.hh"
#include "G4Track.hh"
#include "G4VProcess.hh"

void g4cf::CreateEventNtuple() {
  auto* a = G4AnalysisManager::Instance();
  a->CreateNtuple("events", "G4 Control Fabric truth v2");
  a->CreateNtupleIColumn("record_kind");
  a->CreateNtupleSColumn("run_id");
  a->CreateNtupleIColumn("event_id");
  a->CreateNtupleIColumn("track_id");
  a->CreateNtupleIColumn("parent_id");
  a->CreateNtupleIColumn("step_id");
  a->CreateNtupleIColumn("particle_pdg");
  a->CreateNtupleSColumn("creator_process");
  a->CreateNtupleSColumn("step_process");
  a->CreateNtupleSColumn("volume_id");
  a->CreateNtupleSColumn("material_id");
  a->CreateNtupleDColumn("x_mm");
  a->CreateNtupleDColumn("y_mm");
  a->CreateNtupleDColumn("z_mm");
  a->CreateNtupleDColumn("px_MeV");
  a->CreateNtupleDColumn("py_MeV");
  a->CreateNtupleDColumn("pz_MeV");
  a->CreateNtupleDColumn("kinetic_pre_MeV");
  a->CreateNtupleDColumn("kinetic_post_MeV");
  a->CreateNtupleDColumn("energy_deposit_MeV");
  a->CreateNtupleDColumn("global_time_ns");
  a->CreateNtupleDColumn("source_weight");
  a->CreateNtupleDColumn("event_weight");
  a->CreateNtupleSColumn("genealogy_class");
  a->CreateNtupleSColumn("detector_channel");
  a->FinishNtuple();
}

void g4cf::FillPrimaryRecords(const G4Event& event) {
  auto* a = G4AnalysisManager::Instance();
  for (G4int iv = 0; iv < event.GetNumberOfPrimaryVertex(); ++iv) {
    const auto* vertex = event.GetPrimaryVertex(iv);
    if (!vertex) continue;
    for (G4int ip = 0; ip < vertex->GetNumberOfParticle(); ++ip) {
      const auto* particle = vertex->GetPrimary(ip);
      if (!particle) continue;
      const auto p = particle->GetMomentum();
      const auto w = vertex->GetWeight() * particle->GetWeight();
      a->FillNtupleIColumn(0, static_cast<int>(RecordKind::Primary));
      a->FillNtupleSColumn(1, g4cf::env("G4CF_RUN_ID", "UNSET"));
      a->FillNtupleIColumn(2, event.GetEventID());
      a->FillNtupleIColumn(3, -1);
      a->FillNtupleIColumn(4, -1);
      a->FillNtupleIColumn(5, -1);
      a->FillNtupleIColumn(6, particle->GetPDGcode());
      a->FillNtupleSColumn(7, "PRIMARY");
      a->FillNtupleSColumn(8, "SOURCE_GENERATION");
      a->FillNtupleSColumn(9, "SOURCE_VERTEX");
      a->FillNtupleSColumn(10, "UNDEFINED");
      a->FillNtupleDColumn(11, vertex->GetX0()/mm);
      a->FillNtupleDColumn(12, vertex->GetY0()/mm);
      a->FillNtupleDColumn(13, vertex->GetZ0()/mm);
      a->FillNtupleDColumn(14, p.x()/MeV);
      a->FillNtupleDColumn(15, p.y()/MeV);
      a->FillNtupleDColumn(16, p.z()/MeV);
      a->FillNtupleDColumn(17, particle->GetKineticEnergy()/MeV);
      a->FillNtupleDColumn(18, particle->GetKineticEnergy()/MeV);
      a->FillNtupleDColumn(19, 0.0);
      a->FillNtupleDColumn(20, vertex->GetT0()/ns);
      a->FillNtupleDColumn(21, w);
      a->FillNtupleDColumn(22, w);
      a->FillNtupleSColumn(23, "PRIMARY");
      a->FillNtupleSColumn(24, "SOURCE");
      a->AddNtupleRow();
    }
  }
}

void g4cf::FillStepRecord(RecordKind kind, const G4Step& step, const std::string& channel) {
  auto* a = G4AnalysisManager::Instance();
  const auto* track = step.GetTrack();
  const auto* pre = step.GetPreStepPoint();
  const auto* post = step.GetPostStepPoint();
  const auto* event = G4RunManager::GetRunManager()->GetCurrentEvent();
  const auto* creator = track->GetCreatorProcess();
  const auto* defined = post->GetProcessDefinedStep();
  const auto* volume = pre->GetPhysicalVolume();
  const auto* material = pre->GetMaterial();
  const auto p = pre->GetMomentum();

  a->FillNtupleIColumn(0, static_cast<int>(kind));
  a->FillNtupleSColumn(1, g4cf::env("G4CF_RUN_ID", "UNSET"));
  a->FillNtupleIColumn(2, event ? event->GetEventID() : -1);
  a->FillNtupleIColumn(3, track->GetTrackID());
  a->FillNtupleIColumn(4, track->GetParentID());
  a->FillNtupleIColumn(5, track->GetCurrentStepNumber());
  a->FillNtupleIColumn(6, track->GetParticleDefinition()->GetPDGEncoding());
  a->FillNtupleSColumn(7, creator ? creator->GetProcessName() : "PRIMARY");
  a->FillNtupleSColumn(8, defined ? defined->GetProcessName() : "NONE");
  a->FillNtupleSColumn(9, volume ? volume->GetName() : "NONE");
  a->FillNtupleSColumn(10, material ? material->GetName() : "NONE");
  a->FillNtupleDColumn(11, pre->GetPosition().x()/mm);
  a->FillNtupleDColumn(12, pre->GetPosition().y()/mm);
  a->FillNtupleDColumn(13, pre->GetPosition().z()/mm);
  a->FillNtupleDColumn(14, p.x()/MeV);
  a->FillNtupleDColumn(15, p.y()/MeV);
  a->FillNtupleDColumn(16, p.z()/MeV);
  a->FillNtupleDColumn(17, pre->GetKineticEnergy()/MeV);
  a->FillNtupleDColumn(18, post->GetKineticEnergy()/MeV);
  a->FillNtupleDColumn(19, step.GetTotalEnergyDeposit()/MeV);
  a->FillNtupleDColumn(20, pre->GetGlobalTime()/ns);
  a->FillNtupleDColumn(21, 1.0);
  a->FillNtupleDColumn(22, track->GetWeight());
  a->FillNtupleSColumn(23, creator ? creator->GetProcessName() : "PRIMARY");
  a->FillNtupleSColumn(24, channel);
  a->AddNtupleRow();
}
