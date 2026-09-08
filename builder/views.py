from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from datetime import timedelta
import re

from .models import Business, Website
from .forms import RegisterForm, LoginForm, BusinessForm
from .ai_service import generate_website_content


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome {user.username}! Your account has been created successfully.")
            return redirect('dashboard')
    else:
        form = RegisterForm()

    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


@login_required
def dashboard_view(request):
    businesses = Business.objects.filter(user=request.user).select_related('website')
    
    # Calculate stats
    total_sites = businesses.count()
    success_sites = businesses.filter(status='success').count()
    today = timezone.now().date()
    today_count = businesses.filter(created_at__date=today).count()
    remaining_today = max(0, 5 - today_count)

    context = {
        'businesses': businesses,
        'total_sites': total_sites,
        'success_sites': success_sites,
        'today_count': today_count,
        'remaining_today': remaining_today,
    }
    return render(request, 'website/dashboard.html', context)


@login_required
def add_business_view(request):
    today = timezone.now().date()
    today_count = Business.objects.filter(user=request.user, created_at__date=today).count()

    if today_count >= 5:
        messages.warning(request, "You have reached the daily limit of 5 AI website generations. Please try again tomorrow.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = BusinessForm(request.POST)
        if form.is_valid():
            business = form.save(commit=False)
            business.user = request.user
            business.status = 'generating'
            business.save()

            try:
                # Generate website via Gemini AI
                ai_result = generate_website_content(business)

                website = Website.objects.create(
                    business=business,
                    website_title=ai_result.get('title', business.name),
                    tagline=ai_result.get('tagline', ''),
                    about_section=ai_result.get('about', ''),
                    services=ai_result.get('services', []),
                    slug=ai_result.get('html', ''),
                    status='published'
                )

                business.status = 'success'
                business.save()

                messages.success(request, f"✨ Website for '{business.name}' generated successfully!")
                return redirect('view_website', id=website.id)

            except Exception as e:
                business.status = 'failed'
                business.save()
                messages.error(request, f"AI generation encountered an error: {str(e)}")
                return redirect('dashboard')
    else:
        form = BusinessForm()

    return render(request, 'website/add_business.html', {'form': form})


@login_required
def view_website(request, id):
    website = get_object_or_404(Website, id=id, business__user=request.user)
    return render(request, 'website/preview.html', {'website': website})


def raw_website(request, id):
    website = get_object_or_404(Website, id=id)
    return HttpResponse(website.slug, content_type='text/html')


@login_required
def download_website(request, id):
    website = get_object_or_404(Website, id=id, business__user=request.user)
    clean_title = re.sub(r'[^a-zA-Z0-9_\-]', '_', website.website_title.lower()).strip('_') or 'website'
    filename = f"{clean_title}.html"

    response = HttpResponse(website.slug, content_type='text/html; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


@login_required
def delete_business_view(request, id):
    business = get_object_or_404(Business, id=id, user=request.user)
    name = business.name
    business.delete()
    messages.success(request, f"Website for '{name}' was deleted.")
    return redirect('dashboard')
