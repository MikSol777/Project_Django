from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = 'Создает группу "Модератор продуктов" с необходимыми правами.'

    group_name = 'Модератор продуктов'
    required_permissions = [
        ('can_unpublish_product', 'catalog'),
        ('delete_product', 'catalog'),
    ]

    @transaction.atomic
    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name=self.group_name)
        permissions = []
        missing_perms = []

        for codename, app_label in self.required_permissions:
            try:
                perm = Permission.objects.get(codename=codename, content_type__app_label=app_label)
                permissions.append(perm)
            except Permission.DoesNotExist:
                missing_perms.append(f'{app_label}.{codename}')

        if missing_perms:
            self.stdout.write(
                self.style.WARNING(
                    'Следующие права не найдены и не были добавлены к группе: '
                    + ', '.join(missing_perms)
                )
            )

        if permissions:
            group.permissions.add(*permissions)

        if created:
            self.stdout.write(self.style.SUCCESS(f'Группа "{self.group_name}" создана.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Группа "{self.group_name}" обновлена.'))

