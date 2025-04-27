

# from database.db import

# res = add_numbers(2, 7)
# print(res)
# print(res.get(blocking=False))
# print(res.get(blocking=True, timeout=10))

from database.db import DatabaseStore

# user = DatabaseStore.users.upsert('bayan79', {'name': 'Kirlli', 'value': {'some': 'shit'}})
user = DatabaseStore.users.get_by_key('bayan79')
print(user)

# action = DatabaseStore.action.get({'action': 'a1'})
# action['action'] = 'a2'
# saved = DatabaseStore.action.upsert({'action': 'a1', ''})