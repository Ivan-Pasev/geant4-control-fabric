cmake_minimum_required(VERSION 3.16...3.27)
project(g4_control_fabric VERSION 0.12.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

option(G4CF_WITH_UIVIS "Enable all installed Geant4 UI/visualization drivers" OFF)
if(G4CF_WITH_UIVIS)
  find_package(Geant4 11.4 REQUIRED ui_all vis_all)
else()
  find_package(Geant4 11.4 REQUIRED)
endif()

if(NOT Geant4_VERSION VERSION_GREATER_EQUAL "11.4" OR NOT Geant4_VERSION VERSION_LESS "11.5")
  message(FATAL_ERROR "GM-07 canonical runtime requires Geant4 11.4.x; found ${Geant4_VERSION}")
endif()

set(G4CF_SOURCES
  g4cf.cc
  src/ActionInitialization.cc
  src/AnalysisRecord.cc
  src/DetectorConstruction.cc
  src/DetectorSD.cc
  src/PhaseSpaceSD.cc
  src/PhysicsListLoader.cc
  src/PrimaryGeneratorAction.cc
  src/ProvenanceLedger.cc
  src/RunAction.cc
)

add_executable(g4cf ${G4CF_SOURCES})
target_include_directories(g4cf PRIVATE ${PROJECT_SOURCE_DIR}/include)
target_link_libraries(g4cf PRIVATE ${Geant4_LIBRARIES})

target_compile_definitions(g4cf PRIVATE G4CF_VERSION=\"${PROJECT_VERSION}\")

install(TARGETS g4cf DESTINATION bin)
