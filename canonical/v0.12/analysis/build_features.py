#!/usr/bin/env python3
import argparse, json, pathlib
import numpy as np
import uproot

def select(arr, expr):
    mask = np.ones(len(arr["record_kind"]), dtype=bool)
    for term in [x.strip() for x in expr.split("&&")]:
        key, val = [x.strip() for x in term.split("==")]
        mask &= arr[key] == int(val)
    return mask

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("root_file", type=pathlib.Path); ap.add_argument("--schema", type=pathlib.Path, default=pathlib.Path(__file__).resolve().parents[1]/"schemas"/"feature-schema-v1.json"); ap.add_argument("--out", type=pathlib.Path, required=True); args=ap.parse_args()
    schema=json.loads(args.schema.read_text())
    with uproot.open(args.root_file) as f:
        tree=f["events"]
        fields={"record_kind","particle_pdg","kinetic_pre_MeV","global_time_ns","energy_deposit_MeV"}
        arr=tree.arrays(list(fields), library="np")
    vec=[]; labels=[]
    for b in schema["blocks"]:
        m=select(arr,b["selection"])
        if b["kind"]=="hist1d":
            h,_=np.histogram(arr[b["field"]][m], bins=b["bins"], range=tuple(b["range"]))
        else:
            x,y=b["fields"]; h,_,_=np.histogram2d(arr[x][m], arr[y][m], bins=tuple(b["bins"]), range=[tuple(r) for r in b["range"]]); h=h.ravel()
        vec.extend(h.astype(float)); labels.extend([f"{b['name']}:{i}" for i in range(len(h))])
    args.out.parent.mkdir(parents=True, exist_ok=True)
    np.savez(args.out, vector=np.asarray(vec), labels=np.asarray(labels), schema=json.dumps(schema, sort_keys=True))
if __name__=="__main__": main()
