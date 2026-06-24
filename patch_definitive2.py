with open('/Users/nicolelloyd/Projects/workout/workout-agent.html', 'r') as f:
    content = f.read()

old = """  // Fetch recent history for this focus to avoid repeats
  const focusKey=S.muscles.includes('full_body')?'full_body':S.muscles.join('_');
  const recentHistory=await fetchRecentHistory(focusKey);
  const recentExercises=[...new Set(recentHistory.flatMap(h=>h.exercises||[]))];
  const recentHint=recentExercises.length>0
    ?`\\n\\nAVOID these exercises used in recent sessions (use different ones): ${recentExercises.join(', ')}`
    :'';

  // Annotate library with movement patterns for smarter ordering
  const exList=filtered.length>0
    ?`EXERCISE LIBRARY — use ONLY these exact names:\\n${filtered.map(e=>{
        const meta=e.movement_pattern?` [${e.movement_pattern},pri:${e.order_priority},${e.role_hint}]`:'';
        return e.name+meta;
      }).join(', ')}`
    :'No library loaded. Use expert knowledge.';

  const ml=S.muscles.includes('full_body')?'Full Body':S.muscles.map(id=>MUSCLES.find(m=>m.id===id)?.label||id).join(', ');
  const eqList=EQ_GROUPS.filter(g=>S.eq.includes(g.id)).map(g=>g.label).join(', ')||'Body Weight only';"""

new = """  const focusKey=S.muscles.includes('full_body')?'full_body':S.muscles.join('_');
  const recentHistory=await fetchRecentHistory(focusKey);

  // Recency scoring: last session = -10, 2 ago = -5, 3 ago = -2
  const recencyScores={};
  const penalties=[-10,-5,-2];
  recentHistory.forEach((h,i)=>{
    (h.exercises||[]).forEach(name=>{
      recencyScores[name]=(recencyScores[name]||0)+penalties[i];
    });
  });
  const allRecent=Object.keys(recencyScores);
  const strongAvoid=allRecent.filter(n=>recencyScores[n]<=-10);
  const softAvoid=allRecent.filter(n=>recencyScores[n]>-10&&recencyScores[n]<=-5);
  const allUsed=new Set(allRecent);
  const freshExercises=filtered.filter(e=>!allUsed.has(e.name)).map(e=>e.name);

  let recentHint='';
  if(strongAvoid.length>0)recentHint+=`\\n\\nDO NOT USE (used last session): ${strongAvoid.join(', ')}`;
  if(softAvoid.length>0)recentHint+=`\\nPREFER TO AVOID (used recently): ${softAvoid.join(', ')}`;
  if(freshExercises.length>0)recentHint+=`\\nPREFER THESE (not used recently): ${freshExercises.join(', ')}`;

  // Circuit timing rules
  const circuitRules={'20 min':'1 circuit, 4 exercises, 3 rounds','30 min':'2 circuits, 3 exercises each, 3 rounds each','45 min':'2 circuits, 4 exercises each, 3 rounds each','60 min':'3 circuits, 4 exercises each, 3 rounds each'};
  const circuitNote=S.style==='circuit'?`\\nCIRCUIT STRUCTURE: ${circuitRules[S.time]||'2 circuits, 3-4 exercises, 3 rounds'}. Follow this exactly.`:'';

  // Legs focus includes calves
  const legsNote=S.muscles.includes('legs')?' Legs includes calves — include at least one calf exercise (e.g. Calf Raise, Lateral Step Up) as a finisher slot.':'';

  // Annotate library with movement patterns for smarter ordering
  const exList=filtered.length>0
    ?`EXERCISE LIBRARY — use ONLY these exact names:\\n${filtered.map(e=>{
        const meta=e.movement_pattern?` [${e.movement_pattern},pri:${e.order_priority},${e.role_hint}]`:'';
        return e.name+meta;
      }).join(', ')}`
    :'No library loaded. Use expert knowledge.';

  const ml=S.muscles.includes('full_body')?'Full Body':S.muscles.map(id=>MUSCLES.find(m=>m.id===id)?.label||id).join(', ');
  const eqList=EQ_GROUPS.filter(g=>S.eq.includes(g.id)).map(g=>g.label).join(', ')||'Body Weight only';"""

if old in content:
    content = content.replace(old, new)
    print('✓ 1. Recency scoring + circuit timing + legs note')
else:
    print('✗ 1. No match — printing first 200 chars of search target for debug:')
    print(repr(old[:200]))

old_prompt = """`Generate a ${S.time} strength workout.\\nFocus: ${ml}\\nEquipment: ${eqList}\\nStyle: ${S.style}\\n${GOAL_TEXT[S.goal]}\\n\\n${exList}\\n\\nRULES: Use EXACT exercise names from the library. Body Weight always allowed.\\n\\n${SCHEMAS[S.style]}\\n\\nReturn: {"workout_name":"string","warmup":[{"name":"string","duration":"string"}],"groups":[],"cooldown":[{"name":"string","duration":"string"}]}`"""

new_prompt = """`Generate a ${S.time} strength workout.\\nFocus: ${ml}${legsNote}\\nEquipment: ${eqList}\\nStyle: ${S.style}\\n${GOAL_TEXT[S.goal]}\\n\\n${exList}${recentHint}${circuitNote}\\n\\nRULES: Use EXACT exercise names from the library. Body Weight always allowed. Follow order_priority for exercise sequencing within groups.\\n\\n${SCHEMAS[S.style]}\\n\\nReturn: {"workout_name":"string","warmup":[{"name":"string","duration":"string"}],"groups":[],"cooldown":[{"name":"string","duration":"string"}]}`"""

if old_prompt in content:
    content = content.replace(old_prompt, new_prompt)
    print('✓ 2. Prompt updated')
else:
    print('✗ 2. Prompt not matched — printing for debug:')
    idx = content.find('Generate a ${S.time}')
    if idx > 0:
        print(repr(content[idx:idx+300]))

with open('/Users/nicolelloyd/Projects/workout/workout-agent.html', 'w') as f:
    f.write(content)

print('\nDone')
