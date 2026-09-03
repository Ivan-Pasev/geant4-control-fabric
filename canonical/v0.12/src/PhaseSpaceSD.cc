#include "PhaseSpaceSD.hh"
#include "AnalysisRecord.hh"
#include "G4Step.hh"
#include "G4StepPoint.hh"

PhaseSpaceSD::PhaseSpaceSD(const G4String& name) : G4VSensitiveDetector(name) {}
G4bool PhaseSpaceSD::ProcessHits(G4Step* step, G4TouchableHistory*) {
  if (!step || step->GetPreStepPoint()->GetStepStatus() != fGeomBoundary) return false;
  g4cf::FillStepRecord(g4cf::RecordKind::PhaseSpace, *step, "PHASE_SPACE");
  return true;
}
