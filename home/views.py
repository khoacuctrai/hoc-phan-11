from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from .forms import CommentForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages




def home(request):
    posts = Post.objects.all().order_by('-created_at')  # Lấy bài viết mới nhất
    return render(request, 'index.html', {'posts': posts})



def product_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()  # Lấy tất cả bình luận của bài viết
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('product_detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'product_detail.html', {'post': post, 'comments': comments, 'form': form})


def register(request):
    if request.method == 'POST':
        # Tạo form từ dữ liệu người dùng nhập
        form = UserCreationForm(request.POST)

        if form.is_valid():
            # Lưu thông tin người dùng vào cơ sở dữ liệu
            user = form.save()

            # Đăng nhập người dùng ngay sau khi đăng ký
            login(request, user)

            # Hiển thị thông báo thành công
            messages.success(request, 'Đăng ký thành công! Chào mừng bạn đến với trang web.')

            # Chuyển hướng người dùng về trang chủ
            return redirect('home')
    else:
        # Nếu là GET request, hiển thị form trống
        form = UserCreationForm()

    # Trả về template với form
    return render(request, 'register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        # Tạo form từ dữ liệu người dùng nhập
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            # Lấy thông tin người dùng từ form
            user = form.get_user()

            # Đăng nhập người dùng
            login(request, user)

            # Hiển thị thông báo thành công
            messages.success(request, 'Đăng nhập thành công! Chào mừng bạn quay lại.')

            # Chuyển hướng đến trang chủ
            return redirect('home')
    else:
        # Nếu là GET request, hiển thị form trống
        form = AuthenticationForm()

    # Trả về template với form
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')