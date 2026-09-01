#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
m=json.loads((ROOT/'api_manifest.json').read_text())
errors=[]; symbols=0
for h in m['headers']:
    doc=(ROOT/'docs'/Path(h['path']).with_suffix('.md')).read_text()
    required=[]
    for f in h.get('functions',[]): required += [f['c_name'],f['python_name']]
    for s in h.get('structs',[]):
        required += [s['c_name'],s['python_name']]
        for fld in s.get('fields',[]): required += [fld['name'],fld['python_name']]
    for v in h.get('variables',[]): required += [v['c_name'],v['python_name']]
    for x in h.get('macros',[]): required += [x['c_name']]
    for tok in dict.fromkeys(required):
        symbols+=1
        if tok and tok not in doc: errors.append(f"{h['path']}: undocumented {tok}")
    if h['path']=='wiringPi/wiringSerial.h':
        for tok in ('SerialPort','RS-485','RK3588','cancel_read','cancel_write','rx_trigger'):
            if tok not in doc: errors.append(f'wiringSerial docs missing advanced topic {tok}')
if errors: raise SystemExit('DOC AUDIT FAILED\n- '+'\n- '.join(errors[:100]))
print(f'DOC_AUDIT_OK headers={len(m["headers"])} symbol_references={symbols}')
