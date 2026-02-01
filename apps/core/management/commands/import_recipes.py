import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from apps.core.models import Recipe

class Command(BaseCommand):
    help = 'CSVからレシピを読み込む'

    def handle(self, *args, **options):
        file_path = os.path.join(settings.BASE_DIR, 'data.csv')

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR('data.csv がありません！'))
            return
        
        Recipe.objects.all().delete()
        
        recipes_list = []
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                recipes_list.append(Recipe(
                    title=row['料理名'],
                    description=row['説明'],
                    
                    # ★ここだ！CSVの「材料」「手順」をDBに入れる
                    ingredients=row['材料'],
                    steps=row['手順'],
                    
                    calories=int(row['カロリー']),
                    protein=float(row['タンパク質']),
                    fat=float(row['脂質']),
                    carbs=float(row['炭水化物']),
                    category=row['カテゴリ'],
                    image=None
                ))

        Recipe.objects.bulk_create(recipes_list)
        self.stdout.write(self.style.SUCCESS(f'成功！ {len(recipes_list)}件のレシピ(手順付き)を取り込みました！'))