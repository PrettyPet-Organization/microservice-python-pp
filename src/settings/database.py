# Configurations for connecting and configuring the database,
# including connection settings, connection pooling, and replication settings.


from settings.common import BASE_DIR


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
