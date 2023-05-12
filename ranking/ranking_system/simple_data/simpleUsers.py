from struct_data.tag import Tag
from struct_data.context import Context
from struct_data.user import User

simple_users = [
    User(
    chat_id=23256,
    name="Komnatskiy Aleksandr",
    email="st123224@gmail.com",
    direction="НОД",
    context=Context(
        {
            1 : Tag(id=1, title="Алгебра", type=0),
            2 : Tag(id=2, title="Группы", type=5),
        }
    )
    )
]