const tg = window.Telegram?.WebApp;
tg?.ready(); tg?.expand();
const form = document.querySelector('#captcha-form');
const error = document.querySelector('#error');
const success = document.querySelector('#success');
const submit = document.querySelector('#submit');
 form.addEventListener('submit',(e)=>{e.preventDefault(); const token=window.grecaptcha?.getResponse(); if(!token){error.textContent='Подтвердите, что вы не робот'; return} submit.disabled=true; submit.textContent='Проверяем…'; setTimeout(()=>{form.hidden=true; success.hidden=false; const params=new URLSearchParams(location.search); tg?.sendData(JSON.stringify({type:'captcha_verified',token,chat_id:params.get('chat_id'),user_id:params.get('user_id'),challenge:params.get('challenge'),initData:tg?.initData||''}));},350);});
