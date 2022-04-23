
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from .models import Post, Category
from django.template.loader import render_to_string
from django.contrib.auth.models import User


@receiver(m2m_changed, sender=Post.postCategory.through)
def notify_subs(sender, instance, **kwargs):
    for category in instance.postCategory.all():
        for sub in category.subscribers.all():
            
            html_content = render_to_string(
                'post_created.html',
                {'post':instance,}
            )
            msg = EmailMultiAlternatives(
                subject=f'{instance.postTitle}',
                body = instance.postText,
                from_email='skillgtest@yandex.ru',
                to = [sub.email],
            )
            msg.attach_alternative(html_content, 'text/html')
            msg.send()