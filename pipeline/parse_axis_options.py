import re, json
lines=[ln for ln in open('/sessions/eloquent-epic-mendel/mnt/outputs/axis_raw.txt').read().split('\n')
        if 'Permission to download' not in ln and not re.match(r'^\s*June 2026(\s+\d+)?\s*$',ln)]
def norm(s): return re.sub(r'\s+',' ',s).strip()
idxs=[i for i,ln in enumerate(lines) if 'Unit Type:' in ln]
bounds=idxs+[len(lines)]
BULLET='•'
START=re.compile(r'^(Additional|Replace|Upgrade|Add)\b')

def block(idx,nxt,header):
    for j in range(idx,min(nxt,len(lines))):
        if re.match(rf'^\s*{header}\b',lines[j]):
            for k in range(j+1,min(nxt,len(lines))):
                if re.match(r'^\s*(SQUAD UPGRADES|OPTIONS|SPECIAL RULES|RIFT UNIT)\b',lines[k]): return j,k
                if 'REQUISITION POINTS' in lines[k]: return j,k
                st=norm(lines[k])
                if re.match(r"^[A-Z][A-Z0-9 '’/()\.-]{3,}$",st) and len(re.sub(r'[^A-Z]','',st))>=3 and 'LIMIT' not in st and 'POINTS' not in st:
                    return j,k
            return j,min(nxt,len(lines))
    return None

def limit_of(s):
    m=re.search(r'(\d+)\s+per\s+(squad|Officer|unit|model)',s)
    return {'n':int(m.group(1)),'scope':m.group(2)} if m else None

def parse_options(idx,nxt):
    b=block(idx,nxt,'OPTIONS')
    if not b: return []
    s,e=b
    per_model='per model' in lines[s].lower()
    seg=lines[s+1:e]
    opts=[]
    hero_found=re.findall(r'(Guts|Luck|Rift Mastery|Fear)\s+\+(\d+)', '\n'.join(seg))
    if hero_found or any(('Hero stat' in x) or ('The Officer may take' in x) for x in seg):
        seen=set()
        for nm,val in hero_found:
            if nm in seen: continue
            seen.add(nm)
            opts.append({'type':'hero_stat','desc':nm,'cost':int(val),'per_model':False,'limit':{'n':1,'scope':'Officer'}})
    def is_hero(x):
        return ('Hero stat' in x) or ('The Officer may take' in x) or re.search(r'\bGuts\b|\bLuck\b|\bRift Mastery\b',x)
    seg=[x for x in seg if not is_hero(x)]
    # gather quality costs (appear only in additional-models rows)
    qcost={}
    for ln in seg:
        for m in re.finditer(r'(Inexperienced|Regular|Veteran)\s+(\d+)',ln):
            qcost[m.group(1).lower()]=int(m.group(2))
    # keyword-anchored rows (bullet glyph may be detached)
    rows=[]; cur=None
    for raw in seg:
        t=norm(raw.replace(BULLET,' '))
        if not t: continue
        if START.match(t):
            if cur: rows.append(cur)
            cur=t
        elif cur is not None:
            cur=cur+' '+t
    if cur: rows.append(cur)
    for f in rows:
        low=f.lower()
        if f.startswith('Additional'):
            desc=re.split(r'\s+(Inexperienced|Regular|Veteran|No Mixed|\d+\s+per|\(|[+\-–]?\d)',f)[0].strip()
            cost=dict(qcost) if qcost else None
            if not cost:
                m=re.search(r'\b(\d+)\s+\d+\s+per',f) or re.search(r'\b(\d+)\s*$',f)
                if m: cost={'flat':int(m.group(1))}
            opts.append({'type':'add_models','desc':desc,'cost':cost,'per_model':True,
                         'limit':limit_of(f),'quality_locked':True})
        elif re.match(r'(Replace|Upgrade)',f):
            cm=re.search(r'([+\-–]\s?\d+)',f)
            cost=int(cm.group(1).replace('–','-').replace(' ','')) if cm else (0 if 'free' in low else None)
            cond=None
            if 'only if' in low:
                mm=re.search(r'only if[^)]*',low); cond=mm.group(0).strip(') ') if mm else 'conditional'
            elif 'additional soldiers only' in low: cond='additional soldiers only'
            desc=re.sub(r'\s*[+\-–]\s?\d+.*$','',f).strip()
            desc=re.sub(r'\s*\(.*$','',desc).strip()
            opts.append({'type':'weapon_swap','desc':desc,'cost':cost,'per_model':per_model,
                         'limit':limit_of(f),'condition':cond})
        elif f.startswith('Add'):
            cm=re.search(r'([+\-]\d+)',f) or re.search(r'\b(\d+)\b',f)
            cost=int(cm.group(1)) if cm else None
            desc=f[:cm.start()].strip() if cm else f.strip()
            lim=limit_of(f)
            if not lim:
                um=re.search(r'up to (\d+)',f)
                if um: lim={'n':int(um.group(1)),'scope':'vehicle'}
            opts.append({'type':'vehicle_add','desc':desc,'cost':cost,'per_model':False,
                         'limit':lim,'condition':None})
    return opts

def parse_upgrades(idx,nxt):
    b=block(idx,nxt,'SQUAD UPGRADES')
    if not b: return []
    s,e=b; ups=[]
    for ln in lines[s+1:e]:
        if BULLET in ln:
            t=norm(ln.split(BULLET,1)[1])
            m=re.search(r'([+\-]\d+)\s*$',t)
            if m:
                ups.append({'type':'unit_upgrade','desc':re.sub(r'\s*[+\-]\d+\s*$','',t).strip(),
                            'cost':int(m.group(1)),'per_model':True})
    return ups

def model_count(comp):
    if not comp: return 1
    comp=re.split(r'\s+(Inexperienced|Regular|Veteran|REQUISITION|\d+mm)',comp)[0]
    nums=[int(x) for x in re.findall(r'\b(\d+)\b',comp)]
    return sum(nums) if nums else 1

draft=json.load(open('/sessions/eloquent-epic-mendel/mnt/outputs/axis_units_draft.json'))
out=[]
for n,idx in enumerate(idxs):
    nxt=bounds[n+1]
    out.append({'i':n,'options':parse_options(idx,nxt),'upgrades':parse_upgrades(idx,nxt),
                'models':model_count(draft[n]['composition'])})
dn={n:draft[n]['name'] for n in range(len(draft))}
for target in ['RIFLE SQUAD','US HEAVY INFANTRY SQUAD','PARAGON SQUAD','M5A5 JACKAL']:
    for r in out:
        if dn[r['i']] and dn[r['i']].upper().startswith(target):
            print('###',dn[r['i']],'| models=',r['models'])
            for o in r['options']: print('   OPT',json.dumps(o,ensure_ascii=False))
            for o in r['upgrades']: print('   UPG',json.dumps(o,ensure_ascii=False))
            break
json.dump(out,open('/sessions/eloquent-epic-mendel/mnt/outputs/axis_options_draft.json','w'),indent=2,ensure_ascii=False)
print('\nunits with options:',sum(1 for r in out if r['options']),'/',len(out))
