#pragma once
#include "G4VUserDetectorConstruction.hh"
class G4LogicalVolume;
class G4VPhysicalVolume;

class DetectorConstruction final : public G4VUserDetectorConstruction {
public:
  DetectorConstruction() = default;
  ~DetectorConstruction() override = default;
  G4VPhysicalVolume* Construct() override;
  void ConstructSDandField() override;
private:
  G4LogicalVolume* fPhaseSpaceLV = nullptr;
  G4LogicalVolume* fDetectorLV = nullptr;
};
