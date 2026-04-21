from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from .models import Contact
from plants.models import Plant


def home(request):
    latest_plants = Plant.objects.all()[:3]
    return render(request, 'main/home.html', {'latest_plants': latest_plants})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()
    return render(request, 'main/contact.html', {'form': form})


def messages_list(request):
    contact_messages = Contact.objects.all()
    return render(request, 'main/messages.html', {'contact_messages': contact_messages})
