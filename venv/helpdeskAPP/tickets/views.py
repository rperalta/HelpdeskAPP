from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from .models import Department, Ticket, Category, Subcategory, Comment
from django.template.loader import render_to_string
from datetime import datetime

from .forms import TicketForm, UpdateTicketForm, CommentForm


# Create your views here.
def department_list(request, department_slug=None):
    department = None
    departments = Department.objects.all()
    if department_slug:
        department = get_object_or_404(Department, slug=department_slug)

    return render(request, 'tickets/department/index.html',
                  {'department': department, 'departments': departments})


class MyTicketList(ListView):
    template_name = 'tickets/department/my_ticket_list.html'
    context_object_name = 'department_tickets'

    def get_queryset(self):
        queryset = {'tickets': Ticket.objects.filter(assigned_to=self.request.user, department_id=self.kwargs['pk']),
                    'department': Department.objects.all().filter(id=self.kwargs['pk'])}
        return queryset


class AllTickets(ListView):
    template_name = 'tickets/department/all_tickets.html'
    context_object_name = 'all_tickets'
    # queryset = Department.objects.all().prefetch_related('ticket_set')

    def get_queryset(self):
        all_data = []
        departments = Department.objects.all()
        tickets = Ticket.objects.all().filter(assigned_to=self.request.user)
        for department in departments:
            department_object = {}
            ticket_object = [tickets.filter(department_id=department)]
            department_object['department'] = department
            department_object['ticket'] = ticket_object
            all_data.append(department_object)

        queryset = {'all_data': all_data}
        return queryset


# class CreateTicket(CreateView):
#     template_name = 'tickets/department/submit_ticket.html'
#     form_class = TicketForm
#     queryset = Ticket.objects.all()
#
#     def get_form_kwargs(self):
#         kwargs = super(CreateTicket, self).get_form_kwargs()
#         kwargs.update(self.kwargs)
#         return kwargs
#
#     def dispatch(self, request, *args, **kwargs):
#         self.department_id = get_object_or_404(Department, pk=kwargs['department_id'])
#         return super().dispatch(request, *args, **kwargs)
#
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         form.instance.department_id = self.department_id
#         form.instance.custom_id = Ticket.objects.filter(department_id=form.instance.department_id).count() + 1
#         return super(CreateTicket, self).form_valid(form)
#
#     def get_success_url(self, **kwargs):
#         return 'my_ticket_list'

def save_ticket_form(request, form, template_name, department_id, user, custom_id):
    data = dict()
    department = get_object_or_404(Department, id=department_id)
    if request.method == 'POST':
        if form.is_valid():
            new_instance = form.save(commit=False)
            new_instance.department_id_id = department_id
            new_instance.author = user
            new_instance.custom_id = custom_id
            new_instance.created = datetime.now()
            new_instance.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    context = {'form': form, 'department': department}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def ticket_create(request, department_slug, department_id):
    user = request.user
    custom_id = Ticket.objects.filter(department_id=department_id).count() + 1
    print(custom_id)
    if request.method == 'POST':
        form = TicketForm(request.POST, department_id=department_id, initial={'department_id': department_id, 'author': user, 'custom_id': custom_id})
    else:
        form = TicketForm(department_id=department_id, initial={'department_id': department_id, 'author': user, 'custom_id': custom_id})
    return save_ticket_form(request, form, 'tickets/department/submit_ticket.html', department_id, user, custom_id)


class TicketDetailView(DetailView):
    model = Ticket
    template_name = 'tickets/department/ticket_details.html'
    # queryset = Ticket.objects.all()

    # def get_queryset(self):
    #     queryset = {'tickets': Ticket.objects.filter(assigned_to=self.request.user, department_id=self.kwargs['id']),
    #                 'department': Department.objects.all().filter(id=self.kwargs['department_id'])}
    #     return queryset

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        department = Department.objects.filter(id=self.kwargs['department_id'])
        comments = Comment.objects.filter(ticket_id=self.kwargs['id'])
        data['comments'] = comments
        data['comment_form'] = CommentForm()
        data['department'] = department

        return data

    def post(self, request, *args, **kwargs):
        new_comment = Comment(body=request.POST.get('body'),
                              user_comment=self.request.user,
                              ticket_id=self.get_object())
        new_comment.save()

        return self.get(self, request, *args, **kwargs)

    def get_object(self):
        id_ = self.kwargs.get('id')
        department_id = self.kwargs.get('department_id')
        return get_object_or_404(Ticket, department_id=department_id, id=id_)


class UpdateTicket(UpdateView):
    template_name = 'tickets/department/update_ticket.html'
    form_class = UpdateTicketForm
    # queryset = Ticket.objects.all()

    def get_form_kwargs(self):
        kwargs = super(UpdateTicket, self).get_form_kwargs()
        kwargs.update(self.kwargs)
        return kwargs

    def get_object(self):
        id_ = self.kwargs.get('id')
        department_id = self.kwargs.get('department_id')
        return get_object_or_404(Ticket, department_id=department_id, id=id_)

    def dispatch(self, request, *args, **kwargs):
        self.department_id = get_object_or_404(Department, pk=kwargs['department_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.department_id = self.department_id
        return super(UpdateTicket, self).form_valid(form)

    def get_success_url(self):
        return 'ticket_detail'


def load_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(category_id=category_id).order_by('subcategory_name')
    return render(request, 'tickets/department/subcategory_dropdown.html', {'subcategories': subcategories})


class CreateComment(CreateView):
    template_name = 'tickets/department/submit_comment.html'
    form_class = CommentForm
    queryset = Comment.objects.all()

    def form_valid(self, form):
        form.instance.ticket_id = Ticket.objects.get(id=self.kwargs.get('id'))
        form.instance.user_comment = self.request.user
        return super(CreateComment, self).form_valid(form)

    def get_success_url(self, **kwargs):
        return 'ticket_detail'

# class TransferTicket(CreateView):
#     template