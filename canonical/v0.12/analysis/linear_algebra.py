import numpy as np

def _symmetric_eigensystem(a):
    a=np.asarray(a,float)
    if a.ndim!=2 or a.shape[0]!=a.shape[1]: raise ValueError("matrix must be square")
    s=(a+a.T)/2
    return np.linalg.eigh(s)

def symmetric_pinv(a, rtol=1e-12, negative_rtol=1e-10):
    w,q=_symmetric_eigensystem(a); scale=max(1.0,float(np.max(np.abs(w))))
    if np.min(w) < -negative_rtol*scale: raise ValueError(f"matrix is not positive semidefinite: min eigenvalue={np.min(w)}")
    cut=rtol*scale; keep=w>cut; inv=np.zeros_like(w); inv[keep]=1.0/w[keep]
    return (q*inv)@q.T, w, keep

def whitening(v, rtol=1e-12, negative_rtol=1e-10):
    w,q=_symmetric_eigensystem(v); scale=max(1.0,float(np.max(np.abs(w))))
    if np.min(w) < -negative_rtol*scale: raise ValueError(f"covariance is not positive semidefinite: min eigenvalue={np.min(w)}")
    cut=rtol*scale; keep=w>cut; iw=np.zeros_like(w); iw[keep]=1.0/np.sqrt(w[keep])
    return (q*iw)@q.T, w, keep

def fisher(j, v, prior_precision=None, rtol=1e-12):
    j=np.asarray(j,float)
    if j.ndim==1: j=j[:,None]
    vinv,_,_=symmetric_pinv(v,rtol); out=j.T@vinv@j
    return out if prior_precision is None else out+prior_precision

def nuisance_projector(jnu, v, rtol=1e-12):
    jnu=np.asarray(jnu,float)
    if jnu.ndim==1: jnu=jnu[:,None]
    w,_,_=whitening(v,rtol); u=w@jnu
    q,s,_=np.linalg.svd(u,full_matrices=False)
    keep=s>rtol*max(1.0,float(s[0]) if len(s) else 1.0); qk=q[:,keep]
    return qk@qk.T, s, keep
