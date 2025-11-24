import jwt
import datetime

secret = "m_obhz$^rlrs8hyfh^uhps=c85u@visg@o-&^s6!_=3wz^!8!#"

payload = {
  "token_type": "access",
  "exp": 1764040865,
  "iat": 1763954465,
  "jti": "ad5dce07da41416abfea3483c234ff1a",
  "sub": "erika.neri@forteplus.com.br",
  "user_id": 1,
  "user_name": "Erika Neri",
  "aud": [
    "app",
    "api",
    "assinaturas",
    "events"
  ],
  "iss": "accounts"
}

token = jwt.encode(payload, secret, algorithm="HS256")
print(token)
