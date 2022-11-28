from tortoise import fields, Model

class SiteInfo(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    url = fields.TextField()
    img = fields.TextField()
    category = fields.TextField()
    cnt = fields.IntField()

    class Meta:
        table = "t_siteinfo2"

    def __str__(self):
        return self.name

class Test():
    def __init__(self) -> None:
        print('test init')