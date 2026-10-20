// Keep the sidebar and anchor targets below the sticky header as its size changes.
(function(){
  var header=document.querySelector('header.top');
  if(!header)return;
  function updateHeight(){document.documentElement.style.setProperty('--wiki-header-height',header.getBoundingClientRect().height+'px')}
  updateHeight();
  if(window.ResizeObserver)new ResizeObserver(updateHeight).observe(header);
  else window.addEventListener('resize',updateHeight);
})();
(function(){var q=document.getElementById('q');if(!q)return;var t=document.getElementById('tbl'),rows=[].slice.call(t.tBodies[0].rows),fa=document.getElementById('fa'),ff=document.getElementById('ff'),fs=document.getElementById('fs'),c=document.getElementById('cnt');
var p=new URLSearchParams(location.search).get('q');if(p)q.value=p;
function run(){var s=q.value.toLowerCase(),n=0;rows.forEach(function(r){var ok=(!s||r.textContent.toLowerCase().indexOf(s)>-1)&&(!fa.value||r.dataset.a===fa.value)&&(!ff.value||('|'+r.dataset.f+'|').indexOf('|'+ff.value+'|')>-1)&&(!fs.value||r.dataset.s===fs.value);r.hidden=!ok;if(ok)n++});c.textContent=n+' of '+rows.length+' shown'}
[q,fa,ff,fs].forEach(function(e){e.addEventListener('input',run);e.addEventListener('change',run)});run()})();
// Native disclosure controls retain every navigation link on small screens.
(function(){
  var mobile=matchMedia('(max-width:820px)');
  function update(){document.querySelectorAll('.nav-group').forEach(function(group){group.open=!mobile.matches})}
  update();
  mobile.addEventListener('change',update);
})();
