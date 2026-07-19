import json
P='/sessions/intelligent-loving-albattani/mnt/Konflikt47 Army Builder/data/weapons.json'
w=json.load(open(P))
names={p['name'] for p in w['weapon_profiles']}

NEW=[
 # British
 ("PIAT","12\"","1","+5","Team, Shaped Charge",["piat","projector, infantry, anti-tank"]),
 ("Meteor Launcher","60\"","1","HE","Team, Fixed, HE (3\"), Indirect Fire, Rift Weapon, Corrosive (D6)",["meteor launcher"]),
 # Japan Shiboru
 ("Type 99 Shiboru Cannon","48\"","2","+4","Team, Fixed, Rift Weapon; Crush",["type 99 shiboru cannon","type 99 shiboru"]),
 ("Type 61 Light Shiboru Cannon","36\"","2","+3","Team, Fixed, Rift Weapon; Crush",["type 61 light shiboru cannon","type 61 shiboru","light shiboru cannon"]),
 ("Type 10 Shiboru Rifle","24\"","1","+1","Rift Weapon; Crush",["type 10 shiboru rifle","shiboru rifle"]),
 # Soviet Zvukovoy
 ("Zvukovoy Proeyektor","24\"","4","+2","Team, Fixed, Rift Weapon; Shockwave",["zvukovoy proeyektor","zvukovoy projektor"]),
 ("Zvukovoy Avtomat","6\"","3","+1","Assault, Rift Weapon; Shockwave",["zvukovoy avtomat"]),
 # Soviet Pulya modal (Advanced Small Arms) - two firing modes
 ("PTRS-46 Pulya-Poykbi","18\" / 6\"","1 / 2","+2 / –","Two modes: (a) Mode / (b) Mode, Assault",["ptrs-46 pulya-poykbi","pulya-poykbi","pulya"]),
 ("ROKS-6 Plamya-Poykbi","6\" / 6\"","1 / 2","+2 / –","Two modes: (a) Mode, Flamethrower / (b) Mode, Assault",["roks-6 plamya-poykbi","plamya-poykbi","plamya"]),
 ("DPM Pulemet-Poykbi","18\" / 6\"","4 / 2","+1 / –","Two modes: (a) Mode / (b) Mode, Assault",["dpm pulemet-poykbi","pulemet-poykbi","pulemet"]),
]
profiles=[{"name":n,"range":r,"shots":s,"pen":p,"special":sp,"aliases":al} for (n,r,s,p,sp,al) in NEW]
add=[p for p in profiles if p['name'] not in names]
# prepend so specific named weapons match before generics
w['weapon_profiles']=add+w['weapon_profiles']

# RPG-1 / PRIAM share the Panzerfaust profile -> add as aliases
for p in w['weapon_profiles']:
    if p['name']=='Panzerfaust':
        for a in ['rpg-1','priam']:
            if a not in p['aliases']: p['aliases'].append(a)

# new weapon special rules
w.setdefault('weapon_special_rules',{})
w['weapon_special_rules']['Crush']="A unit with Crush weaponry may exhaust a Rift Die when firing (including in Ambush). If the weapon scores hits with all of its shots, it automatically inflicts one additional hit at the same Pen with no to-hit roll. Against a Vehicle hit by all of its shots, add the Pen values together (including the bonus hit) and roll damage as a single hit."
w['weapon_special_rules']['Shockwave']="A unit with Shockwave weaponry may exhaust a Rift Die when firing (including in Ambush) to generate a blast. Roll to hit as normal, then combine the shots that hit into a single hit whose HE-equivalent template size equals the number of hits scored. Shockwave attacks ignore Cover Saves; their Pen equals the template size."

json.dump(w,open(P,'w'),indent=1,ensure_ascii=False)
print('added profiles:',[p['name'] for p in add])
print('total profiles now:',len(w['weapon_profiles']))
print('weapon_special_rules:',list(w['weapon_special_rules'].keys()))
