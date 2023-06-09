import configparser

config = configparser.ConfigParser()

# Add the structure to the file we will create
config.add_section('validation')
config.set('validation', 'new_bal', '1000')
config.set('validation', 'old_bal', '1000')
config.set('validation', 'rules', '''{"balance_match":["old_bal==new_bal"], "presence":["'amount' in fileA.columns"]}''')

config.add_section('data_transform')
config.set('data_transform', 'limitsA', '{"amount":[3, 6], "name":[5, -1]}')
config.set('data_transform', 'limitsB', '{"balance":[2, 5]}')
config.set('data_transform', 'new_colsA', '{"netamt":["(","amount","+","interest",")"]}')
config.set('data_transform', 'new_colsB', '{"title":["name"]}')

config.add_section('generate_map')
config.set('generate_map', 'uniqueA', '{"name":"amount"}')
config.set('generate_map', 'uniqueB', '{}')
config.set('generate_map', 'sumA', '{}')
config.set('generate_map', 'sumB', '{"name":"balance"}')

config.add_section('matching')
config.set('matching', 'match_dict', '{"name":["title", "ALL_A"], "netamt":["balance", "pending_amt", "ANY_A"]}')

# Write the new structure to the new file
with open("config.ini", 'w') as configfile:
    config.write(configfile)