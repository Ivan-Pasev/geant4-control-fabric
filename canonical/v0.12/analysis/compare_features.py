#!/usr/bin/env python3
import argparse, json, numpy as np
p=argparse.ArgumentParser(); p.add_argument('a'); p.add_argument('b'); p.add_argument('--out',required=True); x=p.parse_args()
a=np.load(x.a); b=np.load(x.b)
if not np.array_equal(a['labels'],b['labels']): raise ValueError('feature labels differ')
va=a['vector'].astype(float); vb=b['vector'].astype(float); d=vb-va
scale=np.sqrt(np.maximum(va+vb,1.0)); z=d/scale
r={'schema':'g4cf-feature-comparison-v1','n_features':int(len(d)),'l1_difference':float(np.abs(d).sum()),'l2_difference':float(np.linalg.norm(d)),
   'max_abs_poisson_diagnostic_z':float(np.max(np.abs(z))) if len(z) else 0.0,
   'bins_abs_z_gt_5':int(np.sum(np.abs(z)>5.0)),
   'note':'Poisson z is diagnostic only because feature blocks overlap and bins are not globally independent.'}
open(x.out,'w').write(json.dumps(r,indent=2)+'\n'); print(json.dumps(r,indent=2))
