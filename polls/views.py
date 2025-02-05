from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # 체크박스의 name에 맞춰 'choices'로 값을 받아옴
    selected_choices_ids = request.POST.getlist("choices")

    if not selected_choices_ids:
        # 아무것도 선택하지 않았을 경우 에러 메시지와 함께 폼 다시 렌더링
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "하나 이상의 선택지를 선택해주세요.",
        })

    # 선택된 모든 초이스에 대해 투표수를 업데이트
    for choice_id in selected_choices_ids:
        try:
            selected_choice = question.choice_set.get(pk=choice_id)
        except Choice.DoesNotExist:
            # 선택지 중 유효하지 않은 경우 에러 처리
            continue  # 혹은 다른 처리를 할 수 있음
        selected_choice.votes = F("votes") + 1
        selected_choice.save()

    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))