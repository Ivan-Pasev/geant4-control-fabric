#include "DetectorSD.hh"
#include "AnalysisRecord.hh"
#include "G4Step.hh"

DetectorSD::DetectorSD(const G4String& name) : G4VSensitiveDetector(name) {}
G4bool DetectorSD::ProcessHits(G4Step* step, G4TouchableHistory*) {
  if (!step || step->GetTotalEnergyDeposit() <= 0.0) return false;
  g4cf::FillStepRecord(g4cf::RecordKind::DetectorStep, *step, "GE_DETECTOR");
  return true;
}
