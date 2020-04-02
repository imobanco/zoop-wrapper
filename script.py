from ZoopAPIWrapper import ZoopWrapper
from ZoopAPIWrapper.models.token import Token


client = ZoopWrapper()

token = Token(
    bank_code='001',
    taxpayer_id='12685293892',
    holder_name='foo',
    account_number='1',
    routing_number='1',
    type='checking'
)

data = token.to_dict()

response = client.add_bank_account(data)

print(response)
