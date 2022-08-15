from tortoise import fields, models


class Source(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    id = fields.IntField(pk=True)
    source = fields.ForeignKeyField('models.Source', related_name='vacancies')
    technology = fields.CharField(max_length=50, null=True)
    date = fields.DatetimeField(auto_now=True)
    description = fields.CharField(max_length=500, null=True)
    url = fields.CharField(max_length=150, null=True)

    def __str__(self):
        return self.technology
