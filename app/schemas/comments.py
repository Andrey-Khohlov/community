from pydantic import BaseModel


class CommentsAddSchema(BaseModel):
    '''Comments (Комментарии)
    --------
    Хранит комментарии, включая корневые и вложенные.

    Поле	    Тип данных	Описание
    id	        INT (PK)	Уникальный идентификатор комментария
    product_id	INT (FK)	Идентификатор обсуждаемого продукта
    user_id	    INT (FK)	Идентификатор автора комментария
    content	    TEXT	    Текст комментария
    parent_id	INT (FK)	ID родительского комментария (NULL для корневых)
    review_id   INT (FK)	ID родительского комментария (NULL для некорневых)
    created_at	TIMESTAMP	Время создания комментария
    updated_at	TIMESTAMP	Время последнего редактирования'''
    product_id: int
    user_id: int
    content: str
    parent_id: int
    review_id: int


class CommentsSchema(CommentsAddSchema):
    id: int
    created_at: str
    updated_at: str