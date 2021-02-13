from django.forms import ModelForm, ModelChoiceField
from django import forms
from tickets.models import Department, Ticket, Category, Subcategory, Comment


class TicketForm(forms.ModelForm):
    #category_id = ModelChoiceField(queryset=Category.objects.none())
    class Meta:
        model = Ticket
        fields = ['category_id', 'subcategory_id', 'status', 'priority', 'title', 'assigned_to', 'body']
        exclude = ['department_id', 'slug', 'author', 'custom_id']

    def __init__(self, *args, **kwargs):
        # print(kwargs)
        department_slug = kwargs.pop('department_slug')
        department_id = kwargs.pop('department_id')
        super(TicketForm, self).__init__(*args, **kwargs)
        self.fields['category_id'].queryset = Category.objects.all().filter(department_id=department_id)
        self.fields['subcategory_id'].queryset = Subcategory.objects.none()

        if 'category_id' in self.data:
            try:
                category_id = int(self.data.get('category_id'))
                self.fields['subcategory_id'].queryset = Subcategory.objects.filter(category_id=category_id).order_by('subcategory_name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            print(self.instance.pk)
            self.fields['subcategory_id'].queryset = self.instance.department.subcategory_set.order_by('subcategory_name')


class UpdateTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'
        exclude = ['department_id', 'custom_id', 'slug', 'author']

    def __init__(self, *args, **kwargs):
        # department_slug = kwargs.pop('department_slug')
        # department_id = 1
        department_id = kwargs.pop('department_id')
        ticket_id = kwargs.pop('id')
        # custom_id = kwargs.pop('custom_id')
        super(UpdateTicketForm, self).__init__(*args, **kwargs)
        self.fields['category_id'].queryset = Category.objects.all().filter(department_id=department_id)
        self.fields['subcategory_id'].queryset = Subcategory.objects.none()

        if 'category_id' in self.data:
            print(self.data)
            try:
                category_id = int(self.data.get('category_id'))
                self.fields['subcategory_id'].queryset = Subcategory.objects.filter(category_id=category_id).order_by(
                    'subcategory_name')
            except (ValueError, TypeError):
                pass
        # elif self.instance.pk:
        #     print(self.instance.pk)
        #     self.fields['subcategory_id'].queryset = self.instance.department.subcategory_set.order_by(
        #         'subcategory_name')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
