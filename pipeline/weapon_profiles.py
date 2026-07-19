import json,re
# canonical profiles from Core Rulebook weapons charts (2025). aliases matched case-insensitively.
# order matters: most specific first so 'light anti-tank gun' beats 'anti-tank gun'.
P=[
 # --- Rift (specific tesla names first) ---
 ("M177 Dual Tesla Cannon","48\"","2","+2..+3","Team, Fixed, Rift Weapon; Tesla Arc (1)",["m177 dual tesla cannon","m177"]),
 ("M21 Light Tesla Cannon","30\"","1","+1","Team, Fixed, Rift Weapon; Tesla Arc (3)",["m21 light tesla cannon","m21 tesla","m21"]),
 ("M17 Tesla Cannon","36\"","1","+2","Team, Fixed, Rift Weapon; Tesla Arc (3)",["m17 tesla cannon","m17 tesla"]),
 ("Heavy Tesla Rifle","18\" / 6\"","1 / 3","+1","Two modes: Charge (Team, Tesla Arc 1) / Rapid (Assault)",["heavy tesla rifle"]),
 ("Tesla Gauntlet","Close Quarters","—","+2","Rift Weapon; Tesla Arc (1) (close combat)",["tesla gauntlet"]),
 # --- Heavy weapons ---
 ("Super-heavy Anti-tank Gun","84\"","1","+7","Team, Fixed, Anti-Tank Gun, HE (3\")",["super-heavy anti-tank gun","super heavy anti-tank gun","super-heavy at gun"]),
 ("Heavy Anti-tank Gun","72\"","1","+6","Team, Fixed, Anti-Tank Gun, HE (2\")",["heavy anti-tank gun","heavy at gun"]),
 ("Medium Anti-tank Gun","60\"","1","+5","Team, Fixed, Anti-Tank Gun, HE (1\")",["medium anti-tank gun","medium at gun"]),
 ("Light Anti-tank Gun","48\"","1","+4","Team, Fixed, Anti-Tank Gun, HE (1\")",["light anti-tank gun","light at gun"]),
 ("Heavy Automatic Cannon","72\"","2","+3","Team, Fixed, HE (1\")",["heavy automatic cannon"]),
 ("Light Automatic Cannon","48\"","2","+2","Team, Fixed, HE (1\")",["light automatic cannon","automatic cannon"]),
 ("Heavy Machine Gun (HMG)","48\"","6*","+1","Team, Fixed (*Shots halved on a Vehicle)",["heavy machine gun","hmg"]),
 ("Medium Machine Gun (MMG)","36\"","6*","–","Team, Fixed (*Shots halved on a Vehicle)",["medium machine gun","mmg"]),
 ("Flamethrower (Vehicle)","12\"","1","+2","Flamethrower",["flamethrower (vehicle)","vehicle flamethrower"]),
 # --- Infantry anti-armour ---
 ("Super Bazooka","24\"","1","+6","Team, Shaped Charge",["super bazooka","panzerschreck"]),
 ("Bazooka","24\"","1","+5","Team, Shaped Charge",["bazooka"]),
 ("Anti-tank Rifle","48\"","1","+2","Team",["anti-tank rifle","anti tank rifle"]),
 ("AT Rifle Grenade","12\"","1","+3","Shaped Charge",["at rifle grenade","anti-tank rifle grenade"]),
 ("ATRD (Anti-tank Rocket Device)","12\"","1","+6","Anti-tank Launchers, Shaped Charge",["atrd"]),
 # --- HE weapons ---
 ("Heavy Mortar","12-72\"","1","HE","Team, Fixed, Indirect Fire, HE (3\")",["heavy mortar"]),
 ("Medium Mortar","12-60\"","1","HE","Team, Fixed, Indirect Fire, HE (2\")",["medium mortar"]),
 ("Light Mortar","12-36\"","1","HE","Team, Indirect Fire, HE (1\")",["light mortar"]),
 ("Heavy Howitzer","72\" (42-84\")","1","HE","Team, Fixed, Howitzer, HE (4\")",["heavy howitzer"]),
 ("Medium Howitzer","60\" (36-72\")","1","HE","Team, Fixed, Howitzer, HE (3\")",["medium howitzer"]),
 ("Light Howitzer","48\" (30-60\")","1","HE","Team, Fixed, Howitzer, HE (2\")",["light howitzer"]),
 ("Medium Rocket System","24\"","1","HE","Team, Fixed, HE (3\")",["medium rocket system"]),
 ("Rifle Grenade","6-18\"","1","HE","Indirect Fire, HE (1\")",["rifle grenade"]),
 ("Grenade Launcher","6-18\" / 12\"","1","HE / +3","Fires Rifle Grenades & AT Rifle Grenades",["grenade launcher"]),
 # --- Advanced / small arms named ---
 ("Thompson M1X1/2","12\" / 6\"","2 / 1","+1 / +2","Two modes: Normal (Assault) / E-Slug",["thompson m1x1/2","thompson m1x1","m1x1"]),
 ("Assault Rifle","18\"","2","–","Assault",["assault rifle"]),
 ("Automatic Rifle","30\"","2","–","–",["automatic rifle"]),
 ("Light Machine Gun (LMG)","36\"","4*","–","Team (*Shots halved on a Vehicle)",["lmg","light machine gun"]),
 ("Infantry Flamethrower","6\"","1","+2","Team, Flamethrower",["infantry flamethrower","flamethrower (infantry)","flamethrower"]),
 ("Submachine Gun (SMG)","12\"","2","–","Assault",["smg","submachine gun","thompson"]),
 ("Rifle","24\"","1","–","–",["rifle"]),
 ("Pistol","6\"","1","–","–",["pistol"]),
]
profiles=[{"name":n,"range":r,"shots":s,"pen":p,"special":sp,"aliases":al} for (n,r,s,p,sp,al) in P]
json.dump(profiles,open('weapon_profiles.json','w'),indent=1,ensure_ascii=False)
print("profiles:",len(profiles))
