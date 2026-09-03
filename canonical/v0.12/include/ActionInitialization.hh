#pragma once
#include "G4VUserActionInitialization.hh"
class ActionInitialization final : public G4VUserActionInitialization {
public:
  ActionInitialization() = default;
  ~ActionInitialization() override = default;
  void BuildForMaster() const override;
  void Build() const override;
};
