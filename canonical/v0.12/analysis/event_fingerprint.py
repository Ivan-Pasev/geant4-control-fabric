#!/usr/bin/env python3
import argparse, hashlib, json, pathlib
import numpy as np
import uproot

FIELDS=["event_id","record_kind","track_id","parent_id","step_id","particle_pdg","creator_process","step_process","volume_id","material_id","x_mm","y_mm","z_mm","px_MeV","py_MeV","pz_MeV","kinetic_pre_MeV","kinetic_post_MeV","energy_deposit_MeV","global_time_ns","source_weight","event_weight","detector_channel"]

def scalar(v):
    if isinstance(v, bytes): return v.decode("utf-8")
    if hasattr(v,"item"): return v.item()
    return v

def main():
    p=argparse.ArgumentParser(); p.add_argument("root_file",type=pathlib.Path); p.add_argument("--out",type=pathlib.Path,required=True); a=p.parse_args()
    with uproot.open(a.root_file) as f: arr=f["events"].arrays(FIELDS,library="np")
    events={}
    for i,e in enumerate(arr["event_id"]): events.setdefault(int(e),[]).append(i)
    hashes={}
    for eid, idxs in events.items():
        idxs=sorted(idxs,key=lambda i:(int(arr["track_id"][i]),int(arr["step_id"][i]),int(arr["record_kind"][i]),str(scalar(arr["detector_channel"][i]))))
        rows=[[scalar(arr[k][i]) for k in FIELDS if k!="event_id"] for i in idxs]
        payload=json.dumps(rows,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()
        hashes[str(eid)]=hashlib.sha256(payload).hexdigest()
    a.out.parent.mkdir(parents=True,exist_ok=True); a.out.write_text(json.dumps({"schema":"g4cf-event-fingerprint-v1","source":str(a.root_file),"fields":FIELDS,"events":hashes},indent=2,sort_keys=True))
if __name__=="__main__": main()
