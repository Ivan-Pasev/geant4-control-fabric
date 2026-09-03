#!/usr/bin/env python3
import argparse, hashlib, json, math, pathlib

def sha256(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

def close(a,b,tol=1e-9):
    try: return math.isclose(float(a),float(b),rel_tol=0.0,abs_tol=tol)
    except Exception: return False

def compare_vec(name, exp, got, failures, tol=1e-9):
    if len(exp)!=len(got): failures.append(f'{name}:length'); return
    for i,(a,b) in enumerate(zip(exp,got)):
        if not close(a,b,tol): failures.append(f'{name}[{i}]:{a}!={b}')

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('declared',type=pathlib.Path)
    ap.add_argument('constructed',type=pathlib.Path)
    ap.add_argument('--out',type=pathlib.Path,required=True)
    a=ap.parse_args()
    d=json.loads(a.declared.read_text()); c=json.loads(a.constructed.read_text()); failures=[]
    if d.get('schema')!='g4cf-geometry-descriptor-v1': failures.append('bad_declared_schema')
    if c.get('schema')!='g4cf-constructed-geometry-runtime-v1': failures.append('bad_constructed_schema')
    pairs=[('world.material',d['world']['material'],c['world']['material']),('target.material',d['target']['material'],c['target']['material']),('phase_space.material',d['phase_space']['material'],c['phase_space']['material']),('detector.material',d['detector']['material'],c['detector']['material'])]
    for name,exp,got in pairs:
        if exp!=got: failures.append(f'{name}:{exp}!={got}')
    compare_vec('world.half_size_mm',d['world']['half_size_mm'],c['world']['half_size_mm'],failures)
    compare_vec('target.center_mm',d['target']['center_mm'],c['target']['center_mm'],failures)
    compare_vec('target.half_xy_mm',d['target']['half_xy_mm'],c['target']['half_xy_mm'],failures)
    compare_vec('phase_space.half_xy_mm',d['phase_space']['half_xy_mm'],c['phase_space']['half_xy_mm'],failures)
    compare_vec('detector.half_xy_mm',d['detector']['half_xy_mm'],c['detector']['half_xy_mm'],failures)
    scalars=[('target.thickness_mm',d['target']['thickness_mm'],c['target']['thickness_mm']),('phase_space.thickness_mm',d['phase_space']['thickness_mm'],c['phase_space']['thickness_mm']),('phase_space.center_z_mm',d['phase_space']['center_z_mm'],c['phase_space']['center_z_mm']),('detector.thickness_mm',d['detector']['thickness_mm'],c['detector']['thickness_mm']),('detector.center_z_mm',d['detector']['center_z_mm'],c['detector']['center_z_mm']),('detector.front_face_z_mm',d['detector']['front_face_z_mm'],c['detector']['front_face_z_mm'])]
    for name,exp,got in scalars:
        if not close(exp,got): failures.append(f'{name}:{exp}!={got}')
    expected_enabled=d['target']['state']=='material'
    if bool(c.get('target',{}).get('enabled'))!=expected_enabled: failures.append('target.enabled_mismatch')
    match=not failures
    r={'schema':'g4cf-constructed-geometry-audit-v1','run_id':c.get('run_id'),'declared_vs_constructed_match':match,'review_required':True,'automatic_geometry_acceptance':False,'declared_sha256':sha256(a.declared),'constructed_sha256':sha256(a.constructed),'failures':failures,'note':'Structural runtime geometry identity only; scientific geometry adequacy remains review-required.'}
    a.out.parent.mkdir(parents=True,exist_ok=True); a.out.write_text(json.dumps(r,indent=2)+'\n'); print(json.dumps(r,indent=2))
    return 0 if match else 2
if __name__=='__main__': raise SystemExit(main())
