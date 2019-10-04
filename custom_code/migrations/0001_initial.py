# Generated by Django 2.1.2 on 2019-05-18 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TNSTarget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', help_text='The name of the target, e.g. 2017cbv.', max_length=100, verbose_name='Name')),
                ('name_prefix', models.CharField(blank=True, default='', help_text='The name prefix, either AT (astronomical transient) or SN (supernova).', max_length=100, null=True, verbose_name='Name prefix')),
                ('ra', models.FloatField(help_text='Right Ascension, in degrees.', verbose_name='Right Ascension')),
                ('dec', models.FloatField(help_text='Declination, in degrees.', verbose_name='Declination')),
                ('redshift', models.FloatField(blank=True, help_text='Redshift.', null=True, verbose_name='Redshift')),
                ('classification', models.CharField(blank=True, default='', help_text='The classification of this target, e.g. SN Ia.', max_length=100, null=True, verbose_name='Target classification')),
                ('internal_name', models.CharField(blank=True, default='', help_text='Internal name for an object, e.g. DLT17u.', max_length=100, null=True, verbose_name='Internal name')),
                ('source_group', models.CharField(blank=True, default='', help_text='Source group, e.g. DLT', max_length=100, null=True, verbose_name='Source group')),
                ('lnd_jd', models.FloatField(blank=True, help_text='Last non-detection JD', null=True, verbose_name='Last non-detection JD')),
                ('lnd_maglim', models.FloatField(blank=True, help_text='Last non-detection limiting magnitude', null=True, verbose_name='Last non-detection limiting magnitude')),
                ('lnd_filter', models.CharField(blank=True, default='', help_text='Last non-detection filter', max_length=100, null=True, verbose_name='Last non-detection filter')),
                ('disc_jd', models.FloatField(blank=True, help_text='Discovery JD', null=True, verbose_name='Discovery JD')),
                ('disc_mag', models.FloatField(blank=True, help_text='Discovery magnitude', null=True, verbose_name='Discovery magnitude')),
                ('disc_filter', models.CharField(blank=True, default='', help_text='Discovery filter', max_length=100, null=True, verbose_name='Discovery filter')),
                ('all_phot', models.TextField(blank=True, help_text='All photometry', null=True, verbose_name='All photometry')),
                ('TESS_sectors', models.CharField(blank=True, default='', help_text='TESS sectors the object is in.', max_length=255, null=True, verbose_name='TESS Sectors')),
            ],
            options={
                'ordering': ('id',),
                'get_latest_by': ('name',),
            },
        ),
# #BY LW:
#         migrations.CreateModel(
#             name='UlensTarget',
#             fields=[
#                 ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
#                 ('name', models.CharField(default='', help_text='The name of the target, e.g. Gaia16aye', max_length=100, verbose_name='Name')),
#                 ('ra', models.FloatField(help_text='Right Ascension, in degrees.', verbose_name='Right Ascension')),
#                 ('dec', models.FloatField(help_text='Declination, in degrees.', verbose_name='Declination')),
#                 ('classification', models.CharField(blank=True, default='', help_text='The classification of this target, e.g. SN Ia.', max_length=100, null=True, verbose_name='Target classification')),
#                 ('last_jd', models.FloatField(blank=True, help_text='Last observation JD', null=True, verbose_name='Last observation JD')),
#                 ('last_mag', models.FloatField(blank=True, help_text='Last observation magnitude', null=True, verbose_name='Last observation magnitude')),
#                 ('last_obs', models.FloatField(blank=True, help_text='Last observation observatory', null=True, verbose_name='Last observation observatory')),
#                 ('disc_jd', models.FloatField(blank=True, help_text='Discovery JD', null=True, verbose_name='Discovery JD')),
#                 ('disc_mag', models.FloatField(blank=True, help_text='Discovery magnitude', null=True, verbose_name='Discovery magnitude')),
#                 ('all_phot', models.TextField(blank=True, help_text='All photometry', null=True, verbose_name='All photometry')),
#                 ('TESS_sectors', models.CharField(blank=True, default='', help_text='TESS sectors the object is in.', max_length=255, null=True, verbose_name='TESS Sectors')),
#             ],
#             options={
#                 'ordering': ('id',),
#                 'get_latest_by': ('name',),
#             },
#         ),

    ]
