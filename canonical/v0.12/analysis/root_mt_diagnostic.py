#!/usr/bin/env python3
import argparse, hashlib, json, pathlib
import numpy as np
import uproot

ROOT=pathlib.Path(__file__).resolve().parents[1]
CONTRACT=json.loads((ROOT/'runtime/evidence-contract-v1.json').read_text())

def sha256(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo-root',type=pathlib.Path,default=ROOT)
    ap.add_argument('--out',type=pathlib.Path,required=True)
    a=ap.parse_args(); base=a.repo_root.resolve(); failures=[]; runs={}
    mmap=CONTRACT.get('run_manifest_map',{})
    for rid in CONTRACT['required_run_ids']:
        mpath=base/mmap[rid]; rpath=base/f'results/{rid}/events.root'
        entry={'manifest':str(mpath),'root':str(rpath)}; runs[rid]=entry
        if not mpath.is_file(): failures.append(f'{rid}:missing_manifest'); continue
        if not rpath.is_file(): failures.append(f'{rid}:missing_root'); continue
        m=json.loads(mpath.read_text()); entry.update({'manifest_sha256':sha256(mpath),'root_sha256':sha256(rpath),'expected_events':int(m['events']),'run_manager':m.get('run_manager'),'threads':int(m.get('threads',0))})
        if m.get('run_id')!=rid: failures.append(f'{rid}:manifest_run_id_mismatch')
        if m.get('run_manager')=='MTOnly' and int(m.get('threads',0))<2: failures.append(f'{rid}:mt_threads_lt_2')
        if m.get('run_manager')=='SerialOnly' and int(m.get('threads',0))!=1: failures.append(f'{rid}:serial_threads_not_1')
        try:
            with uproot.open(rpath) as f:
                if 'events' not in f: failures.append(f'{rid}:missing_events_tree'); continue
                tree=f['events']; branches=set(tree.keys())
                for req in ('record_kind','event_id'):
                    if req not in branches: failures.append(f'{rid}:missing_branch_{req}')
                if not {'record_kind','event_id'} <= branches: continue
                arr=tree.arrays(['record_kind','event_id'],library='np')
            kinds=np.asarray(arr['record_kind'],dtype=int); eids=np.asarray(arr['event_id'],dtype=np.int64)
            pe=eids[kinds==2]; n_expected=int(m['events']); unique=np.unique(pe)
            entry['primary_records']=int(pe.size); entry['unique_primary_event_ids']=int(unique.size)
            entry['primary_event_id_min']=int(unique.min()) if unique.size else None
            entry['primary_event_id_max']=int(unique.max()) if unique.size else None
            complete=(pe.size==n_expected and unique.size==n_expected and (n_expected==0 or (unique[0]==0 and unique[-1]==n_expected-1)))
            entry['complete_primary_event_population']=bool(complete)
            if not complete: failures.append(f'{rid}:incomplete_primary_event_population')
        except Exception as e:
            failures.append(f'{rid}:root_read_error:{type(e).__name__}:{e}')
    pass_structural=not failures
    report={'schema':'g4cf-root-mt-diagnostic-v1','required_run_ids':CONTRACT['required_run_ids'],'runs':runs,
            'structural_root_mt_pass':pass_structural,'review_required':True,'automatic_root_mt_acceptance':False,
            'failures':failures,
            'note':'This diagnostic proves ROOT readability and complete Primary event population for the declared run corpus, including MT outputs. It does not by itself scientifically validate MT transport or detector distributions.'}
    a.out.parent.mkdir(parents=True,exist_ok=True); a.out.write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps(report,indent=2))
    return 0 if pass_structural else 2
if __name__=='__main__': raise SystemExit(main())
