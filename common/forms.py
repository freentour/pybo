from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class UserForm(UserCreationForm):
    """
    [팁] 일반적인 forms.ModelForm을 상속받지 않고 UserCreationForm을 상속받으면 좋은 이유
    - UserCreationForm은 BaseUserCreationForm을 상속 받았는데, BaseUserCreationForm과의 유일한 차이는 대소문자만 다른 username을 허용하지 않는다는 것. 이것 외에는 차이가 없음.
    - 그리고, BaseUserCreationForm은 django 4.2에서 새롭게 추가된 것으로, 새로운 user 객체를 생성하기 위한 ModelForm인데, username, password1, password2 이렇게 3개의 프로퍼티만 가짐. 이 폼에서는 자동으로 password1과 password2가 일치하는지, validate_password() 함수를 이용해 비밀번호가 유효한지, 그리고 set_password() 함수를 사용해서 user 객체의 password를 저장하는 기능을 수행함.
    """
    # UserCreationForm 클래스에 기본적으로 정의되어 있는 username, password1, password2 외에 추가로 폼에 표시할 프로퍼티를 정의
    # 이렇게 상속받은 클래스에 정의되어 있지 않은 프로퍼티들을 정의해 두어야 이 폼에서 기본적인 validation을 자동으로 수행해 줌. 추가로 정의하지 않으면 validation 수행하지 않음.
    # [참고] label 파라미터는 validation 수행 후 오류가 발생했을 때 오류 내용에 표시할 폼 필드 레이블이 무엇인지를 설정해 줌. label 파라미터를 명시하지 않으면 그냥 클래스 프로퍼티의 이름이 그대로 폼 필드의 레이블로 사용됨.
    email = forms.EmailField(label="이메일")
    first_name = forms.CharField(label="성")
    last_name = forms.CharField(label="이름")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileForm(forms.ModelForm):
    nickname = forms.CharField(label="닉네임")
    # is_teacher의 경우 template 파일에서 checkbox 타입으로 했더니 checked 상태는 값이 있는 것으로 인식하는 반면, unchecked 상태는 값을 입력하지 않은 것으로 인식함. 그래서, 아예 validation 수행하지 않는 것으로 설정함. (dafault 값을 False로 지정하기도 했고)
    # is_teacher = forms.BooleanField(label="교사 여부")

    class Meta:
        model = Profile
        fields = ['nickname', 'is_teacher']
