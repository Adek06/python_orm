class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        if name=="Model":
            return type.__new__(cls, name, bases, attrs)
        mappings = dict()
        for k, v in attrs.items():
            if isinstance(v, Field):
                mappings[k] = ""
            if isinstance(v, KeyField):
                key_field=k
        # print("this is attrs:{}".format(attrs))
        # print("this is mappings:{}".format(mappings))
        for k in mappings.keys():
            attrs.pop(k)
        attrs["__mappings__"] = mappings
        attrs["__table_name__"] = name
        attrs["__key_field__"] = key_field
        return type.__new__(cls, name, bases, attrs)

class Model(dict, metaclass=ModelMeta):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def insert(self):
        field=[]
        values=[]
        question_mark=[]
        # print(self.__mappings__)
        for k,v in self.__mappings__.items():
            field.append(k)
            values.append(getattr(self,k))
            question_mark.append("?")
        # print(field)
        # print(str(values))
        print("insert into {} ({}) values ({});".format(self.__table_name__, ",".join(field),",".join(question_mark)))

    def delete(self):
        k = self.__key_field__
        print("delete from {} where {}={};".format(self.__table_name__,k,getattr(self,k)))

    def update(self):
        pass

class Field():
    pass
class StringField(Field):
    pass
class IntField(Field):
    pass
class KeyField(Field):
    pass

class User(Model):
    name = KeyField()
    age = IntField()

    
u = User(name="test",age=10)
u.insert()
u.delete()

