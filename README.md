# Geant4 Control Fabric — GM-07

Canonical execution mirror for the GILC Geant4 Control Fabric.

## Authority

Google Drive remains the **scientific and constitutional authority**. This repository is an execution/CI mirror; GitHub status alone never advances a physics gate.

Current sealed source generation: **GM-07 v0.12.0**.

- Canonical bundle: `g4-control-harness-gm07-v0.12.0.zip`
- Bundle SHA-256: `2c11a57fc102266ebe72bd0c91f5271a56040248032c447d2dfb08329953f6e1`
- Authority-tree SHA-256: `8cc717669c23f63062f5a70806480414c23d1ecb0ede4670e369b2cd148cc3ee`
- Geant4 target: **11.4.2**
- Pinned Geant4 source commit: `8cc04f65977807f1848da7b958c421cd5e162f26`
- XPhysics: **NONE**

## Invariants

1. `REVIEW_READY != GATE_ACCEPTED`.
2. Automated workflows set no scientific gate to PASS.
3. The canonical evidence-producing path must prove the unchanged GM-07 source identity and exact pinned Geant4 source identity.
4. CI that cannot prove those identities is explicitly **NON-EVIDENTIARY**.
5. Returned runtime evidence enters Drive quarantine before scientific adjudication.

## Runtime frontier

The first evidentiary campaign must generate the required `RUN_002`, `RUN_005`, MT/reproducibility and source-energy perturbation (`nu-`, `nu+`) corpus, plus geometry, truth-schema, ROOT/MT, material-response and derivative diagnostics. The expected return artifact is:

`GM07_RUNTIME_EVIDENCE_0.12.0.tar.gz`

Until that corpus is produced and reviewed, the canonical state remains:

`GM07_RUNTIME = BLOCKED_NO_GEANT4`

## Repository bootstrap state

This repository has been bound to the sealed v0.12 authority. Source materialization and runner activation must preserve the hashes above; do not substitute reconstructed or modified source while retaining the canonical version label.
