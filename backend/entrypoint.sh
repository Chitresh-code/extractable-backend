#!/usr/bin/env bash
set -e

# Show Django version & environment basics
python - <<'PY'
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "extractable.settings")
try:
    import django
    print("Django:", django.get_version())
except Exception as e:
    print("Django import failed:", e)
print("DEBUG:", os.environ.get("DEBUG"))
print("ALLOWED_HOSTS:", os.environ.get("ALLOWED_HOSTS"))
PY

# Make migrations for any changes
python manage.py makemigrations --noinput

# Apply migrations
python manage.py migrate --noinput

# Create superuser from env if missing
python - <<'PY'
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "extractable.settings")

try:
    import django
    django.setup()
    from django.contrib.auth import get_user_model

    email = os.getenv("DJANGO_SUPERUSER_EMAIL")
    password = os.getenv("DJANGO_SUPERUSER_PASSWORD")
    name = os.getenv("DJANGO_SUPERUSER_NAME", "Admin")

    if email and password:
        User = get_user_model()
        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(email=email, password=password, name=name)
            print(f"Created superuser: {email}")
        else:
            print(f"Superuser already exists: {email}")
    else:
        print("Skipping superuser creation (missing DJANGO_SUPERUSER_* env).")
except Exception as e:
    print("Superuser creation failed:", e)
PY

# Collect static files
if [ "${SKIP_COLLECTSTATIC}" != "1" ]; then
  python manage.py collectstatic --noinput
fi

exec "$@"