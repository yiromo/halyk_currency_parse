from tortoise.models import Model
from tortoise import fields
from pydantic import BaseModel

class Currency(Model):
    id = fields.IntField(pk=True)
    currency_pair = fields.CharField(max_length=10)
    buy = fields.FloatField()
    sell = fields.FloatField()

class CurrencyIn(BaseModel):
    currency_pair: str
    buy: float
    sell: float