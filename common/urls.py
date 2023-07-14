from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# URL 별칭이 여러 앱들끼리 중복되는 것을 방지하기 위해 URL 네임스페이스 지정
# URL 별칭: urlpatterns 내부에 사용한 name='index', name='detail' 부분을 URL 별칭이라고 함.
app_name = 'common'

urlpatterns = [
    # django.contrib.auth 앱의 LoginView 클래스를 활용했으므로 별도의 views.py 파일의 수정은 필요 없음!
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
]
