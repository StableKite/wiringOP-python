#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re, subprocess, tempfile
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
PINNED='a7921ca2f5c124203be10d3418db70a2e15f3c10'
KNOWN_MISSING={'digitalRead8','digitalWrite8','wiringPiSetupPiFace','wiringPiSetupPiFaceForGpioProg','getResponce'}
FUNCTION_NAME_OVERRIDES={
 'getResponce':'get_response_legacy','W25Q64_fastread':'w25q64_fast_read','W25Q64_readUniqieID':'w25q64_read_unique_id',
 'lcd128x64getScreenSize':'lcd128x64_get_screen_size','DS1302clockRead':'ds1302_clock_read','DS1302clockWrite':'ds1302_clock_write',
 'ds1302clockRead':'ds1302_clock_read','ds1302clockWrite':'ds1302_clock_write',
}
SPECIAL_ADAPTERS={
 'wiringPiISR':'callback_isr','piThreadCreate':'callback_thread','wiringPiSPIDataRW':'spi_inout_buffer',
 'W25Q64_read':'w25_read','W25Q64_fastread':'w25_read','W25Q64_pageWrite':'w25_page_write','W25Q64_readManufacturer':'w25_manufacturer','W25Q64_readUniqieID':'w25_unique_id',
 'serialPrintf':'prepared_printf','lcdPrintf':'prepared_printf','scrollPhatPrintf':'prepared_printf','wiringPiFailure':'prepared_printf',
 'DS1302clockRead':'ds1302_clock_read','DS1302clockWrite':'ds1302_clock_write','ds1302clockRead':'ds1302_clock_read','ds1302clockWrite':'ds1302_clock_write',
 'lcdCharDef':'lcd_char_def','maxDetectRead':'maxdetect_read','rht03Read':'rht03_read','readRHT03':'rht03_read','lcd128x64getScreenSize':'lcd_screen_size',
 'oledReadReg':'oled_read_reg','oledWriteReg':'oled_write_reg','oledWriteData':'oled_write_data','oledOpen':'mutable_c_string','loadWPiExtension':'mutable_c_string',
 'oled_open':'oled_open','oled_send':'oled_send','oled_putstr':'oled_putstr','oled_putstrto':'oled_putstrto',
 'serialRead':'serial_read','serialReadTimeout':'serial_read_timeout','serialWrite':'serial_write','serialWriteTimeout':'serial_write_timeout',
 'serialConfigInit':'serial_config_init','serialGetConfig':'serial_get_config','serialGetBaud':'serial_get_baud','serialGetModemLines':'serial_get_modem_lines',
 'serialGetCounters':'serial_get_counters','serialGetRS485':'serial_get_rs485','serialGetHardwareInfo':'serial_get_hardware_info','serialGetCapabilities':'serial_get_capabilities',
 'serialContextOpen':'serial_context_open','serialContextFromFd':'serial_context_from_fd','serialContextClose':'serial_context_close','serialContextGetFd':'serial_context_get_fd',
 'serialContextRead':'serial_context_read','serialContextWrite':'serial_context_write','serialContextCancelRead':'serial_context_cancel_read','serialContextCancelWrite':'serial_context_cancel_write',
}
OUTPUT_POINTER_FUNCTIONS={'wiringPiVersion','piBoardId','lcd128x64getScreenSize'}

def snake(name:str)->str:
    if name in FUNCTION_NAME_OVERRIDES:return FUNCTION_NAME_OVERRIDES[name]
    name=name.replace('WPi','WPI').replace('wPi','WPI')
    protected={'W25Q64':'Acrtoken0','RS485':'Acrtoken1','I2C':'Acrtoken2','SPI':'Acrtoken3','GPIO':'Acrtoken4','PWM':'Acrtoken5','OLED':'Acrtoken6','WPI':'Acrtoken7'}
    for k,v in protected.items(): name=name.replace(k,v)
    name=re.sub(r'([A-Z]+)([A-Z][a-z])',r'\1_\2',name)
    name=re.sub(r'([a-z0-9])([A-Z])',r'\1_\2',name)
    name=re.sub(r'[-\s]+','_',name).lower()
    for k,v in protected.items(): name=name.replace(v.lower(),k.lower())
    name=re.sub(r'__+','_',name).strip('_')
    return name.replace('w25q64_fastread','w25q64_fast_read').replace('read_uniqie_id','read_unique_id')

def capwords(name:str)->str:
    parts=snake(name).split('_'); acr={'i2c':'I2C','spi':'SPI','gpio':'GPIO','pwm':'PWM','oled':'OLED','w25q64':'W25Q64','wpi':'WPi','rs485':'RS485'}
    return ''.join(acr.get(p,p[:1].upper()+p[1:]) for p in parts if p)

def header_module(header:str)->str:
    return 'wiringop.'+'.'.join(snake(x) for x in Path(header).with_suffix('').parts)

def discover_headers(upstream:Path)->list[str]:
    h=sorted(p.relative_to(upstream).as_posix() for p in upstream.rglob('*.h') if not p.relative_to(upstream).as_posix().startswith('examples/'))
    if len(h)!=54: raise RuntimeError(f'expected 54 public headers, found {len(h)}')
    return h

def direct_decl(node:dict[str,Any],header_abs:Path,tu:Path)->bool:
    loc=node.get('loc') or {}; f=loc.get('file')
    if f and Path(f).resolve()==header_abs.resolve():return True
    inc=(loc.get('includedFrom') or {}).get('file')
    return not f and bool(inc) and Path(inc).resolve()==tu.resolve()

def ast_for_header(upstream:Path,header:str):
    with tempfile.NamedTemporaryFile('w',suffix='.c',delete=False) as f:
        tu=Path(f.name); f.write('#include <stdint.h>\n#include <stddef.h>\n#include <stdbool.h>\n');f.write(f'#include "{(upstream/header).as_posix()}"\n')
    cmd=['clang','-std=gnu11','-D_GNU_SOURCE','-DCONFIG_ORANGEPI',f'-I{upstream}',f'-I{upstream/"wiringPi"}',f'-I{upstream/"devLib"}',f'-I{upstream/"wiringPiD"}','-Xclang','-ast-dump=json','-fsyntax-only',str(tu)]
    try:return json.loads(subprocess.check_output(cmd,text=True,stderr=subprocess.STDOUT)),tu
    except subprocess.CalledProcessError as e:raise RuntimeError(f'clang AST failed for {header}:\n{e.output}')

def return_type(q:str)->str:
    i=q.find('('); return q.strip() if i<0 else q[:i].strip()

def parse_header_ast(upstream:Path,header:str)->dict[str,Any]:
    ast,tu=ast_for_header(upstream,header); habs=upstream/header; top=ast.get('inner',[])
    records={}; entries=[]
    for n in top:
        if not isinstance(n,dict) or not direct_decl(n,habs,tu):continue
        if n.get('kind')=='RecordDecl' and n.get('completeDefinition',True):
            fs=[{'name':x.get('name') or '','c_type':(x.get('type') or {}).get('qualType','')} for x in n.get('inner',[]) if x.get('kind')=='FieldDecl']
            if fs:
                e={'id':n.get('id'),'tag_name':n.get('name') or '','typedef_name':'','fields':fs};records[n.get('id','')]=e;entries.append(e)
    for n in top:
        if not isinstance(n,dict) or not direct_decl(n,habs,tu) or n.get('kind')!='TypedefDecl':continue
        owned=None
        for x in n.get('inner',[]):
            if isinstance(x,dict) and x.get('ownedTagDecl'):owned=x['ownedTagDecl'];break
        rid=(owned or {}).get('id')
        if rid in records:records[rid]['typedef_name']=n.get('name') or ''
    structs=[]
    for r in entries:
        cn=r['typedef_name'] or r['tag_name']
        if not cn:continue
        fs=[]
        for f in r['fields']:
            ct=f['c_type']; pn=snake(f['name']); pointer='*' in ct or '(*)' in ct; arr=re.search(r'\[(\d+)\]$',ct)
            if pointer:pn+='_address'
            fs.append({**f,'python_name':pn,'pointer':pointer,'function_pointer':'(*' in ct,'array_len':int(arr.group(1)) if arr else None})
        structs.append({'c_name':cn,'tag_name':r['tag_name'],'typedef_name':r['typedef_name'],'python_name':capwords(cn),'fields':fs})
    funcs=[];vars=[];enums=[]
    for n in top:
        if not isinstance(n,dict) or not direct_decl(n,habs,tu):continue
        k=n.get('kind')
        if k=='FunctionDecl':
            name=n.get('name');
            if not name:continue
            params=[]
            for i,x in enumerate(n.get('inner',[])):
                if x.get('kind')!='ParmVarDecl':continue
                pn=x.get('name') or f'arg{i}'; params.append({'name':pn,'python_name':snake(pn),'c_type':(x.get('type') or {}).get('qualType','')})
            ad=SPECIAL_ADAPTERS.get(name,'direct')
            if name in KNOWN_MISSING:ad='legacy_typo' if name=='getResponce' else 'missing'
            if name in OUTPUT_POINTER_FUNCTIONS and ad=='direct':ad='output_pointers'
            if ad=='direct':
                outs=[p for p in params if re.fullmatch(r'(?:const\s+)?(?:unsigned\s+)?(?:int|short|long|char)\s*\*',p['c_type'].replace('volatile ','')) and not p['c_type'].lstrip().startswith('const ')]
                if outs:ad='output_pointers'
            funcs.append({'c_name':name,'python_name':snake(name),'return_type':return_type((n.get('type') or {}).get('qualType','')),'parameters':params,'variadic':bool(n.get('variadic')),'adaptation':ad,'known_missing':name in KNOWN_MISSING})
        elif k=='VarDecl':
            name=n.get('name')
            if name:vars.append({'c_name':name,'python_name':snake(name),'c_type':(n.get('type') or {}).get('qualType',''),'storage':n.get('storageClass') or ''})
        elif k=='EnumDecl':
            mem=[{'c_name':x.get('name'),'python_name':snake(x.get('name','')).upper()} for x in n.get('inner',[]) if x.get('kind')=='EnumConstantDecl']
            if mem:
                en=n.get('name') or f'anonymous_enum_{len(enums)}';enums.append({'c_name':en,'python_name':capwords(en),'members':mem})
    tu.unlink(missing_ok=True);return {'functions':funcs,'structs':structs,'variables':vars,'enums':enums}

def physical_macros(text:str):
    logical=[];cur=''
    for line in text.splitlines():
        cur=(cur+'\n'+line) if cur else line
        if re.search(r'\\\s*$',line):continue
        logical.append(cur);cur=''
    if cur:logical.append(cur)
    out={}
    for line in logical:
        m=re.match(r'^\s*#\s*define\s+([A-Za-z_]\w*)(.*)$',line,re.S)
        if not m:continue
        name,tail=m.group(1),m.group(2); fn=tail.startswith('(');args=[];body=tail.strip()
        if fn:
            close=tail.find(')')
            if close>=0:
                a=tail[1:close].strip();args=[] if not a else [x.strip() for x in a.split(',')];body=tail[close+1:].strip()
        out[name]={'c_name':name,'function_like':fn,'args':args,'body':body}
    return out

def active_macro_definitions(upstream:Path,header:str):
    src=f'#include <stdint.h>\n#include <stddef.h>\n#include <stdbool.h>\n#include "{(upstream/header).as_posix()}"\n'
    cmd=['clang','-std=gnu11','-D_GNU_SOURCE','-DCONFIG_ORANGEPI',f'-I{upstream}',f'-I{upstream/"wiringPi"}',f'-I{upstream/"devLib"}',f'-I{upstream/"wiringPiD"}','-dM','-E','-x','c','-']
    txt=subprocess.check_output(cmd,input=src,text=True,stderr=subprocess.DEVNULL);out={}
    for l in txt.splitlines():
        m=re.match(r'#define\s+([A-Za-z_]\w*)(.*)$',l)
        if m:out[m.group(1)]=m.group(2).strip()
    return out

def probe_macros(upstream:Path,header:str,macros):
    if not macros:return set()
    with tempfile.NamedTemporaryFile('w',suffix='.c',delete=False) as f:
        p=Path(f.name);f.write('#include <stdint.h>\n#include <stddef.h>\n#include <stdbool.h>\n');f.write(f'#include "{(upstream/header).as_posix()}"\n')
        for i,m in enumerate(macros,1):
            expr=m['c_name']
            if m['function_like']:expr+=f'({", ".join("1" for _ in m.get("args",[]))})'
            f.write(f'#line {i} "macro_probe"\nstatic __typeof__(({expr})) *macro_probe_{i};\n')
    cmd=['clang','-std=gnu11','-D_GNU_SOURCE','-DCONFIG_ORANGEPI',f'-I{upstream}',f'-I{upstream/"wiringPi"}',f'-I{upstream/"devLib"}',f'-I{upstream/"wiringPiD"}','-fsyntax-only','-ferror-limit=0',str(p)]
    cp=subprocess.run(cmd,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE);bad={int(x) for x in re.findall(r'macro_probe:(\d+):\d+:\s+(?:fatal\s+)?error:',cp.stderr)}
    if cp.returncode and not bad:bad=set(range(1,len(macros)+1))
    p.unlink(missing_ok=True);return {m['c_name'] for i,m in enumerate(macros,1) if i not in bad}

def macros_for_header(upstream:Path,header:str):
    physical=physical_macros((upstream/header).read_text(errors='replace'));active=active_macro_definitions(upstream,header);items=[]
    for name,m in physical.items():
        x=dict(m);x['active']=name in active;x['definition']=active.get(name,m['body']);x['python_name']=snake(name).upper();x['bindable']=False;x['kind']='inactive' if not x['active'] else ('function' if x['function_like'] else 'object');items.append(x)
    bind=probe_macros(upstream,header,[x for x in items if x['active']])
    for x in items:
        x['bindable']=x['c_name'] in bind
        if x['function_like'] and x['bindable']:x['kind']='function_value'
        elif not x['function_like'] and x['bindable']:x['kind']='value'
        elif x['active']:x['kind']='c_only'
    return items

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--upstream',type=Path,default=ROOT/'build/upstream/wiringOP');ap.add_argument('--output',type=Path,default=ROOT/'api_manifest.json');ns=ap.parse_args();up=ns.upstream.resolve();headers=discover_headers(up)
    manifest={'schema':3,'wiringop_commit':PINNED,'overlay_patches':[p.relative_to(ROOT).as_posix() for p in sorted((ROOT/'patches/wiringOP').glob('*.patch'))],'headers':[]}
    totals={'functions':0,'structs':0,'fields':0,'variables':0,'enums':0,'macros':0,'python_value_macros':0,'function_macros':0}
    for i,h in enumerate(headers,1):
        ast=parse_header_ast(up,h);mac=macros_for_header(up,h);entry={'path':h,'python_module':header_module(h),**ast,'macros':mac};manifest['headers'].append(entry)
        totals['functions']+=len(ast['functions']);totals['structs']+=len(ast['structs']);totals['fields']+=sum(len(s['fields']) for s in ast['structs']);totals['variables']+=len(ast['variables']);totals['enums']+=len(ast['enums']);totals['macros']+=len(mac);totals['python_value_macros']+=sum(x['kind']=='value' for x in mac);totals['function_macros']+=sum(x['kind']=='function_value' for x in mac)
        print(f'[{i:02d}/54] {h}: f={len(ast["functions"])} s={len(ast["structs"])} v={len(ast["variables"])} m={len(mac)}')
    manifest['totals']={'headers':len(headers),**totals};ns.output.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n');print(json.dumps(manifest['totals'],indent=2))
if __name__=='__main__':main()
