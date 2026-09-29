const tg = window.Telegram?.WebApp;
tg?.ready(); tg?.expand();
const form = document.querySelector('#captcha-form');
const error = document.querySelector('#error');
const success = document.querySelector('#success');
const submit = document.querySelector('#submit');
form.addEventListener('submit',(e)=>{e.preventDefault(); if(!window.grecaptcha?.getResponse()){error.textContent='Подтвердите, что вы не робот'; return} submit.disabled=true; submit.textContent='Проверяем…'; setTimeout(()=>{form.hidden=true; success.hidden=false; tg?.sendData(JSON.stringify({type:'captcha_verified',token:window.grecaptcha.getResponse(),initData:tg?.initData||''}));},350);});
