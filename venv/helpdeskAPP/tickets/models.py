from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class Department(models.Model):
    department_name = models.CharField(max_length=50, db_index=True)
    department_image = models.ImageField(upload_to='department/%Y/%m/%d', blank=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('department_name',)
        verbose_name = 'department'
        verbose_name_plural = 'departments'

    def __str__(self):
        return self.department_name

    def get_absolute_url(self):
        return reverse('tickets:department_list_by_department', args=[self.slug])


class Category(models.Model):
    category_name = models.CharField(max_length=50, default="Other")
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name


class Subcategory(models.Model):
    subcategory_name = models.CharField(max_length=50, default="Other")
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'subcategories'

    def __str__(self):
        return self.subcategory_name


class Ticket(models.Model):
    STATUS_CHOICES = (
        ('N', 'New'),
        ('O', 'Open'),
        ('OH', 'On Hold'),
        ('S', 'Solved'),
        ('C', 'Closed'),
    )
    PRIORITY_CHOICES = (
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),
        ('C', 'Critical'),
    )
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    subcategory_id = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    custom_id = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='N')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='L')
    title = models.CharField(max_length=250)
    author = models.ForeignKey(User, related_name='%(class)s_requests_created', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    due_date = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tickets:ticket_detail', kwargs={'id': self.id})


class SharedUsers(models.Model):
    shared_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket_id = models.ForeignKey(Ticket, on_delete=models.CASCADE)

    def __str__(self):
        return self.shared_user_id


class Comment(models.Model):
    ticket_id = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    body = models.TextField()
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body


class Solution(models.Model):
    ticket_id = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body

