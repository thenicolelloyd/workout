with open('/Users/nicolelloyd/Projects/workout/workout-agent.html', 'r') as f:
    content = f.read()

old = """  // Fetch recent history for this focus to avoid repeats
  const focusKey=S.muscles.includes('full_body')?'full_body':S.muscles.join('_');
  const recentHistory=await fetchRecentHistory(focusKey);
  const recentExercises=[...new Set(recentHistory.flatMap(h=>h.exercises||[]))];
  const recentHint=recentExercises.length>0
    ?`\\n\\nAVOID these exercises used in recent sessions (use different ones): ${recentExercises.join(', ')}`
    :'';"""

new = """  // Fetch recent history and build recency-scored hint
  const focusKey=S.muscles.includes('full_body')?'full_body':S.muscles.join('_');
  const recentHistory=await fetchRecentHistory(focusKey);

  // Score each exercise by recency: last session = -10, 2 ago = -5, 3 ago = -2
  const recencyScores={};
  const penalties=[-10,-5,-2];
  recentHistory.forEach((h,i)=>{
    (h.exercises||[]).forEach(name=>{
      recencyScores[name]=(recencyScores[name]||0)+penalties[i];
    });
  });

  // Split into tiers for the prompt
  const allRecent=Object.keys(recencyScores);
  const strongAvoid=allRecent.filter(n=>recencyScores[n]<=-10);
  const softAvoid=allRecent.filter(n=>recencyScores[n]>-10&&recencyScores[n]<=-5);
  const allUsed=new Set(allRecent);
  const freshExercises=S.exercises
    .filter(e=>!allUsed.has(e.name)&&getFiltered().find(f=>f.name===e.name))
    .map(e=>e.name);

  let recentHint='';
  if(strongAvoid.length>0) recentHint+=`\\n\\nDO NOT USE (used last session): ${strongAvoid.join(', ')}`;
  if(softAvoid.length>0) recentHint+=`\\nPREFER TO AVOID (used recently): ${softAvoid.join(', ')}`;
  if(freshExercises.length>0) recentHint+=`\\nPREFER THESE (not used recently): ${freshExercises.join(', ')}`;"""

if old in content:
    content = content.replace(old, new)
    with open('/Users/nicolelloyd/Projects/workout/workout-agent.html', 'w') as f:
        f.write(content)
    print('Done — recency scoring added')
else:
    print('ERROR: could not find target block — no changes made')
