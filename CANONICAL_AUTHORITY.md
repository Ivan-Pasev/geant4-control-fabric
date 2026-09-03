# Canonical Authority Contract

**Repository:** `Ivan-Pasev/geant4-control-fabric`  
**Execution generation:** GM-07 v0.12.0  
**Role:** execution mirror / CI surface  
**Scientific authority:** canonical Google Drive working tree

## Identity tuple

| Object | Canonical identity |
|---|---|
| GM-07 ZIP | `2c11a57fc102266ebe72bd0c91f5271a56040248032c447d2dfb08329953f6e1` |
| GM-07 executable/static tree | `8cc717669c23f63062f5a70806480414c23d1ecb0ede4670e369b2cd148cc3ee` |
| Geant4 version | `11.4.2` |
| Geant4 source commit | `8cc04f65977807f1848da7b958c421cd5e162f26` |
| XPhysics | `NONE` |

A run is not canonical merely because it originates from this repository. The evidence-producing path must attest the identities above according to the sealed v0.12 harness contract.

## Gate law

`REVIEW_READY` means structural/integrity admission only. It never means a physics gate passed.

Automatic paths must preserve:

`physics_gate_advance_authorized = false`

Scientific review remains required for constructed geometry, truth/genealogy scope, ROOT/MT completeness, material response and derivative realization, alongside the remaining runtime-dependent G7 gates.

## Evidence return

Expected canonical return artifact:

`GM07_RUNTIME_EVIDENCE_0.12.0.tar.gz`

The archive is untrusted on arrival and must enter the Drive evidence intake sequence:

`00_INCOMING_UNTRUSTED -> 01_QUARANTINE -> 02_REVIEW_READY -> explicit scientific adjudication -> 03_ACCEPTED_EVIDENCE`

No GitHub badge, workflow success, commit status or artifact presence may bypass that sequence.
