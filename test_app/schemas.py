from quiz_project.behaviours import BaseSchema


class TestSchema(BaseSchema):
    holder: int = None
    published: bool = True