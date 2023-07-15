from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Count

from ..models import Question

import logging
logger = logging.getLogger(__name__)


def index(request):
    logger.info("INFO 레벨로 출력")

    # GET 방식으로 들어온 page 변수의 값 저장.
    # 다음 코드에서 get() 함수의 두번째 파라미터로 사용된 '1'은 page 변수의 값이 지정되지 않았을 때의 DEFAULT 값을 의미함. (숫자 1이 아니고 문자 '1'인 것에 유의)
    page = request.GET.get('page', '1')     # 페이지 번호
    kw = request.GET.get('kw', '')          # 검색어
    so = request.GET.get('so', 'recent')          # 정렬기준
    per_page = 10   # 한 페이지 당 보여줄 게시물 수

    # 정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:
        question_list = Question.objects.order_by('-create_date')

    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()

    # 페이징 처리
    paginator = Paginator(question_list, per_page)
    page_obj = paginator.get_page(page)

    # 전체 페이지가 아니라 현재 페이지에 대한 Page 객체를 context 딕셔너리에 담아 템플릿으로 전달.
    # 이 때 Query Set을 전달하려면 page_obj.object_list를 전달하는 것이 맞지만, 템플릿에서 페이징 처리를 손 쉽게 하기 위해 Page 객체 자체의 프로퍼티와 메소드를 사용할 것이기 때문에 Query Set이 아니라 Page 객체를 전달해야 하는 것에 유의.
    # 즉, context = {'question_list': page_obj.object_list} 이렇게 하면 안됨!
    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so': so}
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)
