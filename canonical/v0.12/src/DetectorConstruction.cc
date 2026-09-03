#include "DetectorConstruction.hh"
#include "DetectorSD.hh"
#include "Env.hh"
#include "PhaseSpaceSD.hh"

#include "G4Box.hh"
#include "G4LogicalVolume.hh"
#include "G4Material.hh"
#include "G4NistManager.hh"
#include "G4PVPlacement.hh"
#include "G4SDManager.hh"
#include "G4SystemOfUnits.hh"

#include <fstream>
#include <iomanip>
#include <stdexcept>
#include <string>

namespace {
std::string json_escape(const std::string& s) {
  std::string out;
  out.reserve(s.size());
  for (const char c : s) {
    switch (c) {
      case '\\': out += "\\\\"; break;
      case '"': out += "\\\""; break;
      case '\n': out += "\\n"; break;
      case '\r': out += "\\r"; break;
      case '\t': out += "\\t"; break;
      default: out += c; break;
    }
  }
  return out;
}

void write_constructed_geometry_report(
    const G4Box& worldSolid, const G4LogicalVolume& worldLV,
    const G4Box& targetSolid, const G4LogicalVolume& targetLV,
    const G4Box& planeSolid, const G4LogicalVolume& planeLV, double planeZ,
    const G4Box& detSolid, const G4LogicalVolume& detLV, double detectorCenterZ,
    bool targetEnabled) {
  const auto path = g4cf::env("G4CF_CONSTRUCTED_GEOMETRY_REPORT", "");
  if (path.empty()) return;
  std::ofstream out(path, std::ios::out | std::ios::trunc);
  if (!out) throw std::runtime_error("Unable to write constructed geometry report: " + path);
  out << std::setprecision(17);
  out << "{\n";
  out << "  \"schema\": \"g4cf-constructed-geometry-runtime-v1\",\n";
  out << "  \"run_id\": \"" << json_escape(g4cf::env("G4CF_RUN_ID", "UNSET")) << "\",\n";
  out << "  \"constructed_from_runtime\": true,\n";
  out << "  \"review_required\": true,\n";
  out << "  \"automatic_geometry_acceptance\": false,\n";
  out << "  \"world\": {\"material\": \"" << json_escape(worldLV.GetMaterial()->GetName())
      << "\", \"half_size_mm\": [" << worldSolid.GetXHalfLength()/mm << ", "
      << worldSolid.GetYHalfLength()/mm << ", " << worldSolid.GetZHalfLength()/mm << "]},\n";
  out << "  \"target\": {\"enabled\": " << (targetEnabled ? "true" : "false")
      << ", \"material\": \"" << json_escape(targetLV.GetMaterial()->GetName())
      << "\", \"center_mm\": [0, 0, 0], \"half_xy_mm\": ["
      << targetSolid.GetXHalfLength()/mm << ", " << targetSolid.GetYHalfLength()/mm
      << "], \"thickness_mm\": " << 2.0*targetSolid.GetZHalfLength()/mm << "},\n";
  out << "  \"phase_space\": {\"material\": \"" << json_escape(planeLV.GetMaterial()->GetName())
      << "\", \"center_z_mm\": " << planeZ/mm << ", \"half_xy_mm\": ["
      << planeSolid.GetXHalfLength()/mm << ", " << planeSolid.GetYHalfLength()/mm
      << "], \"thickness_mm\": " << 2.0*planeSolid.GetZHalfLength()/mm << "},\n";
  out << "  \"detector\": {\"material\": \"" << json_escape(detLV.GetMaterial()->GetName())
      << "\", \"center_z_mm\": " << detectorCenterZ/mm << ", \"front_face_z_mm\": "
      << (detectorCenterZ-detSolid.GetZHalfLength())/mm << ", \"half_xy_mm\": ["
      << detSolid.GetXHalfLength()/mm << ", " << detSolid.GetYHalfLength()/mm
      << "], \"thickness_mm\": " << 2.0*detSolid.GetZHalfLength()/mm << "}\n";
  out << "}\n";
}
}

G4VPhysicalVolume* DetectorConstruction::Construct() {
  auto* nist = G4NistManager::Instance();
  auto* air = nist->FindOrBuildMaterial("G4_AIR");
  auto* vacuum = nist->FindOrBuildMaterial("G4_Galactic");
  auto* ge = nist->FindOrBuildMaterial("G4_Ge");

  const bool targetEnabled = g4cf::env_bool("G4CF_TARGET_ENABLED", false);
  const auto targetName = g4cf::env("G4CF_TARGET_MATERIAL", "G4_POLYETHYLENE");
  auto* targetMaterial = targetEnabled ? nist->FindOrBuildMaterial(targetName) : vacuum;
  if (!targetMaterial) throw std::runtime_error("Unable to build target material: " + targetName);

  const double targetThickness = g4cf::env_double("G4CF_TARGET_THICKNESS_MM", 50.0) * mm;
  const double baseline = g4cf::env_double("G4CF_DETECTOR_BASELINE_MM", 1000.0) * mm;

  auto* worldSolid = new G4Box("World", 1.5*m, 1.5*m, 3.0*m);
  auto* worldLV = new G4LogicalVolume(worldSolid, air, "WorldLV");
  auto* worldPV = new G4PVPlacement(nullptr, {}, worldLV, "WorldPV", nullptr, false, 0, true);

  auto* targetSolid = new G4Box("Target", 50*mm, 50*mm, targetThickness/2.0);
  auto* targetLV = new G4LogicalVolume(targetSolid, targetMaterial, "TargetLV");
  new G4PVPlacement(nullptr, {0,0,0}, targetLV, "TargetPV", worldLV, false, 0, true);

  const double planeThickness = 0.01*mm;
  const double planeZ = targetThickness/2.0 + 10.0*mm;
  auto* planeSolid = new G4Box("PhaseSpace", 75*mm, 75*mm, planeThickness/2.0);
  fPhaseSpaceLV = new G4LogicalVolume(planeSolid, vacuum, "PhaseSpaceLV");
  new G4PVPlacement(nullptr, {0,0,planeZ}, fPhaseSpaceLV, "PhaseSpacePV", worldLV, false, 0, true);

  const double detectorThickness = 50*mm;
  auto* detSolid = new G4Box("GeDetector", 50*mm, 50*mm, detectorThickness/2.0);
  fDetectorLV = new G4LogicalVolume(detSolid, ge, "GeDetectorLV");
  const double detectorCenterZ = baseline + detectorThickness/2.0;
  new G4PVPlacement(nullptr, {0,0,detectorCenterZ}, fDetectorLV, "GeDetectorPV", worldLV, false, 0, true);

  write_constructed_geometry_report(*worldSolid, *worldLV, *targetSolid, *targetLV,
                                    *planeSolid, *fPhaseSpaceLV, planeZ,
                                    *detSolid, *fDetectorLV, detectorCenterZ,
                                    targetEnabled);
  return worldPV;
}

void DetectorConstruction::ConstructSDandField() {
  auto* sdman = G4SDManager::GetSDMpointer();
  auto* phaseSD = new PhaseSpaceSD("PhaseSpaceSD");
  auto* detectorSD = new DetectorSD("DetectorSD");
  sdman->AddNewDetector(phaseSD);
  sdman->AddNewDetector(detectorSD);
  SetSensitiveDetector(fPhaseSpaceLV, phaseSD);
  SetSensitiveDetector(fDetectorLV, detectorSD);
}
