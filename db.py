class InMemoryDatabase:
    def __init__(self):
        self.database = {}
        self.meta_data = {}
        self.transaction_stack = []

    def begin_transaction(self):
        self.transaction_stack.append([])

    def is_transaction_active(self):
        return len(self.transaction_stack) > 0
    
    def get_current_transaction(self):
        if not self.is_transaction_active():
            print('NO TRANSACTION')
            return
        return self.transaction_stack[-1]

    def set_record(self, record_key, record_value):
        if self.is_transaction_active():
            self.get_current_transaction().append(('SET', record_key, self.get_record(record_key)))
        self.database[record_key] = record_value
        self.meta_data[record_value] = self.meta_data.setdefault(record_value, 0) + 1
    
    def get_record(self, record_key):
        return self.database.get(record_key)
    
    def get_value_count(self, record_value):
        return self.meta_data.get(record_value, 0)

    def delete_record(self, record_key):
        if self.is_transaction_active():
            self.get_current_transaction().append(('DELETE', record_key, self.get_record(record_key)))
        if record_key in self.database:
            if self.meta_data[self.database[record_key]] > 0:
                self.meta_data[self.database[record_key]] -= 1
            else:
                del self.meta_data[self.database[record_key]]
            del self.database[record_key]
    
    def commit_transaction(self):
        if not self.is_transaction_active():
            print('NO TRANSACTION')
            return
        self.transaction_stack = []

    def rollback_transaction(self):
        if not self.is_transaction_active():
            print('NO TRANSACTION')
            return
        transaction = self.transaction_stack.pop()
        for op, record_key, record_value in reversed(transaction):
            if op == 'SET':
                self.set_record(record_key, record_value)
            elif op == 'DELETE':
                if record_value is not None:
                    self.set_record(record_key, record_value)
                else:
                    del self.database[record_key]
    
## Test
# db = InMemoryDatabase()
# db.set_record('x', 10)
# print(db.get_record('x'))
# db.delete_record('x')
# print(db.get_record('x'))

