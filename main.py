from loguru import logger

from app.config import link_template
from app.crypto import encrypt_data
from app.events import get_event
from app.schemas import Building, LinkType, Mail, User, typed_decrypt_data
from app.user import get_user

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
        case LinkType.MAIL:
            return (Mail(send_building=Building.from_value(decrypted_id)), -1)
        case _:
            raise ValueError(f"Unknown link type: {decrypted_link_type}")


# print(parse_link(user_link))

# mail_number = generate_stamp()
# print(mail_number)

link = link_template.format(
    encrypted=encrypt_data(f"{LinkType.MAIL.value}_{Building.POKROVKA.value()}")
)
logger.debug(link)
logger.debug(parse_link(link.split("?start=")[1] if "?start=" in link else link))

link = link_template.format(
    encrypted=encrypt_data(f"{LinkType.MAIL.value}_{Building.MYASO.value()}")
)
logger.debug(link)
logger.debug(parse_link(link.split("?start=")[1] if "?start=" in link else link))


link = link_template.format(
    encrypted=encrypt_data(f"{LinkType.MAIL.value}_{Building.BASMAN.value()}")
)
logger.debug(link)
logger.debug(parse_link(link.split("?start=")[1] if "?start=" in link else link))
# print(link_template.format(encrypted=encrypt_data(f"{LinkType.MAIL.value}")))

# print(
#     parse_link(link_template.format(encrypted=encrypt_data(f"{LinkType.MAIL.value}")))
# )
