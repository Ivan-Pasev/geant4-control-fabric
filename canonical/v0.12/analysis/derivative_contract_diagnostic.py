#!/usr/bin/env python3
import argparse, hashlib, json, pathlib
import numpy as np

def sha256(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--nominal-manifest',type=pathlib.Path,required=True)
    ap.add_argument('--minus-manifest',type=pathlib.Path,required=True)
    ap.add_argument('--plus-manifest',type=pathlib.Path,required=True)
    ap.add_argument('--minus-source-validation',type=pathlib.Path,required=True)
    ap.add_argument('--plus-source-validation',type=pathlib.Path,required=True)
    ap.add_argument('--jacobian',type=pathlib.Path,required=True)
    ap.add_argument('--out',type=pathlib.Path,required=True)
    a=ap.parse_args(); failures=[]
    nm=json.loads(a.nominal_manifest.read_text()); mm=json.loads(a.minus_manifest.read_text()); pm=json.loads(a.plus_manifest.read_text())
    ms=json.loads(a.minus_source_validation.read_text()); ps=json.loads(a.plus_source_validation.read_text())
    mn=mm.get('nuisance',{}); pn=pm.get('nuisance',{})
    name=mn.get('name'); nominal=float(mn.get('nominal')); nominal_manifest_energy=float(nm['source']['energy_MeV']); em=float(mm['source']['energy_MeV']); ep=float(pm['source']['energy_MeV'])
    h=(ep-em)/2.0
    checks={
      'nuisance_name_match': name==pn.get('name')=='source_energy_MeV',
      'nominal_match': float(pn.get('nominal'))==nominal and abs(nominal_manifest_energy-nominal)<1e-12,
      'symmetric_manifest_energies': abs(((em+ep)/2.0)-nominal) < 1e-12 and h>0,
      'manifest_steps_match_energies': abs(float(mn.get('step'))-(em-nominal))<1e-12 and abs(float(pn.get('step'))-(ep-nominal))<1e-12,
      'pipeline_status_provisional': mn.get('status')==pn.get('status')=='PROVISIONAL_PIPELINE_TEST_NOT_CALIBRATION_UNCERTAINTY',
      'minus_source_validation_pass': ms.get('pass') is True and ms.get('run_id')==mm.get('run_id'),
      'plus_source_validation_pass': ps.get('pass') is True and ps.get('run_id')==pm.get('run_id'),
    }
    try:
        z=np.load(a.jacobian,allow_pickle=False)
        params=[str(x) for x in z['parameter_names'].tolist()]
        jh=float(z['h'])
        checks['jacobian_parameter_name']=params==['source_energy_MeV']
        checks['jacobian_h_matches_manifest']=abs(jh-h)<1e-12
        checks['jacobian_shape_consistent']=z['J'].ndim==2 and z['J'].shape[1]==1 and z['derivative'].shape[0]==z['J'].shape[0]
    except Exception as e:
        checks['jacobian_readable']=False; failures.append(f'jacobian_read_error:{type(e).__name__}:{e}')
    for k,v in checks.items():
        if v is not True: failures.append(k)
    report={'schema':'g4cf-derivative-contract-diagnostic-v1','parameter':'source_energy_MeV','nominal_MeV':nominal,'minus_MeV':em,'plus_MeV':ep,'h_MeV':h,
            'pipeline_contract_pass':not failures,'review_required':True,'automatic_physics_acceptance':False,'checks':checks,
            'input_sha256':{'nominal_manifest':sha256(a.nominal_manifest),'minus_manifest':sha256(a.minus_manifest),'plus_manifest':sha256(a.plus_manifest),
              'minus_source_validation':sha256(a.minus_source_validation),'plus_source_validation':sha256(a.plus_source_validation),'jacobian':sha256(a.jacobian)},
            'failures':failures,
            'note':'This diagnostic proves that the provisional source-energy perturbation was actually generated and bound to the Jacobian input. It is not a calibrated physical nuisance uncertainty and does not scientifically validate the derivative magnitude.'}
    a.out.parent.mkdir(parents=True,exist_ok=True); a.out.write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps(report,indent=2))
    return 0 if report['pipeline_contract_pass'] else 2
if __name__=='__main__': raise SystemExit(main())
