import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from apps.core.models import Recipe

class Command(BaseCommand):
  help = 'CSVからデータレシピを読み込む'

  def handle(self, * args, **options):
    file_path = os.path.join(settings.BASE_DIR, 'data.csv')

    if not os.path.exists(file_path):
      self.stdout.write(self.style.ERROR(f'data.csv が見つかりません。'))
      return
    
    #既存データをリセット(重複防止)
    Recipe.objects.all().delete()

    recipes_list = []
    with open(file_path, 'r', encoding='utf-8') as file:
      reader = csv.DictReader(file)
      for row in reader:
        recipes_list.append(Recipe(
          title=row['料理名'],
          description=row['説明'],
          calories=int(row['カロリー']),
          protein=float(row['タンパク質']),
          fat=float(row['脂質']),
          carbs=float(row['炭水化物']),
          category=row['カテゴリ'],
          image=row['画像パス']#CSVのパスをそのまま登録
        ))

    # 一括登録(高速化)
    Recipe.objects.bulk_create(recipes_list)
    self.stdout.write(self.style.SUCCESS(f'{len(recipes_list)}件のレシピを取り込みました！'))