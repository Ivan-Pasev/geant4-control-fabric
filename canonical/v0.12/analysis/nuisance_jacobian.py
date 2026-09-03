#!/usr/bin/env python3
import argparse, numpy as np
p=argparse.ArgumentParser(); p.add_argument("minus"); p.add_argument("plus"); p.add_argument("--h",type=float,required=True); p.add_argument("--parameter-name",default="UNSPECIFIED"); p.add_argument("--out",required=True); a=p.parse_args()
if a.h <= 0: raise ValueError("--h must be positive")
m=np.load(a.minus); q=np.load(a.plus)
if not np.array_equal(m["labels"], q["labels"]): raise ValueError("feature labels differ between minus/plus states")
d=(q["vector"]-m["vector"])/(2*a.h)
# Canonical Jacobian representation is n_observables x n_parameters.
J=d[:,None]
np.savez(a.out, J=J, derivative=d, labels=q["labels"], parameter_names=np.asarray([a.parameter_name]), h=a.h)
