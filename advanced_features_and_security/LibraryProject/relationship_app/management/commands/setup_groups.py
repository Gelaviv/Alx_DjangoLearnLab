from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps 


class Command(BaseCommand):
    help = 'Creates default permission groups'

    def handle(self, *args, **options):
         Book = apps.get_model('relationship_app', 'Book')
         content_type = ContentType.objects.get_for_model(Book)


         perms = {
            'view': Permission.objects.get_or_create(
                codename='can_view_book',
                content_type=content_type,
                defaults={'name': 'Can view book'}
            )[0],
            'create': Permission.objects.get_or_create(
                codename='can_create_book',
                content_type=content_type,
                defaults={'name': 'Can create book'}
            )[0],
            'edit': Permission.objects.get_or_create(
                codename='can_edit_book',
                content_type=content_type,
                defaults={'name': 'Can edit book'}
            )[0],
            'delete': Permission.objects.get_or_create(
                codename='can_delete_book',
                content_type=content_type,
                defaults={'name': 'Can delete book'}
            )[0]
        }
         

         Group.objects.get_or_create(name='Viewers')[0].permissions.set([perms['view']])
         Group.objects.get_or_create(name='Editors')[0].permissions.set([
            perms['view'], perms['create'], perms['edit']
        ])
         Group.objects.get_or_create(name='Admins')[0].permissions.set(perms.values())
         self.stdout.write(self.style.SUCCESS('Successfully setup permission groups'))