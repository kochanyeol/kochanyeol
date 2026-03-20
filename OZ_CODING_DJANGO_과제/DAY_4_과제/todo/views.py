from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Todo
from .forms import TodoForm, TodoUpdateForm
from django.db.models import Q

@login_required
def todo_list(request):
    q = request.GET.get('q', '')
    todos = Todo.objects.filter(user=request.user)
    if q:
        todos = todos.filter(Q(title__icontains=q) | Q(description__icontains=q))
    paginator = Paginator(todos, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'todo/todo_list.html', context)

@login_required  # 로그인 안 된 유저는 로그인 페이지로 자동 redirect(django 기능)
def todo_info(request, pk):
    # url에서 넘어온 todo_id로 Todo 객체를 가져오고 없으면 404 반환
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    context = {
        # todo 객체의 필드들을 딕셔너리 형태로 변환해서 전달
        'todo': todo.__dict__
    }
    # todo_info.html 템플릿을 렌더링하고 context 전달
    return render(request, 'todo/todo_info.html', context)

@login_required  # 로그인 안 된 유저는 로그인 페이지로 자동 redirect
def todo_create(request):
    if request.method == 'POST':
        # 사용자가 입력한 데이터를 폼에 담기
        form = TodoForm(request.POST)
        if form.is_valid():  # 입력값이 유효한지 검사
            todo = form.save(commit=False)  # DB 저장 전 Todo 객체만 생성 (아직 user 없음)
            todo.user = request.user  # 로그인한 유저를 Todo 객체에 추가
            todo.save()  # user까지 채운 Todo 객체를 DB에 최종 저장
            return redirect('todo_info', pk=todo.pk)  # 생성된 Todo 상세 페이지로 이동
    else:
        # GET 요청 시 빈 폼을 렌더링
        form = TodoForm()
    return render(request, 'todo/todo_create.html', {'form': form})

@login_required  # 로그인 안 된 유저는 로그인 페이지로 자동 redirect
def todo_update(request, pk):
    # pk와 로그인한 유저가 일치하는 Todo 가져오기 (없으면 404 반환)
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if request.method == 'POST':
        # 수정된 데이터를 기존 Todo 객체(instance)에 덮어씌우기
        form = TodoUpdateForm(request.POST, instance=todo)
        if form.is_valid():  # 입력값이 유효한지 검사
            form.save()  # 수정된 Todo를 DB에 저장 (user는 이미 있으므로 commit=False 불필요)
            return redirect('todo_info', pk=todo.pk)  # 수정된 Todo 상세 페이지로 이동
    else:
        # GET 요청 시 기존 데이터가 채워진 폼을 렌더링
        form = TodoUpdateForm(instance=todo)
    return render(request, 'todo/todo_update.html', {'form': form})

@login_required  # 로그인 안 된 유저는 로그인 페이지로 자동 redirect
def todo_delete(request, pk):
    # pk와 로그인한 유저가 일치하는 Todo 가져오기 (없으면 404 반환)
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    todo.delete()  # Todo를 DB에서 삭제
    return redirect('todo_list')  # 삭제 후 목록 페이지로 이동