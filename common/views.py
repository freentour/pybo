from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import UserForm, ProfileForm


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():
            # form.save()에서 바로 user 객체가 생성이 되고 해당 내용은 데이터베이스에도 바로 반영됨.
            user = form.save()

            """
            [중요] 
            profile_form의 경우에는 profile 객체는 바로 생성해야 하지만, 해당 객체의 user 프로퍼티를 통해 user 객체와 연결해야 하기 때문에, 데이터베이스 반영은 나중에 하기 위해 commit=False 를 지정한 것임. (1:1 관계나 1:다 관계에서는 항상 이와 같이 처리해야 함)
            """
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()  # 이 때 다시 실제적으로 데이터베이스에 반영됨.

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            # 회원 가입하는 상황이라 다음 비교 문장이 거의 필요 없겠지만, 원래는 다음처럼 에러 핸들링 문장을 작성해 줘야 함.
            # 만약 인증에 실패하면 authenticate 함수는 None을 리턴함.
            if user is not None:
                login(request, user)
                return redirect('index')
    else:   # GET 요청이면
        form = UserForm()
        profile_form = ProfileForm()

    context = {'form': form, 'profile_form': profile_form}
    return render(request, 'common/signup.html', context)
