import re, json, sys
FID=sys.argv[1]; BASE='/sessions/intelligent-loving-albattani/mnt/outputs'
lines=[ln for ln in open(f'{BASE}/{FID}_raw.txt').read().split('\n')
        if 'Permission to download' not in ln and not re.match(r'^\s*June 2026(\s+\d+)?\s*$',ln)]
def norm(s): return re.sub(r'\s+',' ',s).strip()
idxs=[i for i,ln in enumerate(lines) if 'Unit Type:' in ln]
bounds=idxs+[len(lines)]
draft=json.load(open(f'{BASE}/{FID}_units_draft.json'))

FIELDLABELS=['Unit Composition:','Team Composition:','Unit Type:','Base Size:','Standard Weapons:',
 'Standard Weapon:','Movement Rate:','Quality:','Damage Value:','Morale Value:']
def stop_line(s):
    return any(l in s for l in FIELDLABELS) or re.match(r'^\s*(SQUAD UPGRADES|TEAM UPGRADES|OPTIONS|SPECIAL RULES|RIFT UNIT)\b',s) or 'REQUISITION POINTS' in s
def strip_cost(s):
    return re.sub(r'\s*(Inexperienced|Regular|Veteran):\s*\d+.*$','',s).strip()
MEAS=r'(?:Rotate|N/?A|Up to \d+["”]|\d+["”]\s*[–-]\s*\d+["”]|\d+["”])'
HEROSTAT=re.compile(r'\b(Guts|Luck|Rift Mastery)\b\s*:?\s*\d+',re.I)

def blk(n): return idxs[n]-4, bounds[n+1]
def field_after(lo,hi,label):
    for j in range(lo,hi):
        if label in lines[j]: return strip_cost(lines[j].split(label,1)[1]),j
    return None,None
def parse_weapons(lo,hi):
    lbl='Standard Weapons:' if any('Standard Weapons:' in lines[j] for j in range(lo,hi)) else 'Standard Weapon:'
    txt,j=field_after(lo,hi,lbl)
    if j is None: return []
    out=[]; first=strip_cost(txt)
    if first: out.append(first)
    k=j+1
    while k<hi:
        s=lines[k]
        if stop_line(s) or norm(s)=='': break
        out.append(strip_cost(norm(s))); k+=1
    return [o for o in out if o and 'Advance' not in o and o!='Run']
def parse_movement(lo,hi):
    ms=None
    for j in range(lo,hi):
        if 'Movement Rate:' in lines[j]: ms=j; break
    if ms is None: return []
    me=hi
    for j in range(ms,hi):
        if 'Quality:' in lines[j] or 'Damage Value:' in lines[j]: me=j; break
    rows=[]
    for j in range(ms,me):
        s=lines[j]; meas=re.findall(MEAS,s)
        if len(meas)>=1 and ('Advance' not in s or len(meas)>=2):
            label=s
            for lab in ['Movement Rate:','Advance','Run']: label=label.replace(lab,' ')
            label=norm(re.sub(MEAS,' ',label)).strip(': ')
            rows.append({'label':label,'adv':meas[0],'run':meas[1] if len(meas)>1 else 'N/A'})
    return rows
def tiers_for(cost):
    if 'fixed' in cost: return ['fixed']
    return [q for q in ['inexperienced','regular','veteran'] if q in cost]
def parse_vals(lo,hi,label,pat,tiers):
    txt,j=field_after(lo,hi,label)
    if j is None: return None
    toks=re.findall(pat,lines[j])
    if not toks: return None
    if len(toks)==len(tiers): return {t:toks[i] for i,t in enumerate(tiers)}
    if len(toks)==1: return {'all':toks[0]}
    return {'list':toks}
def _isherostatline(s):
    return re.match(r'^\s*(Guts|Luck|Rift Mastery)\b\s*:?\s*\d',norm(s),re.I) is not None
def parse_special(lo,hi):
    out=[]
    for j in range(lo,hi):
        if re.match(r'^\s*SPECIAL RULES\b',lines[j]):
            k=j+1
            while k<hi:
                s=lines[k]
                if re.match(r'^\s*(RIFT UNIT|OPTIONS|SQUAD UPGRADES|TEAM UPGRADES)\b',s) or 'REQUISITION' in s: break
                if '•' in s:
                    t=norm(s.split('•',1)[1])
                    m=re.split(r'\s+[–-]\s+',t,1)
                    name=m[0].strip(); desc=m[1].strip() if len(m)>1 else ''
                    name=HEROSTAT.sub('',name).replace('HERO STATISTICS','').strip()
                    kk=k+1
                    while (kk<hi and '•' not in lines[kk] and norm(lines[kk])!='' and
                           not re.match(r'^\s*(RIFT UNIT|OPTIONS|SQUAD UPGRADES|TEAM UPGRADES)\b',lines[kk]) and
                           'REQUISITION' not in lines[kk] and not _isherostatline(lines[kk])):
                        desc=(desc+' '+norm(lines[kk])).strip(); kk+=1
                    if name: out.append({'name':name,'text':HEROSTAT.sub('',desc).strip()})
                    k=kk; continue
                k+=1
            break
    return out
def parse_hero_stats(lo,hi):
    hs={}
    for j in range(lo,hi):
        if re.match(r'^\s*SPECIAL RULES\b',lines[j]):
            for k in range(j,hi):
                if re.match(r'^\s*(RIFT UNIT|OPTIONS|SQUAD UPGRADES|TEAM UPGRADES)\b',lines[k]) or 'REQUISITION' in lines[k]: break
                for m in re.finditer(r'(Guts|Luck|Rift Mastery):\s*(\d+)',lines[k]): hs[m.group(1)]=int(m.group(2))
            break
    return hs
def parse_rift(lo,hi):
    for j in range(lo,hi):
        if re.match(r'^\s*RIFT UNIT\b',lines[j]):
            end=hi
            for k in range(j+1,hi):
                if re.match(r'^\s*(OPTIONS|SQUAD UPGRADES|TEAM UPGRADES|SPECIAL RULES)\b',lines[k]) or 'REQUISITION' in lines[k]: end=k;break
                stx=norm(lines[k])
                if stx and stx.upper()==stx and len(re.sub(r'[^A-Z]','',stx))>=4 and 'RIFT' not in stx: end=k;break
            seg=lines[j+1:end]
            def grab(label,nextlabels):
                buf=[];cap=False
                for s in seg:
                    if label in s: cap=True; buf.append(norm(s.split(label,1)[1])); continue
                    if cap:
                        if any(nl in s for nl in nextlabels) or '•' in s: break
                        if norm(s)=='': continue
                        buf.append(norm(s))
                return norm(' '.join(buf)).strip()
            dice=None
            for s in seg:
                m=re.search(r'Rift Dice:\s*(\d+)',s)
                if m: dice=int(m.group(1))
            note=''
            mnote=re.search(r'RIFT UNIT\s*\(([^)]*)\)',lines[j])
            if mnote: note=mnote.group(1).strip().title()
            enh=''
            for ii,s in enumerate(seg):
                if 'Active Rift' in s:
                    parts=[re.sub(r'.*Active Rift','',s)]
                    for s2 in seg[ii+1:]:
                        if '•' in s2 or 'Surging Bonus' in s2 or 'Exhausted Penalty' in s2: break
                        parts.append(s2)
                    enh=norm(re.sub(r'Enhancements?:','',' '.join(parts))); break
            surg=grab('Surging Bonus:',['Exhausted'])
            exh=grab('Exhausted Penalty:',['XXXX'])
            return {'dice':dice,'enhancement':enh,'surging':surg,'exhausted':exh,'note':note}
    return None

stats=[]
for n,idx in enumerate(idxs):
    lo,hi=blk(n); cost=draft[n]['cost']; tiers=tiers_for(cost)
    base,_=field_after(lo,hi,'Base Size:')
    stats.append({
      'base_size':base,'weapons':parse_weapons(lo,hi),'movement':parse_movement(lo,hi),
      'quality':tiers,'damage':parse_vals(lo,hi,'Damage Value:',r'\d+\+',tiers),
      'morale':parse_vals(lo,hi,'Morale Value:',r'\b\d+\b',tiers),
      'rules':parse_special(lo,hi),'rift':parse_rift(lo,hi),'hero_stats':parse_hero_stats(lo,hi),
    })
json.dump(stats,open(f'{BASE}/{FID}_stats_draft.json','w'),indent=2,ensure_ascii=False)
print(FID,'stats parsed:',len(stats))
