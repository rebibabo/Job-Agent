from database.connector import db_pool

class Entity:        
    def to_dict(self):
        return self.__dict__
    
    @classmethod
    def from_dict(cls, js):
        for key, value in js.items():
            setattr(cls, key, value)
        return cls
    
    def commit_to_db(self):
        key_value = getattr(self, self.key_name)
        result = db_pool.execute(f"SELECT * FROM {self.table_name} WHERE {self.key_name}='{key_value}'")
        if len(result) == 1:
            update_sql = f'UPDATE {self.table_name} SET '
            for key, value in self.__dict__.items():
                value = str(value).replace("'", "''")
                update_sql += f"{key}='{value}', "
            sql = update_sql[:-2] + f" WHERE {self.key_name}='{key_value}';"
            db_pool.execute(sql)
        else:
            insert_sql = f'INSERT INTO {self.table_name} ({", ".join(self.__dict__.keys())}) VALUES ('
            for value in self.__dict__.values():
                value = str(value).replace("'", "''")
                insert_sql += f"'{value}', "
            sql = insert_sql[:-2] + ');'
            db_pool.execute(sql)
    
    @classmethod
    def from_db(cls, id):
        result = db_pool.execute(f"SELECT * FROM {cls.table_name} WHERE {cls.key_name}='{id}'", return_dict=True)
        if len(result) == 1:
            return Entity.from_dict(result[0])
        else:
            return None
    
    def __str__(self):
        str = self.__class__.__name__ + ':\n'
        for attr in self.__dict__:
            str += f'{attr}: {self.__dict__[attr]}\n'
        return str + '\n'