from django.core.management.base import BaseCommand
from django.db import models
from characters.models import Equipment


class Command(BaseCommand):
    help = 'Очищает дублированные записи экипировки, оставляя по одной на персонажа'

    def handle(self, *args, **options):
        # Получаем все персонажи с дублированной экипировкой
        duplicate_characters = Equipment.objects.values('character').annotate(
            count=models.Count('id')
        ).filter(count__gt=1).values_list('character', flat=True)

        cleaned_count = 0

        for character_id in duplicate_characters:
            # Получаем все записи экипировки для этого персонажа
            equipment_records = Equipment.objects.filter(character_id=character_id).order_by('id')

            # Оставляем первую запись, удаляем остальные
            first_equipment = equipment_records.first()
            duplicates = equipment_records.exclude(id=first_equipment.id)

            if duplicates.exists():
                duplicate_count = duplicates.count()
                duplicates.delete()
                cleaned_count += duplicate_count
                self.stdout.write(
                    self.style.SUCCESS(f'Удалено {duplicate_count} дубликатов экипировки для персонажа {character_id}')
                )

        if cleaned_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'Всего очищено дубликатов: {cleaned_count}')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('Дубликатов экипировки не найдено')
            )
