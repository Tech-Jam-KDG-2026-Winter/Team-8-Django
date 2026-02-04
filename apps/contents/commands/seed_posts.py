from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.contents.models import MenuPost

User = get_user_model()

class Command(BaseCommand):
    help = "Create sample MenuPost records"

    def handle(self, *args, **options):
        # 投稿者用ユーザー（いなければ作る）
        user, _ = User.objects.get_or_create(
            username="seed_user",
            defaults={"email": "seed@example.com"},
        )
        user.set_password("password1234")
        user.save()

        samples = [
            {
                "title": "鶏むね肉の塩こうじ焼き",
                "ingredients": "鶏むね肉 200g\n塩こうじ 大さじ1\nこしょう 少々",
                "recipe": "1. 漬ける\n2. 焼く\n3. 盛る",
            },
            {
                "title": "野菜たっぷりスープ",
                "ingredients": "キャベツ\nにんじん\n玉ねぎ\nコンソメ",
                "recipe": "1. 切る\n2. 煮る\n3. 味を調える",
            },
            {
                "title": "納豆たまごごはん",
                "ingredients": "ご飯\n納豆\n卵\n醤油",
                "recipe": "1. 混ぜる\n2. のせる\n3. 食べる",
            },
            {
                "title": "鮭のホイル焼き",
                "ingredients": "鮭\nきのこ\nバター\n醤油",
                "recipe": "1. 包む\n2. 焼く\n3. 仕上げる",
            },
        ]

        created = 0
        for s in samples:
            obj, is_created = MenuPost.objects.get_or_create(
                user=user,
                title=s["title"],
                defaults={
                    "ingredients": s["ingredients"],
                    "recipe": s["recipe"],
                }
            )
            if is_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Seed completed. created={created}"))
