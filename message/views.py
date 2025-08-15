from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
import re
import logging
logger = logging.getLogger(__name__)

def contact_view(request):
    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        # 1️⃣ Basic validation
        if not name or not email or not message:
            messages.error(request, "All fields are required.")
            return redirect('contact')

        # 2️⃣ Email format validation
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            messages.error(request, "Please enter a valid email address.")
            return redirect('contact')

        # 3️⃣ Prepare email content
        admin_subject = f"New Contact Form Submission from {name}"
        admin_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        user_subject = "Thank you for contacting us"
        user_message = (
            f"Hi {name},\n\n"
            "Thank you for reaching out to us. We have received your message and will get back to you soon.\n\n"
            "Your message:\n"
            f"{message}\n\n"
            "Best regards,\nYour Website Team"
        )

        try:
            # Send email to admin
            send_mail(admin_subject, admin_message, settings.DEFAULT_FROM_EMAIL, ['abothulapavani16@gmail.com'])

            # Send confirmation to user
            send_mail(user_subject, user_message, settings.DEFAULT_FROM_EMAIL, [email])

            messages.success(request, "Your message has been sent successfully!")
        except BadHeaderError:
            messages.error(request, "Invalid header found.")
        except Exception as e:
            logger.error(f"Error sending contact form email: {e}")
            messages.error(request, "An error occurred while sending your message. Please try again later.")

        return redirect('contact')

    return render(request, 'message/index.html')


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
