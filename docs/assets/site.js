/* Gushi Repo — interactions: header state, scroll reveal, device tilt, copy toast */
(function(){
'use strict';
var d=document.documentElement;d.classList.add('js');
var mReduce=matchMedia('(prefers-reduced-motion: reduce)');

/* sticky header border */
var top=document.getElementById('top');
function onScroll(){if(top)top.classList.toggle('scrolled',scrollY>8)}
addEventListener('scroll',onScroll,{passive:true});onScroll();

/* reveal on scroll with stagger */
var els=[].slice.call(document.querySelectorAll('.reveal'));
if('IntersectionObserver' in window&&!mReduce.matches){
  var io=new IntersectionObserver(function(entries){
    entries.forEach(function(en){if(en.isIntersecting){en.target.classList.add('in');io.unobserve(en.target)}});
  },{threshold:.12,rootMargin:'0px 0px -7% 0px'});
  els.forEach(function(el){io.observe(el)});
}else{
  els.forEach(function(el){el.classList.add('in')});
}

/* pointer tilt on the lock-screen device (hover-capable, motion-safe only) */
var dev=document.querySelector('.device');
if(dev&&matchMedia('(hover:hover)').matches&&!mReduce.matches){
  var raf=null;
  dev.addEventListener('pointermove',function(ev){
    if(raf)return;
    raf=requestAnimationFrame(function(){
      raf=null;
      var r=dev.getBoundingClientRect();
      var x=(ev.clientX-r.left)/r.width-.5,y=(ev.clientY-r.top)/r.height-.5;
      dev.style.setProperty('--rx',(-y*7).toFixed(2)+'deg');
      dev.style.setProperty('--ry',(x*10).toFixed(2)+'deg');
    });
  });
  dev.addEventListener('pointerleave',function(){
    dev.style.setProperty('--rx','0deg');dev.style.setProperty('--ry','0deg');
  });
}

/* copy source URL with toast feedback */
var toast=document.createElement('div');toast.className='toast';toast.setAttribute('role','status');
var toastTimer=null;
function showToast(msg){
  toast.textContent=msg;
  if(!toast.isConnected)document.body.appendChild(toast);
  toast.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer=setTimeout(function(){toast.classList.remove('show')},1900);
}
function legacyCopy(text){
  var i=document.createElement('textarea');i.value=text;i.setAttribute('readonly','');
  i.style.cssText='position:fixed;opacity:0';document.body.appendChild(i);
  i.select();try{document.execCommand('copy')}catch(e){}
  i.remove();
}
[].slice.call(document.querySelectorAll('.copy')).forEach(function(btn){
  btn.addEventListener('click',function(){
    var text=btn.getAttribute('data-copy')||'';
    if(navigator.clipboard&&navigator.clipboard.writeText){
      navigator.clipboard.writeText(text).then(function(){showToast('已复制 · Copied')},function(){legacyCopy(text);showToast('已复制 · Copied')});
    }else{legacyCopy(text);showToast('已复制 · Copied')}
  });
});
/* expand / collapse all changelog entries */
var tgl=document.querySelector('.toggleall');
if(tgl){
  tgl.addEventListener('click',function(){
    var expand=tgl.getAttribute('aria-expanded')!=='true';
    tgl.setAttribute('aria-expanded',String(expand));
    tgl.textContent=expand?'收起全部 · Collapse all':'展开全部 · Expand all';
    document.querySelectorAll('#changelog details').forEach(function(d){d.open=expand});
  });
}
})();
