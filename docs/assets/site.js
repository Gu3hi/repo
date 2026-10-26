/* Gushi Repo: viewport reveals, device views, source copy and changelogs. */
(function(){
'use strict';
var d=document.documentElement;d.classList.add('js');
var mReduce=matchMedia('(prefers-reduced-motion: reduce)');

/* reveal on scroll with stagger */
var els=[].slice.call(document.querySelectorAll('.reveal'));
if('IntersectionObserver' in window&&!mReduce.matches){
  var io=new IntersectionObserver(function(entries){
    entries.forEach(function(en){if(en.isIntersecting){en.target.classList.add('in');io.unobserve(en.target)}});
  },{threshold:.18,rootMargin:'0px 0px -4% 0px'});
  els.forEach(function(el){io.observe(el)});
}else{
  els.forEach(function(el){el.classList.add('in')});
}

/* Each phrase is observed separately so the reading order follows the viewport. */
var words=document.querySelectorAll('.word-reveal');
if('IntersectionObserver' in window&&!mReduce.matches){
  var wordObserver=new IntersectionObserver(function(entries){
    entries.forEach(function(entry){if(entry.isIntersecting){entry.target.classList.add('lit');wordObserver.unobserve(entry.target)}});
  },{threshold:1,rootMargin:'0px 0px -18% 0px'});
  words.forEach(function(word){wordObserver.observe(word)});
}else{words.forEach(function(word){word.classList.add('lit')})}

/* Switch between two actual device captures without moving the device frame. */
var preview=document.getElementById('device-preview');
var viewButtons=document.querySelectorAll('[data-preview]');
viewButtons.forEach(function(button){
  button.addEventListener('click',function(){
    preview.classList.toggle('wallpaper',button.getAttribute('data-preview')==='wallpaper');
    viewButtons.forEach(function(item){item.setAttribute('aria-pressed',String(item===button))});
    preview.querySelectorAll('img').forEach(function(img){
      img.setAttribute('aria-hidden',String(img.classList.contains('wallpaper-shot')?button.getAttribute('data-preview')!=='wallpaper':button.getAttribute('data-preview')!=='player'));
    });
  });
});

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
  i.select();var copied=false;try{copied=document.execCommand('copy')}catch(e){}
  i.remove();return copied;
}
[].slice.call(document.querySelectorAll('.copy')).forEach(function(btn){
  btn.addEventListener('click',function(){
    var text=btn.getAttribute('data-copy')||'';
    if(navigator.clipboard&&navigator.clipboard.writeText){
      navigator.clipboard.writeText(text).then(function(){showToast('已复制 · Copied')},function(){showToast(legacyCopy(text)?'已复制 · Copied':'未能复制，请手动选择源地址 · Copy failed')});
    }else{showToast(legacyCopy(text)?'已复制 · Copied':'未能复制，请手动选择源地址 · Copy failed')}
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
