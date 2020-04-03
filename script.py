from ZoopAPIWrapper import ZoopWrapper
from ZoopAPIWrapper.models.token import Token


client = ZoopWrapper()

token = Token(
    card_number='123123123123123',
    holder_name='foo',
    expiration_month='01',
    expiration_year='01',
    security_code='111'
)

data = token.to_dict()

response = client.add_card(data, 'e7eec0f640c14e21b35d20d58b49b584')

print(response)
