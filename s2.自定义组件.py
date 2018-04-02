import copy,re
class ValidError(Exception):
    #自定义错误提示
    def __init__(self,msg):
        self.msg = msg
class TextInput(object):
    #在前端返回input标签
    def __str__(self):
        return "<input type='text'/>"
class EmailInput(object):
    def __str__(self):
        return "<input type='email'/>"
class Field(object):
    #基类 所有的XXField都继承这个类
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
    # 根据数据格式自定义验证方法如带有邮箱格式的数据验证
    def valid(self,obj):
        if self.required:
            if not obj:
                error_msg = self.error_msg.get("required")
                raise ValidError(error_msg)
        return obj

class EmailField(Field):
    rule = "^\w+@\w+$"
    def valid(self,obj):
        if self.required:
            if not obj:
                error_msg = self.error_msg.get("required")
                raise ValidError(error_msg)
            ret = re.match(self.rule,obj)
            if not ret:
                error_msg = self.error_msg.get("invalid","格式错误")
                raise ValidError(error_msg)
        return obj
class Form(object):
    #所有XXForm的基类
    def __init__(self,data=None):
        self.data = data
        self.fields = copy.deepcopy(self.__class__.fields)
        self.errors = {}
        self.cleaned_data = {}

    def __new__(cls, *args, **kwargs):
        declare_fields = {}
        for field_name,field in cls.__dict__.items():
            #得到某个XXForm的所有的.__class__,如{"username":CharField()}
            if isinstance(field,Field):
                declare_fields[field_name] = field
        cls.fields = declare_fields
        return object.__new__(cls)

    def is_valid(self):
        #验证规则
        for field_name,field in self.fields.items():
            #得到实例化的字段名称和XXField对象 如{"username":CharField()}
            try:
                value = self.data.get(field_name)
                ret = field.valid(value)
                val = getattr(self,"cleaned_%s"%field_name,None)
                if val:
                    ret = val(ret)
                self.cleaned_data[field_name] = ret
            except ValidError as e:
                self.errors[field_name] = e.msg
        return len(self.errors) == 0
    def __iter__(self):
        return iter(self.fields.values())
class UserForm(Form):
    username = CharField(error_message={"required":"默认不能为空"},widget=TextInput())
    email = EmailField(error_message={"required":"邮箱不能为空","invalid":"邮箱格式错误"},widget=EmailInput())

user_obj = UserForm(data={"username":"medlar","email":"medlar@163com"})
if user_obj.is_valid():
    print("验证成功",user_obj.cleaned_data)
else:
    print("验证失败",user_obj.errors)

for i in user_obj:
    print(i)