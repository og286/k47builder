import re, json, sys
FID=sys.argv[1]; BASE='/sessions/intelligent-loving-albattani/mnt/outputs'
raw=json.load(open(f'{BASE}/{FID}_units_draft.json'))
opts=json.load(open(f'{BASE}/{FID}_options_draft.json'))
stats=json.load(open(f'{BASE}/{FID}_stats_draft.json'))

def clean_type(t):
    if not t: return t
    t=re.split(r'\s+(Inexperienced|Regular|Veteran|REQUISITION)',t)[0]
    return re.sub(r'\s+',' ',t).strip()

KEEP_UPPER={'MMG','HMG','LMG','HQ','US','USA','NCO','SMG','AT','PIAT','ZP','DM','GAZ','KV','RPG',
            'SPG','MK','SS','AA','B','T','QLT','KE','HO','II','KAI','PRIAM','ITA','UK'}
ROMAN=re.compile(r'^[IVXLC]+[A-C]?$')
def cap_word(p):
    up=p.upper()
    if not re.search(r'[A-Za-z]',p): return p
    if up in KEEP_UPPER or ROMAN.fullmatch(up): return up
    if re.search(r'\d',p): return up          # model codes: T-34/ZP, 501/1
    if '.' in p and p.count('.')>=1 and len(p)<=8: return p  # keep dotted abbrevs e.g. Sd.Kfz.
    m=re.search(r'[A-Za-z]',p)               # capitalise first LETTER (skip leading quotes)
    i=m.start()
    return p[:i]+p[i].upper()+p[i+1:].lower()
def clean_name(n):
    if not n: return n
    n=re.sub(r'\s+\d+$','',n).strip().replace('–','-')
    words=[]
    for w in n.split(' '):
        words.append('-'.join(cap_word(p) for p in w.split('-')))
    s=' '.join(words)
    s=re.sub(r'\bMk\b','Mk',s)
    return s

def categorize(t):
    t=(t or '').lower()
    if 'company commander' in t: return 'company_commander'
    if 'platoon commander' in t: return 'platoon_commander'
    if 'hero' in t and 'infantry' not in t: return 'hero'
    if 'heroic specialist infantry' in t: return 'infantry_specialist'
    if 'basic infantry' in t: return 'infantry_basic'
    if 'advanced infantry' in t: return 'infantry_advanced'
    if 'specialist infantry' in t: return 'infantry_specialist'
    if 'inspirational officer' in t: return 'platoon_commander'
    if 'commissar' in t: return 'platoon_commander'
    if 'medic' in t: return 'medic'
    if 'forward observer' in t: return 'forward_observer'
    if 'sniper' in t: return 'sniper_team'
    if 'anti-tank team' in t: return 'anti_tank_team'
    if 'machine gun team' in t: return 'machine_gun_team'
    if 'light mortar' in t: return 'light_mortar_team'
    if 'mortar team' in t: return 'mortar_team'
    if 'flamethrower' in t: return 'flamethrower_team'
    if 'field artillery' in t: return 'field_artillery'
    if 'anti-tank gun' in t: return 'anti_tank_gun'
    if 'walker' in t: return 'armoured_walker'
    if 'tank destroyer' in t: return 'tank_destroyer'
    if 'emplacement' in t or 'tank' in t: return 'tank'
    if 'armoured car' in t: return 'armoured_car'
    if 'assault gun' in t: return 'assault_gun'
    if 'transport' in t: return 'transport'
    return 'other'

def model_count(comp):
    if not comp: return 1
    comp=re.split(r'\s+(Inexperienced|Regular|Veteran|REQUISITION|\d+mm)',comp)[0]
    comp=re.sub(r'\b(Grade|Mark)\s+\d+\b','',comp,flags=re.I)
    nums=[int(x) for x in re.findall(r'\b(\d+)\b',comp)]
    n=sum(nums) if nums else 1
    return n if n<=15 else 1

def split_long(rules):
    out=[]
    for r in rules:
        nm=r.get('name',''); tx=r.get('text','')
        m=re.match(r'^([^(]{2,40})\s*\((.+)\)\s*$',nm)
        if (len(nm)>40 or ':' in nm) and m and not tx:
            out.append({'name':m.group(1).strip(),'text':m.group(2).strip()})
        else:
            out.append(r)
    return out

def split_merged(rules):
    # recover a rule whose detached bullet glued its "Name - text" onto the prior rule's text
    out=[]
    for r in rules:
        nm=r.get('name',''); tx=r.get('text','')
        m=re.match(r"^([A-Z][A-Za-z' ?]{2,38})\s[–-]\s(.+)$",tx)
        if m:
            out.append({'name':nm,'text':''})
            out.append({'name':m.group(1).strip(),'text':m.group(2).strip()})
        else:
            out.append(r)
    return out

def clean_weapons(ws, cost):
    fixed=cost.get('fixed')
    out=[]
    for w in ws:
        w=w.strip()
        if fixed: w=re.sub(rf'\s+{fixed}$','',w).strip()   # strip appended fixed cost
        out.append(w)
    merged=[]
    for w in out:                                          # rejoin wrapped parenthetical notes
        if merged and merged[-1].count('(')>merged[-1].count(')'):
            merged[-1]=(merged[-1]+' '+w).strip(); continue
        merged.append(w)
    return [w for w in merged if re.search(r'[A-Za-z]',w) and not w[:1].islower()]

units=[]
for i,u in enumerate(raw):
    ct=clean_type(u['unit_type']); nm=clean_name(u['name'])
    slug=re.sub(r'[^a-z0-9]+','-',(nm or f'unit{i}').lower()).strip('-')
    st=stats[i]
    st['weapons']=clean_weapons(st.get('weapons',[]),u['cost'])
    st['rules']=split_merged(split_long(st['rules']))
    units.append({'id':f'{FID}-{slug}','name':nm,'unit_type':ct,'category':categorize(ct),
      'composition':u['composition'],'cost':u['cost'],
      'model_count':model_count(u['composition']),
      'special_rules':[r['name'] for r in st['rules']],
      'rift_dice':u['rift_dice'],'photo':'',
      'options':opts[i]['options'],'upgrades':opts[i]['upgrades'],'stats':st})
json.dump(units,open(f'{BASE}/{FID}_units_built.json','w'),indent=1,ensure_ascii=False)
for u in units: print(f"{u['category']:<20} | mc={u['model_count']:<2} | {u['name']}")
print('TOTAL',len(units))
