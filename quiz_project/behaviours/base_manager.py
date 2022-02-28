from sqlalchemy.ext.asyncio import AsyncSession


class BaseManager:
    
    def __init__(self, database: AsyncSession):
        self.db = database
    
    def before_save(self, *args, **kwargs):
        pass

    def after_save(self, *args, **kwargs):
        pass

    def save(self, commit=True):
        self.before_save()
        self.db.add(self)
        if commit:
            try:
                self.db.commit()
            except Exception as e:
                self.db.rollback()
                raise e

        self.after_save()


    def before_update(self, *args, **kwargs):
        pass

    def after_update(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        self.before_update(*args, **kwargs)
        self.db.commit()
        self.after_update(*args, **kwargs)

    def delete(self, commit=True):
        self.db.delete(self)
        if commit:
            self.db.commit()