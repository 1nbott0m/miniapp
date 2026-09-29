from dataclasses import dataclass
from datetime import datetime, timedelta
from .captcha import CaptchaChallenge, create_challenge

@dataclass
class PendingChallenge:
    user_id: int; source_message_id: int; message_id: int; created_at: datetime; attempts: int; answer: str; _captcha: CaptchaChallenge

class RegistrationService:
    def __init__(self, ttl_seconds=30, max_attempts=3, factory=create_challenge):
        self.ttl = timedelta(seconds=ttl_seconds); self.max_attempts = max_attempts; self.factory = factory
        self.open_chats=set(); self.pending={}; self.confirmed={}; self._next_message=100000
    def open(self, chat_id): self.open_chats.add(chat_id); self.confirmed.setdefault(chat_id, [])
    def close(self, chat_id): self.open_chats.discard(chat_id)
    def request_plus(self, chat_id, user_id, source_message_id, now):
        if chat_id not in self.open_chats or user_id in self.confirmed.get(chat_id, []) or (chat_id,user_id) in self.pending: return None
        c=self.factory(); self._next_message += 1
        p=PendingChallenge(user_id, source_message_id, self._next_message, now, 0, c.answer, c)
        self.pending[(chat_id,user_id)] = p; return p
    def answer(self, chat_id, user_id, captcha_message_id, answer, now):
        key=(chat_id,user_id); p=self.pending.get(key)
        if not p or p.message_id != captcha_message_id: return False
        if now - p.created_at > self.ttl: self.pending.pop(key,None); return False
        if p._captcha.verify(answer):
            self.pending.pop(key,None); self.confirmed.setdefault(chat_id, []).append(user_id); return True
        p.attempts += 1
        if p.attempts >= self.max_attempts: self.pending.pop(key,None)
        return False
    def confirm_webapp(self, chat_id, user_id):
        key = (chat_id, user_id)
        if key not in self.pending or user_id in self.confirmed.get(chat_id, []):
            return False
        self.pending.pop(key, None)
        self.confirmed.setdefault(chat_id, []).append(user_id)
        return True
    def queue(self, chat_id): return list(self.confirmed.get(chat_id, []))
    def clear(self, chat_id): self.confirmed[chat_id]=[]; [self.pending.pop(k,None) for k in list(self.pending) if k[0]==chat_id]
