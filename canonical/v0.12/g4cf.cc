#include "ActionInitialization.hh"
#include "DetectorConstruction.hh"
#include "Env.hh"
#include "PhysicsListLoader.hh"

#include "G4RunManagerFactory.hh"
#include "G4UImanager.hh"
#include "G4Version.hh"
#include "Randomize.hh"
#include "CLHEP/Random/MixMaxRng.h"

#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>

static_assert(G4VERSION_NUMBER >= 1140 && G4VERSION_NUMBER < 1150,
              "GM-07 canonical runtime requires Geant4 11.4.x");

int main(int argc, char** argv) {
  try {
    if (argc != 2) {
      std::cerr << "Usage: g4cf <macro.mac>\n";
      return 2;
    }

    auto engine = std::make_unique<CLHEP::MixMaxRng>();
    G4Random::setTheEngine(engine.get());
    G4Random::setTheSeed(g4cf::env_long("G4CF_MASTER_SEED", 11411));

    const auto runManagerType = g4cf::env("G4CF_RUN_MANAGER", "MTOnly");
    const auto threads = g4cf::env_int("G4CF_THREADS", 1);
    auto* runManager = G4RunManagerFactory::CreateRunManager(runManagerType, true, threads);

    runManager->SetUserInitialization(new DetectorConstruction());
    runManager->SetUserInitialization(
      g4cf::LoadReferencePhysicsList(g4cf::env("G4CF_PHYSICS_LIST", "Shielding")));
    runManager->SetUserInitialization(new ActionInitialization());

    const G4String command = "/control/execute ";
    const G4String macro = argv[1];
    const auto status = G4UImanager::GetUIpointer()->ApplyCommand(command + macro);

    delete runManager;
    return status == 0 ? 0 : 3;
  } catch (const std::exception& e) {
    std::cerr << "g4cf fatal: " << e.what() << "\n";
    return 1;
  }
}
