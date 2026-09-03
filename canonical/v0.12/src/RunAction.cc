#include "RunAction.hh"
#include "AnalysisRecord.hh"
#include "Env.hh"
#include "ProvenanceLedger.hh"

#include "G4AnalysisManager.hh"
#include "G4Run.hh"

RunAction::RunAction() {
  auto* a = G4AnalysisManager::Instance();
  a->SetDefaultFileType("root");
  a->SetNtupleMerging(true);
  g4cf::CreateEventNtuple();
}

void RunAction::BeginOfRunAction(const G4Run*) {
  auto* a = G4AnalysisManager::Instance();
  const auto output = g4cf::env("G4CF_OUTPUT_BASENAME", "g4cf-events");
  a->OpenFile(output);
  if (IsMaster()) g4cf::WriteRuntimeProvenance();
}

void RunAction::EndOfRunAction(const G4Run*) {
  auto* a = G4AnalysisManager::Instance();
  a->Write();
  a->CloseFile();
}
