from authentication import views
from django.urls import path

urlpatterns = [

    # * user managment [Admin permission]
    path('admin/users/', views.AllUser.as_view()),
    path('admin/users/<str:id>/', views.GetUser.as_view()),

    # ! type can be { company , employee }
    path('register/<str:type>/', views.Register.as_view()),

    # ! type can be { admin , company , employee }
    path('login/username/<str:type>/', views.Login.as_view()),
    path('my_info/<str:type>/', views.MyInfo.as_view()),
    path('my_info/update/<str:type>/', views.MyInfoUpdate.as_view()),
    path('logout/<str:type>/', views.Logout.as_view()),
    path('delete_my_account/', views.DeleteAccount.as_view()),

    path('update-token/', views.UpdateToken.as_view()),

]
