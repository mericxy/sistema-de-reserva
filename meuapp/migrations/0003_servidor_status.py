# Generated by Django 5.1.6 on 2025-02-14 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meuapp', '0002_alter_servidor_email_alter_servidor_nome_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='servidor',
            name='status',
            field=models.CharField(choices=[('pendente', 'Pendente'), ('aprovado', 'Aprovado'), ('rejeitado', 'Rejeitado')], default='pendente', max_length=10),
        ),
    ]
