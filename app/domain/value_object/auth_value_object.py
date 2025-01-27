from dataclasses import dataclass

JWT_ALGORITHM = 'HS256'


@dataclass
class Claims:
    sub: str
    iat: int
    exp: int
