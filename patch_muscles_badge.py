with open('/Users/nicolelloyd/Projects/workout/workout-agent.html', 'r') as f:
    content = f.read()

# Add muscle badge style
old = ".ex-cue{font-size:13px;color:var(--t2);line-height:1.5;margin-top:4px}"
new = ".ex-cue{font-size:13px;color:var(--t2);line-height:1.5;margin-top:4px}\n.ex-muscles{font-size:11px;color:var(--t3);margin-top:2px;letter-spacing:.02em}"

if old in content:
    content = content.replace(old, new)
    print('✓ 1. Added .ex-muscles style')
else:
    print('ERROR: could not find .ex-cue style')

# Add muscle badge to exercise card render, after ex-reps
old = "      body.appendChild(el('p',{className:'ex-name'},ex.name));\n      body.appendChild(el('p',{className:'ex-reps'},ex.reps));\n      if(ex.cue)body.appendChild(el('p',{className:'ex-cue'},ex.cue));"
new = """      body.appendChild(el('p',{className:'ex-name'},ex.name));
      body.appendChild(el('p',{className:'ex-reps'},ex.reps));
      const exData=findExercise(ex.name);
      if(exData?.muscles?.length)body.appendChild(el('p',{className:'ex-muscles'},exData.muscles.join(' · ')));
      if(ex.cue)body.appendChild(el('p',{className:'ex-cue'},ex.cue));"""

if old in content:
    content = content.replace(old, new)
    print('✓ 2. Added muscle badge to exercise card')
else:
    print('ERROR: could not find exercise card render block')

with open('/Users/nicolelloyd/Projects/workout/workout-agent.html', 'w') as f:
    f.write(content)
