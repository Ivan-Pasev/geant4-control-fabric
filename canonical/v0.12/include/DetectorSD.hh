#pragma once
#include "G4VSensitiveDetector.hh"
class G4Step;
class G4TouchableHistory;
class DetectorSD final : public G4VSensitiveDetector {
public:
  explicit DetectorSD(const G4String& name);
  ~DetectorSD() override = default;
  G4bool ProcessHits(G4Step*, G4TouchableHistory*) override;
};
