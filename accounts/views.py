from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login
from orders.models import Order
from store.models import Review, Subscription, Product
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создание нового пользователя
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            # Аутентификация пользователя
            user = authenticate(username=new_user.username, password=user_form.cleaned_data['password'])
            login(request, user)
            return redirect('accounts:profile')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'user_form': user_form})

@login_required
def profile(request):
    notifications = request.user.notifications.filter(read=False)
    orders = Order.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)
    subscriptions = Subscription.objects.filter(user=request.user)
    subscribed_products = Product.objects.filter(subscriptions__user=request.user)
    return render(request, 'accounts/profile.html', {
        'notifications': notifications,
        'orders': orders,
        'reviews': reviews,
        'subscriptions': subscriptions,
        'subscribed_products': subscribed_products,
    })