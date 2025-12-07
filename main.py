from app.schemas import LinkType, User, typed_decrypt_data
from app.user import get_user
from app.events import get_event

user = User(id="1", name="John Doe", email="john.doe@example.com", phone="1234567890")
print(user.link())
user_link = user.link().split("?start=")[1]
print(user_link)

def parse_link(link: str) -> tuple[LinkType, int]:
    decrypted_link_type, decrypted_id = typed_decrypt_data(link)
    match decrypted_link_type:
        case LinkType.USER:
            return get_user(decrypted_id)
        case LinkType.EVENT:
            return get_event(decrypted_id)
        case _:
            raise ValueError(f"Unknown link type: {decrypted_link_type}")

print(parse_link(user_link))