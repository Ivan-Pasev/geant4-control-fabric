#pragma once
#include <string>
class G4Event;
class G4Step;
namespace g4cf {
enum class RecordKind : int { PhaseSpace = 0, DetectorStep = 1, Primary = 2 };
void CreateEventNtuple();
void FillPrimaryRecords(const G4Event& event);
void FillStepRecord(RecordKind kind, const G4Step& step, const std::string& channel);
}
