#pragma once
#include <string>
class G4VModularPhysicsList;
namespace g4cf { G4VModularPhysicsList* LoadReferencePhysicsList(const std::string& name); }
