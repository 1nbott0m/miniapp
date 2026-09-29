const tg = window.Telegram?.WebApp;
tg?.ready(); tg?.expand();
const input = document.querySelector('#captcha-input');
const form = document.querySelector('#captcha-form');
const error = document.querySelector('#error');
const success = document.querySelector('#success');
const submit = document.querySelector('#submit');
let expected = '';
const alphabet = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
function newCaptcha(){ expected = Array.from({length:6},()=>alphabet[Math.floor(Math.random()*alphabet.length)]).join(''); const canvas=document.createElement('canvas'); canvas.width=900; canvas.height=300; const c=canvas.getContext('2d'); c.fillStyle='#fff'; c.fillRect(0,0,900,300); c.strokeStyle='#cbd0d9'; c.lineWidth=3; for(let i=0;i<10;i++){c.beginPath();c.moveTo(Math.random()*900,Math.random()*300);c.lineTo(Math.random()*900,Math.random()*300);c.stroke()} c.fillStyle='#111827'; c.font='800 112px Manrope, sans-serif'; c.textAlign='center'; c.textBaseline='middle'; c.fillText(expected,450,158); image.src=canvas.toDataURL('image/png'); input.value=''; error.textContent='';}
form.addEventListener('submit',(e)=>{e.preventDefault(); if(!window.grecaptcha?.getResponse()){error.textContent='Подтвердите, что вы не робот'; return} submit.disabled=true; submit.textContent='Проверяем…'; setTimeout(()=>{form.hidden=true; success.hidden=false; tg?.sendData(JSON.stringify({type:'captcha_verified',token:window.grecaptcha.getResponse(),initData:tg?.initData||''}));},350);});
