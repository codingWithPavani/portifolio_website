from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from django.core.mail import send_mail
from django.http import HttpResponse

def contact_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        subject = f"New Contact Form Submission from {name}"
        full_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        try:
            send_mail(subject, full_message, email, ['abothulapavani16@gmail.com'])
            messages.success(request, "Your message has been sent successfully!")
        except Exception as e:
            messages.error(request, f"Failed to send message: {e}")

        return redirect('contact')

    return render(request, 'index.html')


def index(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Send email
            send_mail(
                f"Portfolio Contact from {name}",
                message,
                email,
                ['abothulapavani16@gmail.com'],  # Replace with your email
                fail_silently=False,
            )

            return render(request, 'message/index.html', {
                'form': ContactForm(),  # Empty form after submit
                'success': True
            })
    else:
        form = ContactForm()

    return render(request, 'message/index.html', {'form': form})

def test_email(request):
    send_mail(
        subject='Test Email from Django',
        message='Hello! This is a test email sent from my Django project.',
        from_email='your_gmail@gmail.com',
        recipient_list=['receiver_email@gmail.com'],  # Change this to your test email
        fail_silently=False,
    )
    return HttpResponse("Email sent successfully!")


from django.shortcuts import render

def test_static(request):
    return render(request, 'message/test_static.html')
