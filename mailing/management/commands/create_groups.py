from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from mailing.models import Client, Mailing, Message


class Command(BaseCommand):
    help = 'Создаёт группу "Менеджеры" с правами'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name="Менеджеры")

        # Права для рассылок
        mailing_ct = ContentType.objects.get_for_model(Mailing)
        mailing_perms = Permission.objects.filter(
            content_type=mailing_ct, codename__in=["can_view_all_mailings", "can_block_users"]
        )

        # Права для сообщений
        message_ct = ContentType.objects.get_for_model(Message)
        message_perms = Permission.objects.filter(content_type=message_ct, codename="can_view_all_messages")

        # Права для клиентов
        client_ct = ContentType.objects.get_for_model(Client)
        client_perms = Permission.objects.filter(content_type=client_ct, codename="can_view_all_clients")

        all_perms = mailing_perms | message_perms | client_perms
        group.permissions.set(all_perms)

        self.stdout.write(self.style.SUCCESS('Группа "Менеджеры" обновлена.'))
