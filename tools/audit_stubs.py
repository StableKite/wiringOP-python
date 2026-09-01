#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
m=json.loads((ROOT/'api_manifest.json').read_text())
errors=[]; funcs=classes=fields=vars_=macs=0
for h in m['headers']:
    p=ROOT/'stubs'/Path(h['path']).with_suffix('.pyi')
    if not p.is_file(): errors.append(f'missing {p.relative_to(ROOT)}'); continue
    s=p.read_text()
    if re.search(r'\barg\d+\b',s): errors.append(f'{h["path"]}: accidental argN name')
    for f in h.get('functions',[]):
        funcs+=1
        if not re.search(rf'\bdef\s+{re.escape(f["python_name"])}\s*\(',s): errors.append(f'{h["path"]}: missing def {f["python_name"]}')
    for st in h.get('structs',[]):
        classes+=1
        if not re.search(rf'\bclass\s+{re.escape(st["python_name"])}\b',s): errors.append(f'{h["path"]}: missing class {st["python_name"]}')
        for fld in st.get('fields',[]):
            fields+=1; py=fld['python_name']
            if py not in s: errors.append(f'{h["path"]}: missing field {st["python_name"]}.{py}')
    for v in h.get('variables',[]):
        vars_+=1; py=v['python_name']; ct=v['c_type']; scalar_ptr='*' in ct and '[' not in ct
        if scalar_ptr: toks=[f'get_{py}_address',f'set_{py}_address']
        elif v.get('storage')=='static' and 'struct ' in ct and '[' not in ct: toks=[f'get_{py}',f'set_{py}']
        else: toks=[py]
        for tok in toks:
            if tok not in s: errors.append(f'{h["path"]}: missing variable surface {tok}')
    for x in h.get('macros',[]):
        if x.get('bindable'):
            macs+=1
            if x['python_name'] not in s: errors.append(f'{h["path"]}: missing macro {x["python_name"]}')
    if h['path']=='wiringPi/wiringSerial.h':
        for tok in ('class SerialPort','cancel_read','cancel_write','read_into','readinto','rs485_mode','rx_trigger'):
            if tok not in s: errors.append(f'wiringSerial stub missing {tok}')
if errors: raise SystemExit('STUB AUDIT FAILED\n- '+'\n- '.join(errors[:120]))
print(f'STUB_AUDIT_OK functions={funcs} classes={classes} fields={fields} variables={vars_} macros={macs}')
