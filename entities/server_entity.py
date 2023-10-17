from typing import Dict, List, Optional, Tuple
from pydantic import BaseModel, Field

class WarpChatgptInput(BaseModel):
    query :str = Field(title="The description of the item", max_length=10)
    model:str = Field(title="The description of the item", max_length=10)
    temperature : float  =Field(title="The description of the item", max_length=10)
    n :int =Field(title="The description of the item", max_length=10)
    max_tokens:int =Field(title="The description of the item", max_length=10)
    history:List[Dict[str,str]] = Field(title="The description of the item", max_length=10)
    system :str =Field(title="The description of the item", max_length=10)


class WarpChatgptOutput(BaseModel):
    answer:str = Field(title="The description of the item", max_length=10)
    token_num:int = Field(title="The description of the item", max_length=10)

