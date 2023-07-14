from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    # inline 모드에서 inline 객체만 별도로 삭제할 수 있는지 여부를 결정. False로 설정되었기 때문에 admin 페이지에서 profile 객체만 별도로 삭제할 수는 없고, user 객체가 삭제될 때 같이 삭제되는 방법 밖에 없게 됨. (기본값은 True)
    can_delete = False
    # object에 대한 human-readable한 이름. 명시하지 않으면 클래스 이름의 munged version을 사용.
    # (예) CamelCase --> 'camel case'
    verbose_name = 'profile'
    # verbose_name에 대한 복수형 이름. 명시하지 않으면 verbose_name 뒤에 's'를 붙인 이름이 사용됨.
    # (예) verbose_name이 'story'인 경우 명시하지 않으면 그냥 'storys'가 됨. 따라서, 이런 경우에 verbose_name_plural = 'stories' 라고 명시해 주기 위해 사용함.
    verbose_name_plural = 'profile'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
