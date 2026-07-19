import json
P='/sessions/intelligent-loving-albattani/mnt/Konflikt47 Army Builder/data/rules.json'
r=json.load(open(P))
usr=r.setdefault('unit_special_rules',{})

NEW={
 'Augmented':"Augmented units wield heavy weapons as easily as infantry weapons: they ignore the Fixed and Team Weapon special rules for the weapons they carry.",
 'Computational Systems':"British Commonwealth units with this rule ignore the –1 'to hit' penalty for moving and shooting. A unit must have this rule listed in its profile to benefit.",
 'Deadly':"Deadly (X) models roll X dice each to damage in Close Quarters combat. If a Deadly unit wins an Assault and damages an Armoured Vehicle, resolve it as a weapon of Pen +1 or more; Assault weapons add a further die.",
 'Fearless':"Fearless units can never be Pinned and automatically pass any Morale Check, and ignore Tank Fear when assaulting fully-enclosed Armoured Vehicles. If defeated in Close Quarters with models remaining, treat the result as a draw and fight another round.",
 'Fieldcraft':"These units treat Rough Ground as Open Ground, including when Assaulting through it (negating the defender's Defensive Position bonus).",
 'Flak':"Enemies with the Flak special rule automatically fire at an attacking aircraft whose token or model lies within their range and arc of fire, potentially stopping the Air Strike before it resolves.",
 'Hard to Kill':"Hard to Kill units add +2 to their Cover Save rolls and get a 5+ 'Hard to Kill' save against damage in the open or in Close Quarters. They gain no extra Cover bonus for Down Orders but still halve HE hits against them.",
 'Horror':"Enemy units must pass a Morale Check in order to react by shooting at an assaulting unit that has the Horror special rule.",
 'Large':"Large models are physically bulky and each occupies the equivalent of two spaces (rather than one) when carried in a Transport Vehicle.",
 'Medic':"Infantry and Artillery units within 6\" of a friendly Medic have a chance to ignore a casualty, as the medic tends the wounded (see rulebook p.95).",
 'Multi-legged':"Walkers with four or more legs are Multi-legged, allowing them to Reverse at full speed rather than half speed.",
 'Multi-Legged':"Walkers with four or more legs are Multi-legged, allowing them to Reverse at full speed rather than half speed.",
 'Reinforced Front Armour':"Against all shots hitting the Front arc, count the Vehicle's Damage Value as 1 higher than its Army List entry.",
 'Slow':"A Slow Vehicle has a basic move rate of 6\" on an Advance Order and 12\" on a Run Order, keeping pace with accompanying Infantry.",
 'Sniper':"The unit's leader carries a scoped Sniper Rifle: +1 to hit, +1 Pen and no Cover Save allowed vs Infantry/Artillery, and on a hit the firer may pick the enemy Squad Leader, NCO, Officer, Medic or Observer as the casualty. A target within 12\" is missed automatically.",
 'Turn on the Spot':"These small, agile Vehicles can reverse at full speed when executing a Run Order and finish the move facing the direction of travel.",
 'Wide Formation':"Typically larger or bulkier models: this unit may spread out with up to 2\" between models (instead of the usual 1\"), where noted in its Army List entry.",
 'Armoured All Round':"No additional Penetration modifiers for shooting at the Sides, Rear, or from above apply against a Vehicle with Armoured All Round.",
}
added=[]
for k,v in NEW.items():
    if k not in usr:
        usr[k]=v; added.append(k)
json.dump(r,open(P,'w'),indent=1,ensure_ascii=False)
print('added unit_special_rules:',added)
print('total now:',len(usr))
