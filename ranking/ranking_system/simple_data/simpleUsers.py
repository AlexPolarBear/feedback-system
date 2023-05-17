from struct_data.tag import Tag
from struct_data.user import User

simple_users = { 1 : 
    User(
    chat_id=1,
    name="Komnatskiy Aleksandr",
    email="st123224@gmail.com",
    direction="НОД",
    context=
        {
            "Алгебра" : Tag(id=1, title="Алгебра", type=0),
            "Группы" : Tag(id=2, title="Группы", type=5),
        }

    )
}