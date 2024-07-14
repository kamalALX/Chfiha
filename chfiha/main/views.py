# main/views.py
from django.views.generic import ListView, DetailView, TemplateView, FormView, CreateView
from .models import Project, Service, Categorie, OrderMessage
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm, OrderMessageForm, ServiceForm
from django.urls import reverse

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            context['form'] = ServiceForm(self.request.POST, instance=self.object)
        else:
            context['form'] = ServiceForm(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ServiceForm(request.POST, instance=self.object)
        if form.is_valid():
            form.save()
            return redirect('service', pk=self.object.pk)  # Adjust to your service detail URL name
        else:
            return self.render_to_response(self.get_context_data(form=form))

class ServicesView(ListView):
    model = Service
    template_name = 'services.html'
    context_object_name = 'services'

    """
        overriding the get_queryset method to filter the results based on the search query.
    """
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        category_id = self.request.GET.get('category')

        if query:
            queryset = queryset.filter(title__icontains=query)  # Modify based on your filtering logic
        if category_id:
            queryset = queryset.filter(categorie_id=category_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Categorie.objects.all()
        return context
    

class OrdersMessagesView(ListView):
    model = Project
    template_name = 'ordersmessages.html'
    context_object_name = 'projects'

    def get_queryset(self):
        user_profile = self.request.user.profile
        if user_profile.user_type == 'client':
            projects = Project.objects.filter(client=user_profile)
        elif user_profile.user_type == 'freelancer':
            projects = Project.objects.filter(freelancer=user_profile)
        else:
            projects = Project.objects.none()
        return projects

class OrderDetailView(DetailView):
    model = Project
    template_name = 'order_detail.html'  # Replace with your template name
    context_object_name = 'project'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()  # Fetch the Project instance

        # Fetch related OrderMessages for this Project
        order_messages = OrderMessage.objects.filter(project=project)

        # Add order_messages to the context
        context['order_messages'] = order_messages
        context['message_form'] = OrderMessageForm()
        return context

    def post(self, request, *args, **kwargs):
        project = self.get_object()
        form = OrderMessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user.profile  # Adjust according to your user model
            message.receiver = project.client if request.user.profile == project.freelancer else project.freelancer
            message.project = project
            message.save()
            return redirect('order_detail', pk=project.pk)  # Redirect to the same page
        return self.get(request, *args, **kwargs)

def pay_service(request, pk):
    try:
        service = Service.objects.get(pk=pk)
    except Service.DoesNotExist:
        return redirect(reverse('home'))  # Redirect to home page or appropriate URL

    return redirect(reverse('payment_confirmation'))

def payment_confirmation(request):
    return render(request, 'payment_confirmation.html')
