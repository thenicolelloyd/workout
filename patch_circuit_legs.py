with open('/Users/nicolelloyd/Projects/workout/workout-agent.html', 'r') as f:
    content = f.read()

changes = 0

# 1. Add muscle badge style
old = ".ex-cue{font-size:13px;color:var(--t2);line-height:1.5;margin-top:4px}"
new = ".ex-cue{font-size:13px;color:var(--t2);line-height:1.5;margin-top:4px}\n.ex-muscles{font-size:11px;color:var(--t3);margin-top:2px;letter-spacing:.02em}"
if old in content:
    content = content.replace(old, new)
    changes += 1
    print('✓ 1. Added .ex-muscles style')
else:
    print('✗ 1. Could not find .ex-cue style')

# 2. Add muscle badge to exercise card render
old = "      body.appendChild(el('p',{className:'ex-name'},ex.name));\n      body.appendChild(el('p',{className:'ex-reps'},ex.reps));\n      if(ex.cue)body.appendChild(el('p',{className:'ex-cue'},ex.cue));"
new = """      body.appendChild(el('p',{className:'ex-name'},ex.name));
      body.appendChild(el('p',{className:'ex-reps'},ex.reps));
      const exData=findExercise(ex.name);
      if(exData?.muscles?.length)body.appendChild(el('p',{className:'ex-muscles'},exData.muscles.join(' · ')));
      if(ex.cue)body.appendChild(el('p',{className:'ex-cue'},ex.cue));"""
if old in content:
    content = content.replace(old, new)
    changes += 1
    print('✓ 2. Added muscle badge to exercise card')
else:
    print('✗ 2. Could not find exercise card render block')

# 3. Add circuit timing lookup before doGenerate prompt
old = "  const ml=S.muscles.includes('full_body')?'Full Body':S.muscles.map(id=>MUSCLES.find(m=>m.id===id)?.label||id).join(', ');"
new = """  const ml=S.muscles.includes('full_body')?'Full Body':S.muscles.map(id=>MUSCLES.find(m=>m.id===id)?.label||id).join(', ');
  const legsNote=S.muscles.includes('legs')?' Legs includes calves — include at least one calf exercise (e.g. Calf Raise, Lateral Step Up) as a finisher slot.':'';
  const circuitRules={'20 min':'1 circuit, 4 exercises, 3 rounds','30 min':'2 circuits, 3 exercises each, 3 rounds each','45 min':'2 circuits, 4 exercises each, 3 rounds each','60 min':'3 circuits, 4 exercises each, 3 rounds each'};
  const circuitNote=S.style==='circuit'?`\\nCIRCUIT STRUCTURE FOR ${S.time}: ${circuitRules[S.time]||'2 circuits, 3-4 exercises, 3 rounds'}.`:''"""
if old in content:
    content = content.replace(old, new)
    changes += 1
    print('✓ 3. Added legs note + circuit timing lookup')
else:
    print('✗ 3. Could not find ml line')

# 4. Inject legsNote and circuitNote into the user prompt
old = "`Generate a ${S.time} strength workout.\\nFocus: ${ml}\\nEquipment: ${eqList}\\nStyle: ${S.style}\\n${GOAL_TEXT[S.goal]}\\n\\n${exList}${recentHint}\\n\\nRULES: Use EXACT exercise names from the library. Body Weight always allowed. Follow order_priority for exercise sequencing within groups.\\n\\n${SCHEMAS[S.style]}\\n\\nReturn: {\"workout_name\":\"string\",\"warmup\":[{\"name\":\"string\",\"duration\":\"string\"}],\"groups\":[],\"cooldown\":[{\"name\":\"string\",\"duration\":\"string\"}]}`"
new = "`Generate a ${S.time} strength workout.\\nFocus: ${ml}${legsNote}\\nEquipment: ${eqList}\\nStyle: ${S.style}\\n${GOAL_TEXT[S.goal]}\\n\\n${exList}${recentHint}${circuitNote}\\n\\nRULES: Use EXACT exercise names from the library. Body Weight always allowed. Follow order_priority for exercise sequencing within groups.\\n\\n${SCHEMAS[S.style]}\\n\\nReturn: {\"workout_name\":\"string\",\"warmup\":[{\"name\":\"string\",\"duration\":\"string\"}],\"groups\":[],\"cooldown\":[{\"name\":\"string\",\"duration\":\"string\"}]}`"
if old in content:
    content = content.replace(old, new)
    changes += 1
    print('✓ 4. Injected legs note + circuit rules into prompt')
else:
    print('✗ 4. Could not find user prompt string')

with open('/Users/nicolelloyd/Projects/workout/workout-agent.html', 'w') as f:
    f.write(content)

print(f'\nDone — {changes}/4 changes applied')
if changes < 4:
    print('WARNING: some changes did not apply — check manually')
