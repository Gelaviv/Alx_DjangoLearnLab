from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book  


# class Command(BaseCommand):
#     help = 'Creates default permission groups'

#     def handle(self, *args, **options):
#          Book = apps.get_model('relationship_app', 'Book')
#          content_type = ContentType.objects.get_for_model(Book)


#          perms = {
#             'view': Permission.objects.get_or_create(
#                 codename='can_view_book',
#                 content_type=content_type,
#                 defaults={'name': 'Can view book'}
#             )[0],
#             'create': Permission.objects.get_or_create(
#                 codename='can_create_book',
#                 content_type=content_type,
#                 defaults={'name': 'Can create book'}
#             )[0],
#             'edit': Permission.objects.get_or_create(
#                 codename='can_edit_book',
#                 content_type=content_type,
#                 defaults={'name': 'Can edit book'}
#             )[0],
#             'delete': Permission.objects.get_or_create(
#                 codename='can_delete_book',
#                 content_type=content_type,
#                 defaults={'name': 'Can delete book'}
#             )[0]
#         }
         

#          Group.objects.get_or_create(name='Viewers')[0].permissions.set([perms['view']])
#          Group.objects.get_or_create(name='Editors')[0].permissions.set([
#             perms['view'], perms['create'], perms['edit']
#         ])
#          Group.objects.get_or_create(name='Admins')[0].permissions.set(perms.values())
#          self.stdout.write(self.style.SUCCESS('Successfully setup permission groups'))





class Command(BaseCommand):
    help = 'Creates default permission groups for books'

    def handle(self, *args, **options):
        # Get content type for Book model
        content_type = ContentType.objects.get_for_model(Book)
        
        # Create or get permissions
        view_perm, _ = Permission.objects.get_or_create(
            codename='can_view_book',
            content_type=content_type,
            defaults={'name': 'Can view book'}
        )
        create_perm, _ = Permission.objects.get_or_create(
            codename='can_create_book',
            content_type=content_type,
            defaults={'name': 'Can create book'}
        )
        edit_perm, _ = Permission.objects.get_or_create(
            codename='can_edit_book',
            content_type=content_type,
            defaults={'name': 'Can edit book'}
        )
        delete_perm, _ = Permission.objects.get_or_create(
            codename='can_delete_book',
            content_type=content_type,
            defaults={'name': 'Can delete book'}
        )



        # Create Groups with permissions
        viewers, _ = Group.objects.get_or_create(name='Viewers')
        editors, _ = Group.objects.get_or_create(name='Editors')
        admins, _ = Group.objects.get_or_create(name='Admins')
        
        viewers.permissions.set([view_perm])
        editors.permissions.set([view_perm, create_perm, edit_perm])
        admins.permissions.set([view_perm, create_perm, edit_perm, delete_perm])
        
        self.stdout.write(self.style.SUCCESS(
            'Successfully created groups with book permissions:\n'
            f'- Viewers: {viewers.permissions.count()} permission\n'
            f'- Editors: {editors.permissions.count()} permissions\n'
            f'- Admins: {admins.permissions.count()} permissions'
        ))