from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.urls import reverse_lazy
from .models import Todo

# view는 urls를 통해 사용자의 요청을 받아서 model에게 db를 가져오라고 명령을한다.
# 그리고서 model에게 db를 꺼내온것을 넘겨 받는다
# FBV는 함수 하나가 요청을 받아서 처리하기에 반복횟수가 많다. - 로직이 단순하고, 커스텀을 할 때나 빠르게 제작할 때 쓰임
# CBV는 클래가 요청을 받아서 처리 HTTP를 자동 분기해준다. - 반복되는 로직이 많을 때, 여러 뷰의 같은 장고 기능을 쓰고 싶을 때

# FBV에서의 @login_required데코랑 같은 역할
# CBV는 함수가 아니라 클래스여서 데코를 바로 사용하지 못한다. 그래서 LoginRequiredMixin을 상속받아서 사용
# LoginRequiredMixin 로그인 확인 여부를 판단해주는 기능
# PermissionRequiredMixin 특정 권한 여부를 판단해주는 기능
# UserPassesTestMixin 개발자가 직접 권한 조건을 작성
# ListView는 장고가 목록 조회에 필요한 것들을 미리 만들어 놓은 클래스
    # 자동처리 -DB에서 데이터가져오기, 페이지네이션(몇페이지까지 설정)처리, 템플릿에 테이터 넘기기
# FBV에서 직접 비즈니스 로직을 작성해서 하나하나 구현했지만 CBV에서는 장고의 프레임워크를 통해 쉽게 작업 가능
# 여기서 그냥 View를 쓰게되면 직접 모든걸 구현해야해서 구현 되어있는 ListView를 사용
class TodoListView(LoginRequiredMixin, ListView):
    model = Todo
    paginate_by = 10
    ordering = ['-created_at']
    template_name = 'todo/todo_list.html'

    def get_queryset(self):
        # 만약 모든걸 관리하는 관리자가 아닌 직원이 접근을 할 경우로 설정할 경우 is_staff으로 설정한다.
        if self.request.user.is_superuser:
            # Todo.objects는 객체를 가져오는 방식이 많지만 지문에 전체 가져오기에 all() 사용
            queryset = Todo.objects.all()
        else:
            # 여기서는 지문에서 접근이 관리자가 아닌 일반 유저일경우 본인의 Todo만 가져오게 설계
            # filter(user=self.request.user, id=pk)방식으로 특정하나만 가져오기도 가능
            queryset = Todo.objects.filter(user=self.request.user)
        # q는 사용자의 입력값으로 객체를 가져오기 위해 get요청으로 받아온다
        q = self.request.GET.get('q')
        if q:
            # 사용자 검색어를 작성할 때 이것이 제목에 있을 수도 있고 내용에 있을 수도 있어서 둘중 한 곳에라도
            # 있는것을 가져오기위해 |를 사용해 or을 줘서 둘 중 하나라도 해당하면 가져오게끔 설계
            # 거기에 맞는 검색어에 해당하는 객체를 가져오기위해 __icontains를 사용해서 텍스트 검색을 한다.
            queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))
        return queryset

# DetailView: 특정 todo 하나의 상세 페이지를 보여주는 CBV
# 장고가 자동으로 해주는 것: URL의 pk로 todo 가져오기, 템플릿에 context 넘기기
class TodoDetailView(LoginRequiredMixin, DetailView):
    model = Todo
    template_name = 'todo/todo_info.html'

    # get_object(): URL의 pk에 해당하는 todo를 가져오고 권한을 검증하는 메서드
    # 장고가 자동으로 호출하고, 결과를 self.object에 저장해둠
    def get_object(self, queryset=...):
        # URL의 pk로 todo를 가져옴. 없으면 자동으로 404 반환
        todo = get_object_or_404(Todo, pk=self.kwargs['id'])
        # 관리자이거나 본인의 todo면 반환, 아니면 404
        if self.request.user.is_superuser or todo.user == self.request.user:
            return todo
        raise Http404

    # get_context_data(): 템플릿에 넘길 context(데이터 상자)를 구성하는 메서드
    # **kwargs: 장고가 내부적으로 넘기는 키워드 인자들을 받음
    def get_context_data(self, **kwargs):
        # super().get_context_data(**kwargs): 부모 클래스(DetailView)가 자동으로 만들어주는
        # context를 가져옴. 안에는 {'object': todo객체, 'todo': todo객체, 'view': ...} 가 있음
        context = super().get_context_data(**kwargs)
        # context['todo']: 장고가 자동으로 넣어준 todo객체를 __dict__로 변환해서 덮어씀
        # __dict__: 객체의 모든 필드를 딕셔너리로 변환 {'id':1, 'title':'공부', ...}
        # 결과적으로 context 안에 딕셔너리 안에 딕셔너리가 담김
        context['todo'] = self.get_object().__dict__
        return context

class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    fields = ['title', 'description', 'start_date', 'end_date']
    template_name = 'todo/todo_create.html'

    def form_valid(self, form):
        todo = form.save(commit=False)
        todo.user = self.request.user
        todo.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('cbv_todo_detail', kwargs={'pk': self.object.pk})

class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Todo
    fields = ['title', 'description', 'start_date', 'end_date']
    template_name = 'todo/todo_update.html'

    def get_object(self, queryset = ...):
        todo = get_object_or_404(Todo, pk=self.kwargs['id'])
        if self.request.user.is_superuser or todo.user == self.request.user:
            return todo
        raise Http404

    def get_success_url(self):
        return reverse_lazy('cbv_todo_detail', kwargs={'pk':self.object.pk})

class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo
    template_name = 'todo/todo_delete.html'

    def get_object(self, queryset = ...):
        todo = get_object_or_404(Todo, pk=self.kwargs['id'])
        if self.request.user.is_superuser or todo.user == self.request.user:
            return todo
        raise Http404

    def get_success_url(self):
        return reverse_lazy('cbv_todo_list')