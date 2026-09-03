#include "ProvenanceLedger.hh"
#include "Env.hh"
#include "G4Version.hh"

#include <array>
#include <fstream>

void g4cf::WriteRuntimeProvenance() {
  const auto base = g4cf::env("G4CF_PROVENANCE_BASENAME", "g4cf-runtime");
  std::ofstream out(base + ".txt", std::ios::out | std::ios::trunc);
  out << "g4cf_version=" << G4CF_VERSION << "\n";
  out << "geant4_version=" << G4Version << "\n";
  out << "geant4_version_number=" << G4VERSION_NUMBER << "\n";
  out << "run_id=" << g4cf::env("G4CF_RUN_ID", "UNSET") << "\n";
  out << "manifest_sha256=" << g4cf::env("G4CF_MANIFEST_SHA256", "UNSET") << "\n";
  out << "geometry_descriptor_sha256=" << g4cf::env("G4CF_GEOMETRY_SHA256", "UNSET") << "\n";
  out << "physics_list=" << g4cf::env("G4CF_PHYSICS_LIST", "Shielding") << "\n";
  out << "run_manager=" << g4cf::env("G4CF_RUN_MANAGER", "UNSET") << "\n";
  out << "threads=" << g4cf::env("G4CF_THREADS", "UNSET") << "\n";
  out << "event_modulo=0\n";
  out << "seed_once=0\n";
  out << "master_seed=" << g4cf::env("G4CF_MASTER_SEED", "11411") << "\n";
  out << "target_enabled=" << g4cf::env("G4CF_TARGET_ENABLED", "0") << "\n";
  out << "target_material=" << g4cf::env("G4CF_TARGET_MATERIAL", "G4_POLYETHYLENE") << "\n";
  out << "target_thickness_mm=" << g4cf::env("G4CF_TARGET_THICKNESS_MM", "50") << "\n";
  out << "detector_baseline_mm=" << g4cf::env("G4CF_DETECTOR_BASELINE_MM", "1000") << "\n";

  const std::array<const char*, 15> dataVars = {
    "G4NEUTRONHPDATA", "G4LEDATA", "G4LEVELGAMMADATA", "G4RADIOACTIVEDATA",
    "G4PARTICLEXSDATA", "G4PIIDATA", "G4REALSURFACEDATA", "G4SAIDXSDATA",
    "G4ABLADATA", "G4INCLDATA", "G4ENSDFSTATEDATA", "G4CHANNELINGDATA",
    "G4PARTICLEHPDATA", "G4NUDEXLIBDATA", "G4URRPTDATA"
  };
  for (const auto* key : dataVars) out << key << "=" << g4cf::env(key, "UNSET") << "\n";
}
