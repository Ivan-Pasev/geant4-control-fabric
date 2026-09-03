#!/usr/bin/env python3
import argparse, json, math, pathlib
import numpy as np
import uproot

FIELDS=['record_kind','event_id','particle_pdg','x_mm','y_mm','z_mm','px_MeV','py_MeV','pz_MeV','kinetic_pre_MeV','global_time_ns','source_weight']

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('root_file',type=pathlib.Path); ap.add_argument('manifest',type=pathlib.Path); ap.add_argument('--out',type=pathlib.Path,required=True); a=ap.parse_args()
    m=json.loads(a.manifest.read_text()); src=m['source']; n_expected=int(m['events'])
    with uproot.open(a.root_file) as f: arr=f['events'].arrays(FIELDS,library='np')
    mask=arr['record_kind']==2
    n=int(mask.sum())
    def stats(k):
        x=np.asarray(arr[k][mask],float); return {'mean':float(x.mean()) if len(x) else None,'std':float(x.std()) if len(x) else None,'min':float(x.min()) if len(x) else None,'max':float(x.max()) if len(x) else None}
    p=np.column_stack([arr['px_MeV'][mask],arr['py_MeV'][mask],arr['pz_MeV'][mask]]).astype(float) if n else np.empty((0,3))
    pmag=np.linalg.norm(p,axis=1) if n else np.empty(0); direction=np.divide(p,pmag[:,None],out=np.zeros_like(p),where=pmag[:,None]!=0) if n else p
    exp_dir=np.asarray(src['direction'],float); exp_dir=exp_dir/np.linalg.norm(exp_dir)
    pos=np.column_stack([arr['x_mm'][mask],arr['y_mm'][mask],arr['z_mm'][mask]]).astype(float) if n else np.empty((0,3))
    exp_pos=np.asarray(src['position_mm'],float)
    tol=1e-10
    checks={
      'primary_count': n==n_expected,
      'one_primary_per_event': n==n_expected and len(np.unique(arr['event_id'][mask]))==n_expected,
      'pdg_neutron': n>0 and bool(np.all(arr['particle_pdg'][mask]==2112)),
      'energy_mono': n>0 and bool(np.allclose(arr['kinetic_pre_MeV'][mask],float(src['energy_MeV']),rtol=0,atol=tol)),
      'position': n>0 and bool(np.allclose(pos,exp_pos[None,:],rtol=0,atol=tol)),
      'direction': n>0 and bool(np.allclose(direction,exp_dir[None,:],rtol=0,atol=tol)),
      'time_zero': n>0 and bool(np.allclose(arr['global_time_ns'][mask],0.0,rtol=0,atol=tol)),
    }
    report={'schema':'g4cf-source-validation-v1','run_id':m['run_id'],'records':n,'expected_records':n_expected,'checks':checks,'pass':all(checks.values()),
            'stats':{k:stats(k) for k in ['kinetic_pre_MeV','x_mm','y_mm','z_mm','global_time_ns','source_weight']}}
    a.out.parent.mkdir(parents=True,exist_ok=True); a.out.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n'); print(json.dumps(report,indent=2))
    return 0 if report['pass'] else 1
if __name__=='__main__': raise SystemExit(main())
