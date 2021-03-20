from django.urls import path
from .views import MyTicketList, TicketDetailView, CreateComment, AllTickets
from . import views

app_name = 'tickets'

urlpatterns = [
    # ticket views
    path('', views.department_list, name='department_list'),
    path('<slug:department_slug>', views.department_list, name='department_list_by_department'),
    path('<slug:department_slug>/<int:pk>/my_ticket_list', MyTicketList.as_view(), name='my_ticket_list'),
    path('all_tickets/', AllTickets.as_view(), name='all_tickets'),
    # path('<slug:department_slug>/<int:department_id>/create_ticket', CreateTicket.as_view(), name='create_ticket'),
    path('<slug:department_slug>/<int:department_id>/create_ticket', views.ticket_create, name='create_ticket'),
    path('<int:department_id>/<int:id>/ticket_detail', TicketDetailView.as_view(), name='ticket_detail'),
    # path('<int:department_id>/<int:id>/update_ticket', UpdateTicket.as_view(), name='update_ticket'),
    path('<int:department_id>/<int:id>/update_ticket', views.ticket_update, name='update_ticket'),
    path('ajax/load_subcategories/', views.load_subcategories, name='ajax_load_subcategories'),
    path('<int:id>/create_comment', CreateComment.as_view(), name='create_comment'),
]
