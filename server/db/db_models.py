from tortoise.models import Model
from tortoise import fields


class Admin(Model):
    id = fields.IntField(primary_key=True)
    email = fields.CharField(max_length=256, unique=True)
    name = fields.CharField(max_length=256)
    password = fields.CharField(max_length=256)

    class Meta:
        table = "admins"


class Student(Model):
    id = fields.IntField(primary_key=True)
    session_id = fields.ForeignKeyField("models.Session")
    name = fields.CharField(max_length=256)
    group = fields.CharField(max_length=64)

    class Meta:
        table = "students"


class Session(Model):
    id = fields.IntField(primary_key=True)
    date_started = fields.DatetimeField()
    duration = fields.TimeDeltaField()
    test_duration = fields.TimeDeltaField()
    questions_types = fields.JSONField()
    max_score = fields.IntField()
    finished = fields.BooleanField(default=False)

    class Meta:
        table = "sessions"


class Question(Model):
    id = fields.IntField(primary_key=True)
    session = fields.ForeignKeyField("models.Session")
    student = fields.ForeignKeyField("models.Student")
    type = fields.CharField(max_length=256)
    question = fields.JSONField()

    class Meta:
        table = "questions"


class Result(Model):
    id = fields.IntField(primary_key=True)
    session = fields.ForeignKeyField("models.Session")
    student_name = fields.CharField(max_length=256)
    group = fields.CharField(max_length=64)
    score = fields.IntField()

    class Meta:
        table = "results"
