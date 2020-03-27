from ZoopAPIWrapper import ZoopWrapper


client = ZoopWrapper()

data = {
    "card_brand": "MasterCard",
    "first4_digits": "5201",
    "last4_digits": "4014",
    "expiration_month": "3",
    "expiration_year": "2020",
    "holder_name": "Mcihella"
}

response = client.add_card(data, 'e7eec0f640c14e21b35d20d58b49b584')

print(response)
