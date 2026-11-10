import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('genre', models.CharField(max_length=100)),
                ('listen_url', models.URLField(max_length=500)),
                ('featured_date', models.DateField(blank=True, null=True)),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='songs', to='music.artist')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
