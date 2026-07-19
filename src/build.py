#!/usr/bin/env python3
"""Assemble modular data + template into the single-file index.html.

Source of truth:
  data/weapons.json         -> shared weapon profiles (all factions)
  data/rules.json           -> meta + core platoon selectors (shared)
  data/factions/<f>.json    -> one file per faction (units, special platoons)
  src/app_template.html     -> the UI/logic template (contains /*__DATA__*/ {})

To add a faction: drop a new data/factions/<name>.json and re-run this script.
Output: index.html  (self-contained; open in any browser)
"""
import json, glob, os

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load(p): return json.load(open(os.path.join(ROOT,p),encoding='utf-8'))

rules=load('data/rules.json')
weapons=load('data/weapons.json')
faction_files=sorted(glob.glob(os.path.join(ROOT,'data/factions/*.json')))
factions=[json.load(open(f,encoding='utf-8')) for f in faction_files]

DATA={
  'meta':rules['meta'],
  'core_platoons':rules['core_platoons'],
  'weapon_profiles':weapons['weapon_profiles'],
  'weapon_special_rules':weapons.get('weapon_special_rules',{}),
  'unit_special_rules':rules.get('unit_special_rules',{}),
  'factions':factions,
}

tpl=open(os.path.join(ROOT,'src/app_template.html'),encoding='utf-8').read()
token='/*__DATA__*/ {}'
assert token in tpl, 'template data token not found'
out=tpl.replace(token, json.dumps(DATA,ensure_ascii=False))
open(os.path.join(ROOT,'index.html'),'w',encoding='utf-8').write(out)

print(f"Built index.html  ({len(out):,} bytes)")
print(f"  factions: {', '.join(f['name'] for f in factions)}")
print(f"  weapons:  {len(weapons['weapon_profiles'])} profiles")
print(f"  platoons: {len(rules['core_platoons'])} core selectors")
