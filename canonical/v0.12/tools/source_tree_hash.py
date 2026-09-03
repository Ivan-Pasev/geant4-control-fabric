#!/usr/bin/env python3
import argparse, hashlib, json, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
INCLUDE_FILES=['CMakeLists.txt','g4cf.cc','README.md','requirements.txt','runtime/expected-geant4-11.4.2-datasets.json','runtime/evidence-contract-v1.json','runtime/evidence-intake-contract-v1.json','runtime/host-execution-contract-v1.json','runtime/capsule/geant4-source-pin.json','runtime/capsule/GM07_RUNTIME_CAPSULE_CONTRACT.md']
INCLUDE_DIRS=['scripts','include','src','macros','manifests','schemas','tools','analysis','tests','.github']
EXCLUDE_NAMES={'source-tree-identity.json','runtime-audit.json','campaign-report.json','campaign-next.json','audit-next.json'}

def iter_files(root):
    for rel in INCLUDE_FILES:
        p=root/rel
        if p.is_file(): yield p
    for rel in INCLUDE_DIRS:
        d=root/rel
        if not d.exists(): continue
        for p in d.rglob('*'):
            if p.is_file() and p.name not in EXCLUDE_NAMES and '__pycache__' not in p.parts:
                yield p

def compute(root):
    h=hashlib.sha256(); records=[]
    for p in sorted(iter_files(root), key=lambda x:x.relative_to(root).as_posix()):
        rel=p.relative_to(root).as_posix(); b=p.read_bytes(); sh=hashlib.sha256(b).hexdigest()
        records.append({'path':rel,'size':len(b),'sha256':sh})
        h.update(rel.encode()+b'\0'+bytes.fromhex(sh))
    return h.hexdigest(),records

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',type=pathlib.Path,default=ROOT); ap.add_argument('--out',type=pathlib.Path)
    a=ap.parse_args(); digest,records=compute(a.root.resolve()); obj={'schema':'g4cf-source-tree-identity-v1','sha256':digest,'files':records}
    if a.out: a.out.write_text(json.dumps(obj,indent=2)+'\n')
    else: print(json.dumps(obj,indent=2))
if __name__=='__main__': main()
