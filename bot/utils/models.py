from tortoise import fields
from tortoise.models import Model


class TagModel(Model):
    """A tag model for tortoise ORM sqlite database."""
    guild_id = fields.IntField()
    author_id = fields.IntField()
    name = fields.TextField()
    content = fields.TextField()
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    uses = fields.IntField()

    def __str__(self):
        """Return the content of the model"""
        return self.content
