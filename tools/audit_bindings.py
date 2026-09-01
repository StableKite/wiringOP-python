#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
m=json.loads((ROOT/'api_manifest.json').read_text())
errors=[]; cf=cs=fields=vars_=macs=0
for h in m['headers']:
    cpp=(ROOT/'src'/Path(h['path']).with_suffix('.cpp')).read_text()
    test=(ROOT/'tests'/Path(h['path']).with_suffix('.py')).read_text()
    for f in h.get('functions',[]):
        cf+=1
        if f['python_name'] not in cpp: errors.append(f"{h['path']}: function binding missing {f['python_name']}")
        if f['python_name'] not in test: errors.append(f"{h['path']}: function test missing {f['python_name']}")
    for s in h.get('structs',[]):
        cs+=1
        if s['python_name'] not in cpp: errors.append(f"{h['path']}: class missing {s['python_name']}")
        for fld in s.get('fields',[]):
            fields+=1
            # python_name is already the final adapted public name. Pointer/function-pointer
            # fields are emitted by the manifest with the single `_address` suffix.
            py=fld['python_name']
            if py not in cpp: errors.append(f"{h['path']}: field missing {s['python_name']}.{py}")
            if py not in test: errors.append(f"{h['path']}: field test missing {s['python_name']}.{py}")
    for v in h.get('variables',[]):
        vars_+=1; py=v['python_name']; ct=v['c_type']
        scalar_ptr='*' in ct and '[' not in ct
        tokens=[py]
        if scalar_ptr: tokens=[f'get_{py}_address',f'set_{py}_address']
        elif v.get('storage')=='static' and ('struct ' in ct) and '[' not in ct: tokens=[f'get_{py}',f'set_{py}']
        for tok in tokens:
            if tok not in cpp: errors.append(f"{h['path']}: variable binding missing {tok}")
        if not any(tok in test for tok in tokens): errors.append(f"{h['path']}: variable test missing {py}")
    for x in h.get('macros',[]):
        if not x.get('bindable'): continue
        macs+=1
        if x['python_name'] not in cpp: errors.append(f"{h['path']}: macro binding missing {x['python_name']}")
        if x['python_name'] not in test: errors.append(f"{h['path']}: macro test missing {x['python_name']}")
if errors: raise SystemExit('BINDING AUDIT FAILED\n- '+'\n- '.join(errors[:100]))
print(f'BINDING_AUDIT_OK functions={cf} structs={cs} fields={fields} variables={vars_} macros={macs}')
