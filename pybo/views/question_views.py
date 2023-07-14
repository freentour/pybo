from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question


@login_required(login_url='account_login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()

            return redirect('pybo:index')
    else:
        form = QuestionForm()

    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='account_login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    # [중요] 버튼 메뉴를 통하지 않고 urlpattern으로 직접 요청이 들어올 수도 있기 때문에 반드시 검사해야 함!
    if request.user != question.author:
        # messages 모듈을 통한 에러 핸들링.
        # 템플릿에서 {% if messages %} 블럭으로 처리해야 함.
        messages.error(request, '본인이 작성한 질문만 수정할 수 있습니다')
        return redirect('pybo:detail', question_id=question.id)
    else:
        if request.method == "POST":
            form = QuestionForm(request.POST, instance=question)
            if form.is_valid():
                question = form.save(commit=False)
                question.author = request.user
                question.modify_date = timezone.now()
                question.save()
                return redirect('pybo:detail', question_id=question.id)
        else:
            form = QuestionForm(instance=question)

    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='account_login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    # [중요] 버튼 메뉴를 통하지 않고 urlpattern으로 직접 요청이 들어올 수도 있기 때문에 반드시 검사해야 함!
    if request.user != question.author:
        # messages 모듈을 통한 에러 핸들링.
        # 템플릿에서 {% if messages %} 블럭으로 처리해야 함.
        messages.error(request, '본인이 작성한 질문만 삭제할 수 있습니다')
        return redirect('pybo:detail', question_id=question.id)
    else:
        question.delete()

    return redirect('pybo:index')


@login_required(login_url='account_login')
def question_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.user == question.author:
        # messages 모듈을 통한 에러 핸들링.
        # 템플릿에서 {% if messages %} 블럭으로 처리해야 함.
        messages.error(request, '본인이 작성한 질문은 추천할 수 없습니다')
    else:
        # [참고] 그런데, 이렇게 비교하는건 추천자가 많은 경우에는 불필요한 오버로드가 발생함.
        if request.user in question.voter.all():
            messages.error(request, '이미 추천한 질문입니다')
        else:
            # [참고] 사실 다대다 관계에서 add 메소드는 이미 추가된 레코드를 또 추가하려고 해도 에러나 예외가 발생하지 않음. 따라서, 바로 앞의 if 문이 필요하지 않을 수 있지만, 여러 번 '추천' 버튼을 눌러도 숫자가 올라가지 않는 이유를 사용자에게 좀 더 분명한 메세지로 전달하기 위해 messages.error 함수를 사용함.
            question.voter.add(request.user)

    return redirect('pybo:detail', question_id=question.id)
