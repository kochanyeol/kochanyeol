from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.urls import reverse_lazy

from .forms import CommentForm, TodoForm, TodoUpdateForm
from .models import Todo, Comment

class TodoListView(LoginRequiredMixin, ListView):
    model = Todo
    paginate_by = 10
    ordering = ['-created_at']
    template_name = 'todo/todo_list.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Todo.objects.all()
        else:
            queryset = Todo.objects.filter(user=self.request.user)

        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))
        return queryset.order_by('-created_at')

class TodoDetailView(LoginRequiredMixin, DetailView):
    template_name = 'todo/todo_info.html'
    queryset = Todo.objects.prefetch_related('comments', 'comments__user')

    def get_object(self, queryset=None):
        # prefetch_related: 댓글을 미리 한 번에 가져와서 DB 쿼리 횟수를 줄임
        todo = get_object_or_404(self.queryset, pk=self.kwargs['id'])
        if self.request.user.is_superuser or todo.user == self.request.user:
            return todo
        raise Http404

    # get_context_data(): 템플릿에 넘길 context(데이터 상자)를 구성하는 메서드
    # **kwargs: 장고가 내부적으로 넘기는 키워드 인자들을 받음
    # self.object - 장고가 정한 고정 변수명(DetailView가 가져온 todo 객체)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todo'] = self.object
        # 6일차 과제 수정 사항
        # 빈 댓글 입력 폼을(forms.py에 이미 만들어 둠) 템플릿에 넘겨서 사용자가 댓글 쓸 수 있게.
        context['comment_form'] = CommentForm()

        # prefetch_related: todo에 달린 댓글을 미리 한 번에 가져옴 (DB 쿼리 최적화)
        # filter로 매번 DB 조회하는 대신 이미 가져온 댓글을 재사용
        comments = self.object.comments.all()
        # 화면에 표시할 댓글 수 지정
        paginator = Paginator(comments, 10)
        # url에서 get할 때 page내용을 찾아옴
        page = self.request.GET.get('page')
        # get으로 찾아온 page에 댓글들을 템플릿에 넘김
        context['page_obj'] = paginator.get_page(page)
        return context

class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    form_class = TodoForm
    template_name = 'todo/todo_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('cbv_todo_detail', kwargs={'id': self.object.pk})

class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Todo
    form_class = TodoUpdateForm
    template_name = 'todo/todo_form.html'

    def get_object(self, queryset=None):
        todo = get_object_or_404(Todo, pk=self.kwargs['id'])
        if self.request.user.is_superuser or todo.user == self.request.user:
            return todo
        raise Http404

    def get_success_url(self):
        return reverse_lazy('cbv_todo_detail', kwargs={'id': self.object.pk})

class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo
    template_name = 'todo/todo_delete.html'

    def get_object(self, queryset=None):
        todo = get_object_or_404(Todo, pk=self.kwargs['id'])
        if self.request.user.is_superuser or todo.user == self.request.user:
            return todo
        raise Http404

    def get_success_url(self):
        return reverse_lazy('cbv_todo_list')

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['message']
    pk_url_kwarg = 'todo_id'

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.todo = get_object_or_404(Todo, pk=self.kwargs['todo_id'])
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('cbv_todo_detail', kwargs={'id': self.kwargs['todo_id']})

class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['message']
    template_name = 'todo/todo_info.html'

    def get_object(self, queryset=None):
        comment = get_object_or_404(Comment, pk=self.kwargs['id'])
        if self.request.user.is_superuser or comment.user == self.request.user:
            return comment
        raise Http404

    def get_success_url(self):
        return reverse_lazy('cbv_todo_detail', kwargs={'id': self.object.todo.pk})

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment

    def get_object(self, queryset=None):
        comment = get_object_or_404(Comment, pk=self.kwargs['id'])
        if self.request.user.is_superuser or comment.user == self.request.user:
            return comment
        raise Http404

    def get_success_url(self):
        return reverse_lazy('cbv_todo_list')