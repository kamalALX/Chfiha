# main/views.py
from django.views.generic import ListView, DetailView, TemplateView, FormView
from .models import Project, Service, Categorie
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm

from django.http import JsonResponse
from django.views import View
from django.template.loader import render_to_string


class AboutPageView(TemplateView):
    template_name = 'about.html'

class BookingPageView(TemplateView):
    template_name = 'booking.html'

class SuccessPageView(TemplateView):
    template_name = 'success.html'

class ContactPageView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/success/'  # URL to redirect to after successful form submission

    def form_valid(self, form):
        # Get form data
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        msg = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        
        # Send email
        send_mail(
            f'Message from {name}',  # Subject
            msg,  # Message
            settings.DEFAULT_TO_EMAIL,  # From email
            [settings.DEFAULT_TO_EMAIL],  # To email
            fail_silently=False,
        )
        return super().form_valid(form)

class HomePageView(ListView):
    model = Service
    template_name = 'home.html'
    context_object_name = 'services'

class MessagesPageView(ListView):
    model = Service
    template_name = 'messages.html'
    context_object_name = 'all_messages_list'

class ServiceDetailView(DetailView):
    model = Service
    template_name = 'service.html'
    context_object_name = 'service'

class ServicesView(ListView):
    model = Service
    template_name = 'services.html'
    context_object_name = 'services'

    # """
    #     overriding the get_queryset method to filter the results based on the search query.
    # """
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     query = self.request.GET.get('q')
    #     category_id = self.request.GET.get('category')

    #     if query:
    #         queryset = queryset.filter(title__icontains=query)  # Modify based on your filtering logic
    #     if category_id:
    #         queryset = queryset.filter(categorie_id=category_id)

    #     return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Categorie.objects.all()
        return context
    

class FilterServicesView(View):
    def get(self, request):
        category_id = request.GET.get('category')
        query = request.GET.get('q')

        services = Service.objects.all()
        if category_id:
            services = services.filter(categorie_id=category_id)
        if query:
            services = services.filter(title__icontains=query)

        services_html = render_to_string('partials/service_list.html', {'services': services})
        return JsonResponse({'services_html': services_html})


def suggestions(request):
    query = request.GET.get('q', '')
    suggestions = Service.objects.filter(title__icontains=query).values_list('title', flat=True)[:5]
    return JsonResponse({'suggestions': list(suggestions)})


class OrdersMessagesView(ListView):
    model = Project
    template_name = 'ordersmessages.html'
    context_object_name = 'orders'

    def get_queryset(self):
        user_profile = self.request.user.profile
        if user_profile.is_client:
            orders = Project.objects.filter(client=user_profile)
        elif user_profile.is_freelancer:
            orders = Project.objects.filter(freelancer=user_profile)
        else:
            orders = Project.objects.none()
        return orders
