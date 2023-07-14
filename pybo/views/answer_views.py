from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..forms import AnswerForm
from ..models import Question, Answer


@login_required(login_url='account_login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()

            return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=question.id), answer.id))
    else:
        form = AnswerForm()

    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)


@login_required(login_url='account_login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)

    # [중요] 버튼 메뉴를 통하지 않고 urlpattern으로 직접 요청이 들어올 수도 있기 때문에 반드시 검사해야 함!
    if request.user != answer.author:
        # messages 모듈을 통한 에러 핸들링.
        # 템플릿에서 {% if messages %} 블럭으로 처리해야 함.
        messages.error(request, '본인이 작성한 답변만 수정할 수 있습니다')
        return redirect('pybo:detail', question_id=answer.question.id)
    else:
        if request.method == "POST":
            form = AnswerForm(request.POST, instance=answer)
            if form.is_valid():
                answer = form.save(commit=False)
                answer.author = request.user
                answer.modify_date = timezone.now()
                answer.save()
                return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=answer.question.id), answer.id))
        else:
            form = AnswerForm(instance=answer)

    context = {'form': form}
    return render(request, 'pybo/answer_form.html', context)


@login_required(login_url='account_login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)

    # [중요] 버튼 메뉴를 통하지 않고 urlpattern으로 직접 요청이 들어올 수도 있기 때문에 반드시 검사해야 함!
    if request.user != answer.author:
        # messages 모듈을 통한 에러 핸들링.
        # 템플릿에서 {% if messages %} 블럭으로 처리해야 함.
        messages.error(request, '본인이 작성한 답변만 삭제할 수 있습니다')
        return redirect('pybo:detail', question_id=answer.question.id)
    else:
        answer.delete()

    return redirect('pybo:detail', question_id=answer.question.id)


@login_required(login_url='account_login')
def answer_vote(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)

    if request.user == answer.author:
        # messages 모듈을 통한 에러 핸들링.
        # 템플릿에서 {% if messages %} 블럭으로 처리해야 함.
        messages.error(request, '본인이 작성한 답변은 추천할 수 없습니다')
        return redirect('pybo:detail', question_id=answer.question.id)
    else:
        # [참고] 그런데, 이렇게 비교하는건 추천자가 많은 경우에는 불필요한 오버로드가 발생함.
        if request.user in answer.voter.all():
            messages.error(request, '이미 추천한 답변입니다')
            return redirect('pybo:detail', question_id=answer.question.id)
        else:
            # [참고] 사실 다대다 관계에서 add 메소드는 이미 추가된 레코드를 또 추가하려고 해도 에러나 예외가 발생하지 않음. 따라서, 바로 앞의 if 문이 필요하지 않을 수 있지만, 여러 번 '추천' 버튼을 눌러도 숫자가 올라가지 않는 이유를 사용자에게 좀 더 분명한 메세지로 전달하기 위해 messages.error 함수를 사용함.
            answer.voter.add(request.user)

    return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=answer.question.id), answer.id))
