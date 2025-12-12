import sys
with open("django_check_log.txt", "w") as f:
    try:
        import django
        f.write(f"Django version: {django.get_version()}\n")
        f.write(f"Executable: {sys.executable}\n")
    except Exception as e:
        f.write(f"Error: {e}\n")
