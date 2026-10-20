(function(){
  const figure=document.querySelector('.problem-figure');
  const drawings=window.ENGRAVE && window.ENGRAVE.heroes;
  if(!figure || !drawings || !drawings.length)return;
  const art=document.getElementById('problem-art');
  const caption=document.getElementById('problem-caption');
  const id=document.getElementById('problem-id');
  const title=document.getElementById('problem-title');
  const next=document.getElementById('problem-next');
  const reducedMotion=matchMedia('(prefers-reduced-motion:reduce)');
  let current=0;
  function show(index){
    current=index;
    const drawing=drawings[index];
    art.innerHTML=drawing.svg;
    id.textContent='MAIS-'+drawing.id;
    title.textContent=drawing.title;
    caption.href='p/MAIS-'+drawing.id+'.html';
    const svg=art.querySelector('svg');
    if(reducedMotion.matches && svg && svg.pauseAnimations)svg.pauseAnimations();
    try{localStorage.setItem('mais-last',drawing.id)}catch(e){}
  }
  let last=null;
  try{last=localStorage.getItem('mais-last')}catch(e){}
  const pool=drawings.map((drawing,index)=>index).filter(index=>drawings[index].id!==last);
  show(pool.length ? pool[Math.floor(Math.random()*pool.length)] : 0);
  figure.hidden=false;
  next.addEventListener('click',()=>show((current+1)%drawings.length));
})();
