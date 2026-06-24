with open('/Users/nicolelloyd/Projects/workout/workout-agent.html', 'r') as f:
    content = f.read()

changes = 0

# 1. Remove setup screen — go straight to main
old = "if(S.apiKey)S.screen='main';"
new = "S.screen='main';"
if old in content:
    content = content.replace(old, new)
    changes += 1
    print('✓ 1. Removed API key gate')

# 2. Remove gear icon from main header
old = "  h.appendChild(el('button',{className:'icon-btn',onClick:()=>{S.showSettings=true;S.settingsVal=S.apiKey;render();}},'⚙'));"
new = "  h.appendChild(el('span',{},''));"
if old in content:
    content = content.replace(old, new)
    changes += 1
    print('✓ 2. Removed gear icon from main header')

# 3. Remove gear icon from workout page header
old = "  hdr.appendChild(el('button',{className:'icon-btn',onClick:()=>{S.showSettings=true;S.settingsVal=S.apiKey;render();}},'⚙'));"
new = ""
if old in content:
    content = content.replace(old, new)
    changes += 1
    print('✓ 3. Removed gear icon from workout header')

# 4. Remove showSettings modal render call
old = "  if(S.showSettings)app.appendChild(renderModal());"
new = ""
if old in content:
    content = content.replace(old, new)
    changes += 1
    print('✓ 4. Removed modal render call')

# 5. Replace renderSetup with instant load
old = """function renderSetup(){
  const w=el('div',{className:'setup'});
  w.appendChild(el('h2',{},'Workout Agent'));
  w.appendChild(el('p',{},'Enter your Anthropic API key to get started.'));
  const inp=el('input',{type:'password',placeholder:'sk-ant-…',id:'ki'});
  const btn=el('button',{className:'gen-btn',style:{marginTop:'0'},onClick:()=>{const v=document.getElementById('ki').value.trim();if(!v)return;localStorage.setItem(LS_KEY,v);S.apiKey=v;S.screen='main';loadExercises();render();}});
  btn.textContent='Get started';
  const lnk=el('a',{href:'https://console.anthropic.com/settings/keys',target:'_blank',style:{color:'var(--acc)'}},'Get your API key →');
  const hint=el('p',{className:'hint',style:{textAlign:'center'}});hint.appendChild(lnk);
  const col=el('div',{style:{width:'100%',maxWidth:'380px',display:'flex',flexDirection:'column',gap:'14px'}});
  col.append(inp,btn,hint);w.appendChild(col);return w;
}"""
new = """function renderSetup(){
  const w=el('div',{className:'setup'});
  w.appendChild(el('h2',{},'Workout Agent'));
  return w;
}"""
if old in content:
    content = content.replace(old, new)
    changes += 1
    print('✓ 5. Replaced renderSetup')

# 6. Remove renderModal function entirely
old = """function renderModal(){
  const ov=el('div',{className:'modal-overlay',onClick:e=>{if(e.target===ov){S.showSettings=false;render();}}});
  const m=el('div',{className:'modal'});
  m.appendChild(el('h3',{},'Settings'));
  m.appendChild(el('label',{className:'flbl'},'Anthropic API Key'));
  const inp=el('input',{type:'password',placeholder:'sk-ant-…',value:S.settingsVal||'',onInput:e=>S.settingsVal=e.target.value});
  m.appendChild(inp);
  m.appendChild(el('p',{className:'hint'},'Stored in your browser only.'));
  const btns=el('div',{className:'modal-btns'});
  btns.appendChild(el('button',{className:'btn btn-ghost',onClick:()=>{S.showSettings=false;render();}},'Cancel'));
  btns.appendChild(el('button',{className:'btn btn-pri',onClick:()=>{const v=(S.settingsVal||'').trim();if(!v)return;localStorage.setItem(LS_KEY,v);S.apiKey=v;S.showSettings=false;render();}},'Save'));
  m.appendChild(btns);ov.appendChild(m);return ov;
}"""
new = ""
if old in content:
    content = content.replace(old, new)
    changes += 1
    print('✓ 6. Removed renderModal function')

# 7. Switch doGenerate to call /api/generate instead of Anthropic directly
old = "    const res=await fetch('https://api.anthropic.com/v1/messages',{\n      method:'POST',\n      headers:{'Content-Type':'application/json','x-api-key':S.apiKey,'anthropic-version':'2023-06-01','anthropic-dangerous-direct-browser-access':'true'},"
new = "    const res=await fetch('/api/generate',{\n      method:'POST',\n      headers:{'Content-Type':'application/json'},"
if old in content:
    content = content.replace(old, new)
    changes += 1
    print('✓ 7. Switched to /api/generate endpoint')

# 8. Remove API key check at start of doGenerate
old = "  if(!S.apiKey){S.error='No API key — tap ⚙ to add it.';render();return;}\n  S.loading=true;"
new = "  S.loading=true;"
if old in content:
    content = content.replace(old, new)
    changes += 1
    print('✓ 8. Removed API key check from doGenerate')

with open('/Users/nicolelloyd/Projects/workout/workout-agent.html', 'w') as f:
    f.write(content)

print(f'\nDone — {changes}/8 changes applied')
if changes < 8:
    print('WARNING: some changes did not apply — check manually')
