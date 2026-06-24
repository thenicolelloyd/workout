with open('/Users/nicolelloyd/Projects/workout/workout-agent.html', 'r') as f:
    content = f.read()

changes = 0

# 1. Clean up orphaned constants and state
old = "const LS_KEY='wo_api_key';\n"
new = ""
if old in content:
    content = content.replace(old, new)
    changes += 1
    print('✓ 1. Removed LS_KEY constant')

old = "  apiKey:localStorage.getItem(LS_KEY)||'',\n"
new = ""
if old in content:
    content = content.replace(old, new)
    changes += 1
    print('✓ 2. Removed apiKey from state')

old = "  lightbox:null,showSettings:false,settingsVal:'',\n"
new = "  lightbox:null,\n"
if old in content:
    content = content.replace(old, new)
    changes += 1
    print('✓ 3. Removed showSettings/settingsVal from state')

# 2. Add pulse keyframe animation after existing animations
old = "@keyframes groupFlash{0%{border-color:var(--acc);box-shadow:0 0 0 1px var(--acc)}40%{border-color:var(--acc);box-shadow:0 0 0 1px var(--acc)}100%{border-color:var(--b1);box-shadow:none}}"
new = "@keyframes groupFlash{0%{border-color:var(--acc);box-shadow:0 0 0 1px var(--acc)}40%{border-color:var(--acc);box-shadow:0 0 0 1px var(--acc)}100%{border-color:var(--b1);box-shadow:none}}\n@keyframes btnPulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.75;transform:scale(.98)}}\n.gen-btn.pulsing{animation:btnPulse 1.2s ease-in-out infinite}"
if old in content:
    content = content.replace(old, new)
    changes += 1
    print('✓ 4. Added pulse keyframe + .pulsing class')

# 3. Update gen-btn to use pulsing class when loading
old = "  const gb=el('button',{className:'gen-btn',onClick:doGenerate},S.loading?'Building your workout…':'Generate Workout →');\n  if(S.loading)gb.setAttribute('disabled','true');"
new = "  const gb=el('button',{className:'gen-btn'+(S.loading?' pulsing':''),onClick:doGenerate},S.loading?'Building your workout…':'Generate Workout →');\n  if(S.loading)gb.setAttribute('disabled','true');"
if old in content:
    content = content.replace(old, new)
    changes += 1
    print('✓ 5. Button pulses while loading')

with open('/Users/nicolelloyd/Projects/workout/workout-agent.html', 'w') as f:
    f.write(content)

print(f'\nDone — {changes}/5 changes applied')
if changes < 5:
    print('WARNING: some changes did not apply — check manually')
