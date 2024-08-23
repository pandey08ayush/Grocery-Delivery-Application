from django.urls import path
from django import views
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm,MyPasswordResetForm,MySetPasswordForm
urlpatterns = [
   
    path('home/', views.ProductView.as_view(),name='home'),
    path('product-detail/<int:pk>', views.ProductDetailsView.as_view(),name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name="show_cart"),
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('logout/', views.user_logout, name='logout'),

    path('minuscart/', views.minus_cart, name='minus_cart'),
    path('removecart/', views.remove_cart, name='remove_cart'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),  
    path('orders/', views.orders, name='orders'),
    path('flour/', views.flour, name='flour'),
    path('flour/<slug:data>', views.flour, name='flourdata'),
     path('oils-ghees/', views.Oils, name='Oils'),
    path('oils-ghees/<slug:data>', views.Oils, name='Oilsdata'),

     path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='payment_done'),

    path('tpwear/', views.topwear, name='tpwear'),
    path('tpwear/<slug:data>', views.topwear, name='tpweardata'),
    path('account/login/',auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm), name='login'),
    # path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='app/password_change.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/',auth_views.PasswordChangeView.as_view(template_name='app/password_change_done.html',form_class=MyPasswordChangeForm), name='passwordchangedone'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='app/password_reset.html', form_class= MyPasswordResetForm),name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_confirm.html',),name='password_reset_confirm'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name='password_reset_done'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='registration'),
   
    path('export-csv/', views.export_single_csv, name='export_single_csv'),
] + static(settings.MEDIA_URL,document_root=settings.
MEDIA_ROOT)
