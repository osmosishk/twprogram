# Generated by Django 2.0.6 on 2020-07-08 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Buildings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='大廈名稱')),
                ('status', models.CharField(choices=[('using', 'using'), ('stoping', 'stoping')], default='using', max_length=10, verbose_name='狀態')),
                ('createTime', models.DateTimeField(auto_now_add=True, verbose_name='創建時間')),
            ],
            options={
                'verbose_name': '大廈',
                'verbose_name_plural': '大廈',
                'db_table': 'm_buildings',
                'ordering': ['-createTime'],
            },
        ),
        migrations.CreateModel(
            name='MeterData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('v1', models.IntegerField(verbose_name='V1')),
                ('v2', models.IntegerField(verbose_name='V2')),
                ('v3', models.IntegerField(verbose_name='V3')),
                ('l1', models.IntegerField(verbose_name='L1')),
                ('l2', models.IntegerField(verbose_name='L2')),
                ('l3', models.IntegerField(verbose_name='L3')),
                ('pf1', models.IntegerField(verbose_name='PF1')),
                ('pf2', models.IntegerField(verbose_name='PF2')),
                ('pf3', models.IntegerField(verbose_name='PF3')),
                ('kwh', models.IntegerField(verbose_name='KWH')),
                ('time', models.DateTimeField(verbose_name='time')),
                ('createTime', models.DateTimeField(auto_now_add=True, verbose_name='創建時間')),
                ('building', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='bases.Buildings', verbose_name='大廈名稱')),
            ],
            options={
                'verbose_name': '電表數據',
                'verbose_name_plural': '電表數據',
                'db_table': 'meter_datas',
                'ordering': ['-createTime'],
            },
        ),
        migrations.CreateModel(
            name='Meters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='電表名稱')),
                ('no', models.CharField(max_length=50, verbose_name='電表編號')),
                ('currentNumber', models.CharField(max_length=10, verbose_name='當前電表讀數')),
                ('location', models.CharField(max_length=20, verbose_name='樓棟-層數-房號')),
                ('status', models.CharField(choices=[('1', 'online'), ('0', 'offline')], default='1', max_length=10, verbose_name='狀態')),
                ('isTest', models.CharField(choices=[('1', 'yes'), ('0', 'no')], default='1', max_length=10, verbose_name='是否測試電表')),
                ('createTime', models.DateTimeField(auto_now_add=True, verbose_name='創建時間')),
                ('remark', models.CharField(blank=True, max_length=100, null=True, verbose_name='備註')),
                ('building', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='bases.Buildings', verbose_name='大廈名稱')),
            ],
            options={
                'verbose_name': '電表',
                'verbose_name_plural': '電表',
                'db_table': 'm_meters',
                'ordering': ['no'],
            },
        ),
        migrations.CreateModel(
            name='Params',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('paramName', models.CharField(max_length=50, verbose_name='參數名')),
                ('paramValue', models.CharField(max_length=50, verbose_name='參數值')),
                ('remark', models.CharField(max_length=50, verbose_name='用途')),
                ('status', models.IntegerField(verbose_name='狀態')),
                ('sort', models.IntegerField(verbose_name='順序')),
                ('createTime', models.DateTimeField(auto_now_add=True, verbose_name='創建時間')),
            ],
            options={
                'verbose_name': '參數',
                'verbose_name_plural': '參數',
                'db_table': 'm_params',
            },
        ),
        migrations.CreateModel(
            name='Rasps',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='名稱')),
                ('no', models.CharField(max_length=50, verbose_name='編號')),
                ('location', models.CharField(max_length=20, verbose_name='樓棟-層數-房號')),
                ('status', models.CharField(choices=[('1', 'online'), ('0', 'offline')], default='1', max_length=10, verbose_name='狀態')),
                ('isTest', models.CharField(choices=[('1', 'yes'), ('0', 'no')], default='1', max_length=10, verbose_name='是否測試設備')),
                ('createTime', models.DateTimeField(auto_now_add=True, verbose_name='創建時間')),
                ('remark', models.CharField(blank=True, max_length=100, null=True, verbose_name='備註')),
                ('building', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='bases.Buildings', verbose_name='大廈名稱')),
            ],
            options={
                'verbose_name': '樹莓派',
                'verbose_name_plural': '樹莓派',
                'db_table': 'm_rasps',
                'ordering': ['no'],
            },
        ),
        migrations.AddField(
            model_name='meters',
            name='rasp',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='bases.Rasps', verbose_name='樹莓派名稱'),
        ),
        migrations.AddField(
            model_name='meterdata',
            name='meter',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='bases.Meters', verbose_name='電表名稱'),
        ),
        migrations.AddField(
            model_name='meterdata',
            name='rasp',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='bases.Rasps', verbose_name='樹莓派名稱'),
        ),
        migrations.AlterUniqueTogether(
            name='buildings',
            unique_together={('name',)},
        ),
        migrations.AlterUniqueTogether(
            name='rasps',
            unique_together={('name',)},
        ),
        migrations.AlterUniqueTogether(
            name='meters',
            unique_together={('name',)},
        ),
    ]
