# Svoizizov Mini App

Mobile-first Telegram Mini App front-end for a clean CAPTCHA verification flow.

## Local preview

Serve this directory over HTTP (for example with any static file server) and open `index.html` in a browser. Telegram integration is optional during local preview; the screen works in demo mode with a locally generated CAPTCHA.

## Telegram integration

Host the `miniapp/` directory on a public HTTPS domain, configure it in BotFather under **Bot Settings → Configure Mini App**, and open it from a `web_app` button. The current `app.js` sends a `captcha_verified` payload through `Telegram.WebApp.sendData`; the bot must validate Telegram `initData` server-side before accepting it.

## Supabase

Use a Supabase Edge Function as the verification endpoint. Keep the Telegram bot token only in Supabase secrets, never in this frontend. The next integration step is to replace the demo comparison with a POST to the Edge Function and have the bot consume the validated result.
