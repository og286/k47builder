import json
BASE='/sessions/intelligent-loving-albattani/mnt/outputs'
DEST='/sessions/intelligent-loving-albattani/mnt/Konflikt47 Army Builder/data/factions'

ARMY_RULES={
 'british':[
  {'name':'Computational Systems','text':"British Commonwealth units with this special rule ignore the –1 'to hit' penalty for moving and shooting. Units must have this special rule indicated in their Unit Profile to benefit from it."},
  {'name':'Automated Recovery','text':"When rolling on the Vehicle Damage tables against British Commonwealth Vehicles that are Rift Units, ignore Crew Stunned results. The damage has no effect other than the normal Pin Marker(s) inflicted for being successfully hit by a ranged weapon."},
  {'name':'Keep Calm Lads','text':"Each time a British Infantry unit on a Down Order receives a Pin Marker, roll a D6. On the roll of a 4+, immediately discard it. If it would receive multiple Pin Markers at once, roll for each separately."},
  {'name':'Superior Codebreaking','text':"Once per game, at the start of any Game Turn, a British Commonwealth player may choose a Die to draw from the Dice bag, rather than draw randomly. If the Order is issued to an Officer or a Command Vehicle, it may not be used to initiate a Snap to Action! ability. If there is more than one British Commonwealth player, and they decide to use this ability at the same time, roll off. The winner may make use of this ability; the loser must wait for a future turn."},
 ],
 'japan':[
  {'name':'Death Before Dishonour','text':"All Empire of Japan Infantry and Artillery units have the Fanatics special rule, and automatically pass Morale Checks for being assaulted by enemy Vehicles. Furthermore, Empire of Japan units may re-roll failed Order Tests when attempting to Assault."},
  {'name':'From Nowhere','text':"Empire of Japan Infantry units on Ambush may Ambush Charge enemies that move within 12\", rather than the usual 6\". This still counts as a Surprise Charge. If the Ambush Charge goes over Rough Ground or Obstacles, or the ambushing unit begins in Rough Ground, the Ambush Charge distance is reduced to the Advance rate of the assaulting unit."},
  {'name':'Shadow Work','text':"If deemed to be in Cover from enemy shooting, Empire of Japan units on Ambush Orders improve their Cover Save by +1."},
  {'name':'Secrets of Iwo Jima','text':"Empire of Japan Rift units attempting an Outflanking Manoeuvre may be ordered onto the table from Turn 2 onwards, rather than from Turn 3 onwards, entering the table from any point on the owning player's DZE or the left/right edge of the table (as written down during deployment). Furthermore, Japanese Rift units attempting an Outflanking Manoeuvre do not suffer the -1 modifier to the Order Test for moving onto the table from Reserve."},
 ],
 'soviet':[
  {'name':'Harmonic Resonance','text':"At the start of every Game Turn roll a D6 for each enemy unit on the table that does not have the Fearless special rule. On a 5+, that unit immediately receives a Pin Marker."},
  {'name':'Za Stalina','text':"Whenever a Soviet Bloc Infantry or Artillery unit fails a Morale Check and would be destroyed as a result, re-roll it and apply the second result instead. If a test is passed in this way, that unit is immediately up-rated to the next Quality level for the rest of the game. If the unit was already Veteran, it gains +1 Morale Value instead."},
  {'name':'Heroes of the Soviet Bloc','text':"At the start of the game, before deployment, one non-Hero, non-Rift Infantry unit in a Soviet Bloc force may be designated 'Heroes of the Soviet Bloc'. The chosen unit immediately gains a point of Guts – any model in the unit may spend it as if they were a Hero. Furthermore, friendly units within 6\" of the Heroes of the Soviet Bloc unit gain the Fanatics special rule."},
  {'name':'Stolen Rift-Tech','text':"Once per Game, when a Soviet Bloc Rift Die is drawn randomly from the Dice Bag, rolled and assigned to a Soviet Bloc Rift unit, its owning player may swap the result with that of another Rift Die assigned to another unit within 6\", friend or foe. For example, if it rolled an Exhausted result and an enemy unit within 6\" had an Active Rift Die, you may change the Soviet Rift Die to Active and the enemy's Rift Die to Exhausted."},
 ],
}

NAMES={'british':'British Commonwealth','japan':'Empire of Japan','soviet':'Soviet'}

# British special platoon (only faction of the three with one)
BRITISH_PLATOON={
 'id':'automated-infantry','name':'Automated Infantry Platoon','faction':'british',
 'counts_as_assault':True,
 'notes':[
   "The range of the Data Transmission rule on Mk IIC Automated Directors and Mk II Heavy Automated Infantry units is extended to 12\".",
   "Mk II Heavy Automated Infantry units in this Platoon may use the Snap to Action! ability as if they were Officers, but may only issue one Order. This must be to a unit within 6\" in the same Platoon that ordinarily has the First Off the Line special rule. This rule may not be used in conjunction with Superior Codebreaking.",
 ],
 'slots':[
   {'role':'Mk IIC Automated Director','min':1,'max':1,'match':'name','names':['MK IIC Automated Director']},
   {'role':'Mk I Automated Infantry Squads','min':2,'max':2,'match':'name','names':['MK I Automated Infantry']},
   {'role':'Mk II Heavy Automated Infantry Squad','min':1,'max':1,'match':'name','names':['MK II Heavy Automated Infantry']},
   {'role':'Mk I Automated Infantry Squads','min':0,'max':2,'match':'name','names':['MK I Automated Infantry']},
   {'role':'Mk II Heavy Automated Infantry Squad','min':0,'max':1,'match':'name','names':['MK II Heavy Automated Infantry']},
   {'role':"Automated Mobile Platforms 'Hunter'",'min':0,'max':3,'match':'name','names':['Automated Mobile Platform ‘Hunter’']},
   {'role':"Automated Mobile Platforms 'Bombardier'",'min':0,'max':3,'match':'name','names':['Automated Mobile Platform ‘Bombardier’']},
   {'role':"Automated Mobile Platforms 'Lancer'",'min':0,'max':3,'match':'name','names':['Automated Mobile Platform ‘Lancer’']},
   {'role':'Automated Carriers','min':0,'max':3,'match':'name','names':['Automated Carrier']},
   {'role':"'B for Bertie' – Automated Infantry Hero",'min':0,'max':1,'match':'name','names':["'B For Bertie' - Automated Infantry Hero"]},
 ],
}

for fid in ['british','japan','soviet']:
    units=json.load(open(f'{BASE}/{fid}_units_built.json'))
    fac={'id':fid,'name':NAMES[fid],
         'army_special_rules':ARMY_RULES[fid],
         'special_platoons':[BRITISH_PLATOON] if fid=='british' else [],
         'company_commander_allowed':1,
         'units':units}
    json.dump(fac,open(f'{DEST}/{fid}.json','w'),indent=1,ensure_ascii=False)
    print(fid,'->',len(units),'units,',len(ARMY_RULES[fid]),'army rules,',
          len(fac['special_platoons']),'special platoons')
