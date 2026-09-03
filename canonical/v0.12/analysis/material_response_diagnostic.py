#!/usr/bin/env python3
import argparse, json, pathlib
import numpy as np

def block_name(label):
    s=str(label)
    return s.split(':',1)[0] if ':' in s else s

def main():
    ap=argparse.ArgumentParser(description='Quantify RUN_002 vs RUN_005 feature differences without automatically adjudicating physical consistency.')
    ap.add_argument('control_features',type=pathlib.Path)
    ap.add_argument('material_features',type=pathlib.Path)
    ap.add_argument('--out',type=pathlib.Path,required=True)
    a=ap.parse_args()
    c=np.load(a.control_features,allow_pickle=False); m=np.load(a.material_features,allow_pickle=False)
    if not np.array_equal(c['labels'],m['labels']): raise ValueError('feature labels differ')
    labels=c['labels'].astype(str); vc=c['vector'].astype(float); vm=m['vector'].astype(float)
    if vc.shape != vm.shape: raise ValueError('feature vector shapes differ')
    d=vm-vc; scale=np.sqrt(np.maximum(vc+vm,1.0)); z=d/scale
    blocks={}
    for name in sorted(set(block_name(x) for x in labels)):
        mask=np.array([block_name(x)==name for x in labels],dtype=bool)
        csum=float(vc[mask].sum()); msum=float(vm[mask].sum()); delta=msum-csum
        blocks[name]={
            'control_sum':csum,'material_sum':msum,'delta':delta,
            'fractional_delta_vs_control':None if csum==0 else float(delta/csum),
            'max_abs_poisson_diagnostic_z':float(np.max(np.abs(z[mask]))) if np.any(mask) else 0.0,
            'bins_abs_z_gt_5':int(np.sum(np.abs(z[mask])>5.0)) if np.any(mask) else 0,
        }
    report={
        'schema':'g4cf-material-response-diagnostic-v1',
        'control_features':str(a.control_features),
        'material_features':str(a.material_features),
        'n_features':int(len(d)),
        'l1_difference':float(np.abs(d).sum()),
        'l2_difference':float(np.linalg.norm(d)),
        'max_abs_poisson_diagnostic_z':float(np.max(np.abs(z))) if len(z) else 0.0,
        'bins_abs_z_gt_5':int(np.sum(np.abs(z)>5.0)),
        'blocks':blocks,
        'review_required':True,
        'automatic_physics_acceptance':False,
        'note':'Diagnostics quantify finite-sample feature differences only. Overlapping feature blocks, transport correlations and model/systematic context prohibit automatic physical acceptance from this report.'
    }
    a.out.parent.mkdir(parents=True,exist_ok=True); a.out.write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps(report,indent=2))
    return 0
if __name__=='__main__': raise SystemExit(main())
