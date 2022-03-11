from quiz_project.behaviours import BaseSchema


class TestSchema(BaseSchema):
    holder: str | None
    published: bool
