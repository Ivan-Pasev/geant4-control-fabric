#!/usr/bin/env python3
import argparse,json
p=argparse.ArgumentParser(); p.add_argument("a"); p.add_argument("b"); p.add_argument("--out"); x=p.parse_args()
a=json.load(open(x.a)); b=json.load(open(x.b)); ka=set(a["events"]); kb=set(b["events"]); common=sorted(ka&kb,key=int); mism=[k for k in common if a["events"][k]!=b["events"][k]]
r={"schema":"g4cf-fingerprint-comparison-v1","events_a":len(ka),"events_b":len(kb),"common":len(common),"missing_from_a":sorted(kb-ka,key=int),"missing_from_b":sorted(ka-kb,key=int),"mismatched":mism,"bitwise_event_reproducible":(ka==kb and not mism)}
text=json.dumps(r,indent=2); print(text)
if x.out: open(x.out,"w").write(text+"\n")
raise SystemExit(0 if r["bitwise_event_reproducible"] else 1)
