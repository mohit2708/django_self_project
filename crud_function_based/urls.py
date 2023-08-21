from django.urls import path
from . import views

urlpatterns = [
    path('', views.list, name="list"),
    path('add/', views.create, name="create"),
    path('store/', views.store, name="store"),
    path('edit/<int:id>', views.show, name="show"),
    # path('update/<int:id>', views.update, name='update'),
    # path('delete/<int:id>', views.destroy, name='delete'),
]