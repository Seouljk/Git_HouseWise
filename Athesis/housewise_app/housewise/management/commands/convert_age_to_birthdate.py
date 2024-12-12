from datetime import date, timedelta
from django.core.management.base import BaseCommand
from housewise.models import UserHousewise

class Command(BaseCommand):
    help = 'Convert age to birthdate for UserHousewise model'

    def handle(self, *args, **kwargs):
        today = date.today()
        users = UserHousewise.objects.all()

        for user in users:
            if user.age and not user.birthdate:
                # Approximate birthdate based on age
                user.birthdate = today - timedelta(days=user.age * 365.25)  # Rough approximation
                user.save()
                self.stdout.write(f"Updated birthdate for user {user.username}")
        
        self.stdout.write("Conversion complete.")
