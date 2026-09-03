#include "PhysicsListLoader.hh"
#include "G4PhysListFactory.hh"
#include "G4VModularPhysicsList.hh"
#include <stdexcept>

G4VModularPhysicsList* g4cf::LoadReferencePhysicsList(const std::string& name) {
  G4PhysListFactory factory;
  auto* physics = factory.GetReferencePhysList(name);
  if (!physics) throw std::runtime_error("Unknown/unavailable Geant4 reference physics list: " + name);
  physics->SetVerboseLevel(1);
  return physics;
}
