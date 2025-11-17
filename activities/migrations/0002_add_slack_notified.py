"""Add slack_notified field to Activity

Generated manually to add the slack_notified boolean field.
"""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("activities", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='slack_notified',
            field=models.BooleanField(default=False, verbose_name='Notificado en Slack'),
        ),
    ]
