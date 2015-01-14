- Pagination
- "list_nodes"
- HTML client
- print documentation


resource_list = api.resource_list()

# ends when resource ends
for item in resource_list.get():
    print item.data

# fetches next page
for item in resource_list.get().iterator():
    print item.data

