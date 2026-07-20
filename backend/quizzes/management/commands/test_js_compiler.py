from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Test OnlineCompiler.io JS compiler availability"

    def handle(self, *args, **options):
        self.stdout.write("Testing OnlineCompiler.io JS compiler...")

        try:
            from quizzes.sandbox import execute_code
            result = execute_code("javascript", 'print("hello")', "")
            output = result.get("output", "")
            status = result.get("status", "")

            if status == "success" and "hello" in output:
                self.stdout.write(self.style.SUCCESS(f"PASS — JS compiler works. Output: {output.strip()}"))
                self.stdout.write("Use: python manage.py seed_data --full")
            else:
                self.stdout.write(self.style.WARNING(
                    f"FAIL — JS compiler returned unexpected result.\n"
                    f"  status: {status}\n"
                    f"  output: {output}\n"
                    f"Use: python manage.py seed_data --no-js-coding"
                ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f"FAIL — {e}\n"
                f"Use: python manage.py seed_data --no-js-coding"
            ))
