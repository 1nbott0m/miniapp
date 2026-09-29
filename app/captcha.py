import hashlib, hmac, io, secrets
from dataclasses import dataclass
from PIL import Image, ImageDraw, ImageFont

ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"

@dataclass
class CaptchaChallenge:
    answer: str
    salt: bytes
    digest: bytes
    def verify(self, answer: str) -> bool:
        normalized = answer.strip().upper()
        return hmac.compare_digest(self.digest, _digest(self.salt, normalized))
    def render(self) -> bytes:
        width, height = 640, 220
        image = Image.new("RGB", (width, height), "white"); draw = ImageDraw.Draw(image)
        for _ in range(12):
            x1, y1 = secrets.randbelow(width), secrets.randbelow(height)
            draw.line((x1, y1, secrets.randbelow(width), secrets.randbelow(height)), fill=(185,185,185), width=2)
        font = None
        for path in ("/System/Library/Fonts/Supplemental/Arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
            try:
                font = ImageFont.truetype(path, 86); break
            except OSError:
                pass
        if font is None: font = ImageFont.load_default(size=86)
        box = draw.textbbox((0, 0), self.answer, font=font, stroke_width=2)
        x, y = (width-(box[2]-box[0]))//2, (height-(box[3]-box[1]))//2-8
        draw.text((x, y), self.answer, fill=(15,15,15), font=font, stroke_width=2, stroke_fill=(15,15,15))
        out = io.BytesIO(); image.save(out, format="PNG"); return out.getvalue()

def _digest(salt: bytes, answer: str) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", answer.encode(), salt, 120_000)

def create_challenge(length: int = 6) -> CaptchaChallenge:
    answer = "".join(secrets.choice(ALPHABET) for _ in range(length))
    salt = secrets.token_bytes(16)
    return CaptchaChallenge(answer, salt, _digest(salt, answer))
