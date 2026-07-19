import re, json
raw=json.load(open('axis_units_draft.json'))
opts=json.load(open('axis_options_draft.json'))
stats=json.load(open('axis_stats_draft.json'))

def clean_type(t):
    if not t: return t
    t=re.split(r'\s+(Inexperienced|Regular|Veteran|REQUISITION)',t)[0]
    return re.sub(r'\s+',' ',t).strip()
def clean_name(n):
    if not n: return n
    n=re.sub(r'\s+\d+$','',n).strip().replace('–','-')
    n=re.sub(r'\b([IiVvXx]{1,4})\b',lambda m:m.group(1).upper() if re.fullmatch(r'[ivx]+',m.group(1),re.I) else m.group(1),n)
    return n.title2().replace('Us ','US ').replace('Hmg','HMG').replace('Mmg','MMG').replace('Nco','NCO').replace('Sd.Kfz','Sd.Kfz').replace('Mg ','MG ')
def categorize(t):
    t=(t or '').lower()
    if 'company commander' in t: return 'company_commander'
    if 'platoon commander' in t: return 'platoon_commander'
    if 'hero' in t and 'infantry' not in t: return 'hero'
    if 'heroic specialist infantry' in t: return 'infantry_specialist'
    if 'basic infantry' in t: return 'infantry_basic'
    if 'advanced infantry' in t: return 'infantry_advanced'
    if 'specialist infantry' in t: return 'infantry_specialist'
    if 'medic' in t: return 'medic'
    if 'forward observer' in t: return 'forward_observer'
    if 'sniper' in t: return 'sniper_team'
    if 'anti-tank team' in t: return 'anti_tank_team'
    if 'machine gun team' in t: return 'machine_gun_team'
    if 'light mortar' in t: return 'light_mortar_team'
    if 'mortar team' in t: return 'mortar_team'
    if 'flamethrower team' in t: return 'flamethrower_team'
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
    nums=[int(x) for x in re.findall(r'\b(\d+)\b',comp)]
    return sum(nums) if nums else 1

units=[]
for i,u in enumerate(raw):
    ct=clean_type(u['unit_type']); nm=clean_name(u['name'])
    slug=re.sub(r'[^a-z0-9]+','-',(nm or f'unit{i}').lower()).strip('-')
    st=stats[i]
    units.append({'id':f'axis-{slug}','name':nm,'unit_type':ct,'category':categorize(ct),
      'composition':u['composition'],'cost':u['cost'],
      'model_count':model_count(u['composition']),
      'special_rules':[r['name'] for r in st['rules']],
      'rift_dice':u['rift_dice'],'photo':'',
      'options':opts[i]['options'],'upgrades':opts[i]['upgrades'],'stats':st})
json.dump(units,open('axis_units_built.json','w'),indent=1,ensure_ascii=False)
for u in units: print(f"{u['category']:<20} | {u['name']}")
