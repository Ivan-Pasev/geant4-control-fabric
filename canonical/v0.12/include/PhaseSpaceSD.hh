#pragma once
#include "G4VSensitiveDetector.hh"
class G4Step;
class G4TouchableHistory;
class PhaseSpaceSD final : public G4VSensitiveDetector {
public:
  explicit PhaseSpaceSD(const G4String& name);
  ~PhaseSpaceSD() override = default;
  G4bool ProcessHits(G4Step*, G4TouchableHistory*) override;
};
