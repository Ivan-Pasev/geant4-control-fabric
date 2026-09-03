# GM-07 Runtime Capsule Contract — v0.12

The capsule exists to make the next runtime gate portable without weakening provenance.

## Admission states
1. `SOURCE_PINNED`: upstream Geant4 11.4.2 source identity is explicit.
2. `GEANT4_BUILT`: Geant4 configure/build/install completed and installation paths are recorded.
3. `READY_FOR_BUILD`: runtime audit verifies Geant4 11.4.x and build tooling.
4. `READY_FOR_TRANSPORT`: required installed dataset audit passes.
5. `HARNESS_BUILT`: GM-07 C++ configure/build/link passes against that runtime.
6. `SMOKE_PASSED`: 100-event plumbing smoke completes; this is not physics validation.
7. `CONTROL_CAMPAIGN_EXECUTED`: canonical RUN_002 family, RUN_005 and nuisance branches execute.
8. `REVIEW_PENDING`: source, constructed-geometry, truth-schema, MT reproducibility, ROOT/artifact, material-response and derivative diagnostics exist for adjudication.

No state is inferred from a later state. Every runtime artifact is hashed and imported into Drive before a gate is marked closed.

## Source pin
- Geant4 tag: `v11.4.2`
- Git commit: `8cc04f65977807f1848da7b958c421cd5e162f26`
- Official repository: `Geant4/geant4`

## Dataset policy
The default bootstrap uses `GEANT4_INSTALL_DATA=ON`. Geant4's installation guide states datasets are not required to build Geant4 but may be required by applications/physics models. GM-07 therefore keeps build admission separate from transport admission and checks installed datasets before Shielding transport.

## Reproducibility boundary
- MT4 repeat and MT4↔MT2: event-fingerprint tests under `/run/eventModulo 0 0`.
- Serial↔MT: aggregate feature/distribution diagnostic unless a stronger equality is separately established.
- `RUN_002_SMOKE`: plumbing only.


## Evidence return admission — v0.8
A completed full campaign must be wrapped by `build_evidence_bundle.py`. The returned evidence is content-addressed and then checked by `adjudicate_evidence.py`. Automatic adjudication is capped at `REVIEW_READY`; it never authorizes a scientific gate advance. Exact pinned Git source identity is required for automatic REVIEW_READY. Version-only offline source trees remain scientifically reviewable but are not automatically admitted as canonical evidence.

## External host handoff — v0.8

The runtime capsule has a single host orchestration surface: `tools/execute_external_host.py`. Supported operator host families are Linux and WSL2. Before any full evidentiary campaign, the executing harness tree must match the externally supplied canonical source-tree SHA-256 and the original GM07 transport ZIP must be locally hash-verified against the externally supplied canonical bundle SHA-256. Geant4 network fetch and a local Git source directory at the pinned commit are full-campaign source modes. A normal source archive/non-Git directory may be used only for smoke/build investigation under the current evidence law because version-only source identity cannot prove the pinned commit. Completion produces a content-addressed evidence return archive whose automatic status ceiling is `RETURN_READY_UNTRUSTED_ARCHIVE`; Drive intake and explicit scientific adjudication remain mandatory.


## v0.11 evidence-completeness boundary
A package may reach `REVIEW_READY` only when RUN_002 and RUN_005 include both the manifest-derived geometry descriptor and a geometry report emitted by the running C++ construction path, together with a declared-vs-constructed audit. The ROOT truth schema is also audited explicitly. That audit freezes the genealogy scope as `SCORED_RECORDS_ONLY_NOT_COMPLETE_ALL_TRACK_HISTORY`; it must not be interpreted as complete event genealogy.

The bundled GitHub Actions workflow is non-evidentiary CI/runtime portability only. It does not possess or verify the original canonical GM07 ZIP bytes and therefore must not build or self-adjudicate a canonical evidence package. The Linux/WSL external-host path remains the canonical evidence-producing route.


## v0.12 evidence-completeness extension

A full canonical campaign validates generated Primary source state for every required run, including both source-energy perturbation branches. Structural admission also requires a ROOT/MT completeness diagnostic bound to all returned ROOT/manifest pairs and a derivative-contract diagnostic bound to the perturbation manifests, source-validation reports, and Jacobian artifact. Both diagnostics remain review-required and cannot automatically authorize scientific gate closure.
