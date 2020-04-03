from ZoopAPIWrapper import ZoopWrapper


client = ZoopWrapper()

response = client.retrieve_invoice('')

data = response.instance.to_dict()
print(response)
