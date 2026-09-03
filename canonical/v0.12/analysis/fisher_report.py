#!/usr/bin/env python3
import argparse, json, numpy as np
from linear_algebra import fisher
p=argparse.ArgumentParser(); p.add_argument("jacobian_npz"); p.add_argument("covariance_npy"); p.add_argument("--out",required=True); a=p.parse_args()
j=np.load(a.jacobian_npz)["J"]; v=np.load(a.covariance_npy); I=fisher(j,v); w=np.linalg.eigvalsh((I+I.T)/2); sign,ld=np.linalg.slogdet(I); report={"shape":list(I.shape),"eigenvalues":w.tolist(),"logdet":float(ld) if sign>0 else None,"condition":float(w.max()/w.min()) if np.all(w>0) else None}; open(a.out,"w").write(json.dumps(report,indent=2))
