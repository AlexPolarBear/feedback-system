from dataclasses import dataclass

@dataclass(init=False)
class User_context:
    user_id: int
    tag_id: int
    
 
@dataclass
class User_context_get:
    user_id: int
    tag_id: int
