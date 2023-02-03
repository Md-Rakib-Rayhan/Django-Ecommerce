from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
urlpatterns = [
    # path('', views.home),

    path('', views.ProductView.as_view(), name='home'),

    path('searchresult/', views.search, name='search'),

    # path('product-detail/', views.product_detail, name='product-detail'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name ='product-detail'),

    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('removecart/', views.remove_cart, name='removecart'),


    path('cart_status/', views.cart_status, name='cart_status'),


    path('buy/<slug:data>', views.buy_now, name='buy-now'),

    path('profile/', views.ProfileView.as_view(), name='profile'),

    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),

    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
 
    path('laptop/', views.Laptop, name='laptop'),
    path('laptop/<slug:data>', views.Laptop, name='laptopdata'),

    path('TopWear/', views.TopWear, name='TopWear'),
    path('TopWear/<slug:data>', views.TopWear, name='TopWeardata'),

    path('BottomWear/', views.BottomWear, name='BottomWear'),
    path('BottomWear/<slug:data>', views.BottomWear, name='BottomWeardata'),

    # path('login/', views.login, name='login'),
    path('accounts/login/', auth_views.LoginView.as_view (template_name='app/login.html',authentication_form=LoginForm), name='login'),
    #       urls            ai login athantication use korbe        ai page a kaj korbe       ai login from display korbe karon aitate class deya hoise
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name="logout"),

#password change
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),
    
# password reset
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=MyPasswordResetForm), name='password_reset' ),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done' ),

    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm' ),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete' ),


    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

