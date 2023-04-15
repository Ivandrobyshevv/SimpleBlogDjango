from django.conf import settings
from django.core.mail import send_mail

from blog.models import Post


def send_post_email(post_url: str, post: Post, cleaned_data: dict) -> bool:
    subject = f"{cleaned_data['name']} {post.title}"
    message = f"Read {post.title} at {post_url}\n\n"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [cleaned_data['to']])
    return True
