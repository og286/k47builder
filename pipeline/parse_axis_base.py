import re, json
lines=[ln for ln in open('/sessions/eloquent-epic-mendel/mnt/outputs/axis_raw.txt').read().split('\n')
        if 'Permission to download' not in ln and not re.match(r'^\s*June 2026(\s+\d+)?\s*$',ln)]
def norm(s): return re.sub(r'\s+',' ',s).strip()
idxs=[i for i,ln in enumerate(lines) if 'Unit Type:' in ln]
bounds=idxs+[len(lines)]
SKIP={'SPECIAL RULES','OPTIONS','RIFT UNIT','HERO STATISTICS','ARMY SPECIAL RULES','OFFICERS','COMPANY COMMANDERS','PLATOON COMMANDERS','INFANTRY','MACHINE GUN TEAMS','FLAMETHROWER TEAMS','FIELD ARTILLERY','ANTI-TANK GUNS','SQUAD UPGRADES','ANTI-TANK TEAMS','SNIPER TEAMS','MORTAR TEAMS','ARTILLERY','WALKERS','TANKS','TRANSPORTS','HEROES','SCOUT WALKERS','LIGHT WALKERS','MEDIUM WALKERS'}
def clean_name(s):
    s=re.sub(r'\s*REQUISITION POINTS\s*$','',s,flags=re.I)
    s=re.sub(r'\s*Requisition Points\s*$','',s,flags=re.I)
    return norm(s)
def find_name(idx,prev):
    for j in range(idx, max(idx-40,prev-1),-1):
        s=norm(lines[j])
        if not s or s.startswith('•'): continue
        core=clean_name(s)
        if ':' in core: continue
        if core.upper() in SKIP: continue
        letters=re.sub(r'[^A-Za-z]','',core)
        if not letters: continue
        # accept ALL-CAPS heading (allow digits, parens, hyphen, quotes)
        if core.upper()==core and 2<=len(core)<=70:
            return core
    return None
def field(idx,nxt,*labels):
    for j in range(max(idx-4,0),min(nxt,idx+12)):
        for lab in labels:
            if lab in lines[j]:
                return norm(lines[j].split(lab,1)[1])
    return None
def costs(idx,nxt):
    c={}
    lo=max(idx-6,0); hi=min(nxt,idx+11)
    for j in range(lo,hi):
        for m in re.finditer(r'(Inexperienced|Regular|Veteran):\s*(\d+)',lines[j]):
            c[m.group(1).lower()]=int(m.group(2))
    if c: return c
    # single flat cost near REQUISITION POINTS
    for j in range(max(idx-5,0),min(nxt,idx+6)):
        if 'REQUISITION POINTS' in lines[j]:
            for k in range(j,min(j+5,nxt)):
                m=re.search(r'\b(\d{2,3})\s*$',lines[k])
                if m and (any(x in lines[k] for x in('Composition','Unit Type','Base Size')) or norm(re.sub(r'\d+\s*$','',lines[k]))==''):
                    return {'fixed':int(m.group(1))}
    return {}
def special(idx,nxt):
    r=[]
    for j in range(idx,min(nxt,idx+45)):
        if norm(lines[j])=='SPECIAL RULES':
            for k in range(j+1,min(nxt,j+14)):
                s=norm(lines[k])
                if s.startswith('•'):
                    nm=re.split(r'[–\-(:]',s[1:])[0].strip()
                    if nm: r.append(nm)
                elif s=='' : continue
                elif s.upper()==s and len(s)>3: break
            break
    return r
def rift(idx,nxt):
    for j in range(idx,min(nxt,idx+55)):
        if norm(lines[j])=='RIFT UNIT':
            for k in range(j,min(nxt,j+4)):
                m=re.search(r'Rift Dice:\s*(\d+)',lines[k])
                if m: return int(m.group(1))
            return 1
    return 0
units=[]
for n,idx in enumerate(idxs):
    nxt=bounds[n+1]; prev=bounds[n-1] if n>0 else 0
    units.append({'name':find_name(idx,prev),'unit_type':field(idx,nxt,'Unit Type:'),
      'composition':field(idx,nxt,'Unit Composition:','Team Composition:'),
      'cost':costs(idx,nxt),'special_rules':special(idx,nxt),'rift_dice':rift(idx,nxt)})
for u in units:
    print(f"{str(u['cost']):<48} | {str(u['unit_type']):<40} | {u['name']}")
print("TOTAL:",len(units))
json.dump(units,open('/sessions/eloquent-epic-mendel/mnt/outputs/axis_units_draft.json','w'),indent=2)
