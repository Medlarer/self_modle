import copy
import re
class ValidError(Exception):
    def __init__(self,msg):
        self.msg = msg
class TextInput(object):

    def __str__(self):
        return "<input type='text'/>"

class EmailInput(object):

    def __str__(self):
        return "<input type='email'/>"

class Field(object):
    def __init__(self,required=True,error_message=None,widget=None):
        self.required = required
        self.error_msg = error_message
        if not widget:
            self.widget = TextInput()
        else:
            self.widget = widget

    def __str__(self):
        return str(self.widget)

class CharField(Field):
    def valid(self,val):
        if self.required:
            if not val:
                msg = self.error_msg.get('required')
                raise ValidError(msg)
            return val
class EmailField(Field):
    principle = '^\w+@\w+$'
    def valid(self,val):
        if self.required:
            if not val:
                msg = self.error_msg.get('required')
                raise ValidError(msg)
        succ=re.match(self.principle,val)
        if not succ:
            msg = self.error_msg.get('invalid','格式错误')
            raise ValidError(msg)
        return val
class Form(object):
    def __init__(self,data=None):
        # print(self.__class__.__dict__)
        self.fields = copy.deepcopy(self.__class__.fields)
        # print(self.fields)
        self.data = data
        self.errors = {}
        self.cleaned_data = {}

    def __new__(cls, *args, **kwargs):
        declare_field = {}
        # print(cls.__dict__)
        for field_name,field in cls.__dict__.items():
            if isinstance(field,Field):
                declare_field[field_name] = field
        cls.fields = declare_field
        return object.__new__(cls)

    def is_valid(self):
        for field_name,field in self.fields.items():
            try:
                val = self.data.get(field_name)
                ret_val=field.valid(val)
                value=getattr(self,'cleaned_%s'%field_name,None)
                if value:
                    ret_val = value(ret_val)
                self.cleaned_data[field_name] = ret_val
            except ValidError as e:
                self.errors[field_name] = e.msg
        return len(self.errors) == 0
    def __iter__(self):
        return iter(self.fields.values())
class UserForm(Form):
    # username = 'medlar'
    # email = 'medlar@163.com'
    username = CharField(error_message={'required':'默认不能为空'},widget=TextInput())
    email = EmailField(error_message={'required':'邮箱不能为空','invalid':'密码格式错误'},widget=EmailInput())
obj = UserForm(data={'username':'medlar','email':'medlar@163com'})
if obj.is_valid():
    print('验证成功',obj.cleaned_data)
else:
    print('验证失败',obj.errors)

for htm in obj:
    print(htm)