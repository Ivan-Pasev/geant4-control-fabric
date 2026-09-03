#!/usr/bin/env python3
import argparse, hashlib, json, pathlib
import numpy as np
import uproot

def sha256(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

REQUIRED_BRANCHES={
 'record_kind','run_id','event_id','track_id','parent_id','step_id','particle_pdg',
 'creator_process','step_process','volume_id','material_id','x_mm','y_mm','z_mm',
 'px_MeV','py_MeV','pz_MeV','kinetic_pre_MeV','kinetic_post_MeV',
 'energy_deposit_MeV','global_time_ns','source_weight','event_weight',
 'genealogy_class','detector_channel'}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('root_file',type=pathlib.Path); ap.add_argument('manifest',type=pathlib.Path)
    ap.add_argument('--out',type=pathlib.Path,required=True); a=ap.parse_args()
    m=json.loads(a.manifest.read_text()); failures=[]
    with uproot.open(a.root_file) as f:
        if 'events' not in f: failures.append('missing_events_tree'); branches=set(); arr={}
        else:
            tree=f['events']; branches=set(tree.keys()); missing=sorted(REQUIRED_BRANCHES-branches)
            if missing: failures.append('missing_branches:'+','.join(missing))
            fields=['record_kind','event_id','track_id','parent_id','step_id','particle_pdg']
            arr=tree.arrays([x for x in fields if x in branches],library='np')
    kinds=np.asarray(arr.get('record_kind',[]),dtype=int); allowed={0,1,2}
    bad=sorted(set(kinds.tolist())-allowed)
    if bad: failures.append('unknown_record_kinds:'+','.join(map(str,bad)))
    counts={str(k):int(np.count_nonzero(kinds==k)) for k in sorted(allowed)}
    primary=(kinds==2)
    expected_events=int(m['events'])
    primary_count=int(np.count_nonzero(primary))
    primary_contract=True
    if primary_count!=expected_events: failures.append(f'primary_count:{primary_count}!={expected_events}'); primary_contract=False
    if primary_count:
        pdg=np.asarray(arr['particle_pdg'])[primary]
        if not np.all(pdg==2112): failures.append('primary_pdg_not_all_neutron'); primary_contract=False
        for key in ('track_id','parent_id','step_id'):
            vals=np.asarray(arr[key])[primary]
            if not np.all(vals==-1): failures.append(f'primary_{key}_not_minus_one'); primary_contract=False
        eids=np.asarray(arr['event_id'])[primary]
        if len(np.unique(eids))!=expected_events: failures.append('primary_event_ids_not_unique_complete'); primary_contract=False
    if m.get('role')=='open_beam_anchor' and counts['0']==0: failures.append('open_beam_has_no_phase_space_records')
    structural=not failures
    r={'schema':'g4cf-truth-schema-audit-v1','run_id':m['run_id'],'structural_schema_pass':structural,
       'primary_contract_pass':primary_contract,'required_branches':sorted(REQUIRED_BRANCHES),
       'present_branches':sorted(branches),'record_kind_counts':counts,
       'genealogy_scope':'SCORED_RECORDS_ONLY_NOT_COMPLETE_ALL_TRACK_HISTORY',
       'review_required':True,'automatic_genealogy_acceptance':False,'root_sha256':sha256(a.root_file),'manifest_sha256':sha256(a.manifest),'failures':failures,
       'note':'The ntuple records primaries and scored phase-space/detector steps. It does not claim complete all-interaction genealogy.'}
    a.out.parent.mkdir(parents=True,exist_ok=True); a.out.write_text(json.dumps(r,indent=2)+'\n'); print(json.dumps(r,indent=2))
    return 0 if structural else 2
if __name__=='__main__': raise SystemExit(main())
