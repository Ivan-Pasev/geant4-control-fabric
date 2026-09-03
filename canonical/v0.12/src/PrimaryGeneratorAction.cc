#include "PrimaryGeneratorAction.hh"
#include "AnalysisRecord.hh"
#include "G4Event.hh"
#include "G4GeneralParticleSource.hh"

PrimaryGeneratorAction::PrimaryGeneratorAction()
  : fGPS(std::make_unique<G4GeneralParticleSource>()) {}
PrimaryGeneratorAction::~PrimaryGeneratorAction() = default;
void PrimaryGeneratorAction::GeneratePrimaries(G4Event* event) {
  fGPS->GeneratePrimaryVertex(event);
  if (event) g4cf::FillPrimaryRecords(*event);
}
