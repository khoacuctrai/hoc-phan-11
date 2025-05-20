from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    tags = models.CharField(max_length=100, blank=True)
    img = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)

    likes = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)

    # 👎 THÊM FIELD NÀY
    dislikes = models.ManyToManyField(User, related_name='disliked_posts', blank=True)

    def __str__(self):
        return self.title

    def is_in_stock(self):
        return self.stock > 0

    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    tags = models.CharField(max_length=100, blank=True)
    img = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 👍 Thông tin mua sắm
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stock = models.PositiveIntegerField(default=0)  # Số lượng hàng tồn
    is_available = models.BooleanField(default=True)

    # ❤️ Tương tác
    likes = models.PositiveIntegerField(default=0)
    
    # 👁️ Thêm lượt xem (fix bug ở view)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def is_in_stock(self):
        return self.stock > 0


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # ❤️ Người dùng thích bình luận
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.post}"

    def total_likes(self):
        return self.likes.count()


# models.py

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.quantity * self.post.price

    def __str__(self):
        return f"{self.post.title} x {self.quantity}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def total_price(self):
        return sum(item.subtotal() for item in self.items.all())

    def __str__(self):
        return f"Order #{self.id} by {self.user}"
