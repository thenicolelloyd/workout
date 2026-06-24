with open('/Users/nicolelloyd/Projects/workout/workout-agent.html', 'r') as f:
    content = f.read()

old = "const MUSCLES=[{id:'full_body',label:'Full Body'},{id:'back_chest',label:'Back & Chest'},{id:'shoulders',label:'Shoulders'},{id:'arms',label:'Arms'},{id:'core',label:'Core'},{id:'glutes',label:'Glutes, Hamstrings & Quads'},{id:'calves',label:'Calves'}];"
new = "const MUSCLES=[{id:'full_body',label:'Full Body'},{id:'back_chest',label:'Back & Chest'},{id:'shoulders',label:'Shoulders'},{id:'arms',label:'Arms'},{id:'core',label:'Core'},{id:'legs',label:'Legs'}];"

if old in content:
    content = content.replace(old, new)
    with open('/Users/nicolelloyd/Projects/workout/workout-agent.html', 'w') as f:
        f.write(content)
    print('Done — Legs pill replaces Glutes/Hamstrings/Quads + Calves')
else:
    print('ERROR: could not find MUSCLES array')
