# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.utils.text import format_lazy
from django.contrib.gis.db import models
from django.contrib.postgres.fields import HStoreField
from allauth.account.models import EmailAddress


class V2OfUserRoles(models.Model):
    authority = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'v2of_user_roles'
        verbose_name_plural = format_lazy('{}', db_table)


class V2OfUsers(models.Model):
    email = models.CharField(max_length=255, blank=True, null=True)
    enabled = models.IntegerField(blank=True, null=True)
    firstname = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    passwordformat = models.IntegerField(blank=True, null=True)
    passwordsalt = models.CharField(max_length=255, blank=True, null=True)
    user_role = models.ForeignKey(V2OfUserRoles, on_delete=models.CASCADE, db_column='user_role', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'v2of_users'
        verbose_name_plural = format_lazy('{}', db_table)

    def __str__(self):
        return self.username

    @property
    def is_active(self):
        if not hasattr(self, '_is_active'):
            if (self.enabled):
                self._is_active = True
            if not self._is_active:
                raise ImproperlyConfigured('Could not get user status')
        return self._is_active


class V2OfAreas(models.Model):
    name = models.CharField(max_length=70, blank=True, null=True)
    area = models.GeometryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'v2of_areas'
        verbose_name_plural = format_lazy('{}', db_table)


class V2OfCampaigns(models.Model):
    create_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    name = models.CharField(max_length=70, blank=True, null=True)
    active = models.SmallIntegerField(blank=True, null=True)
    area = models.ForeignKey(V2OfAreas, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(V2OfUsers, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'v2of_campaigns'
        verbose_name_plural = format_lazy('{}', db_table)


class V2OfDevices(models.Model):
    android_id = models.CharField(primary_key=True, max_length=16)
    device_id = models.CharField(unique=True, max_length=16)
    device_serial = models.CharField(max_length=16)
    device_mac = models.TextField()  # This field type is a guess for MAC ADDRESS
    device_brand = models.CharField(max_length=30, blank=True, null=True)
    device_model = models.CharField(max_length=30, blank=True, null=True)
    device_product = models.CharField(max_length=30, blank=True, null=True)
    device_build_id = models.CharField(max_length=30, blank=True, null=True)
    os = models.CharField(max_length=30, blank=True, null=True)
    os_version = models.CharField(max_length=30, blank=True, null=True)
    os_id = models.CharField(max_length=128, blank=True, null=True)
    subscriber_id = models.CharField(max_length=16)
    uuid = models.UUIDField()
    id = models.IntegerField(unique=True)
    user = models.ForeignKey(V2OfUsers, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'v2of_devices'
        unique_together = (('android_id', 'device_id', 'device_mac', 'subscriber_id', 'uuid', 'device_serial'),)
        verbose_name_plural = format_lazy('{}', db_table)


class V2OfCollections(models.Model):
    lon = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    lat = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    geomcol1 = models.BinaryField(blank=True, null=True)
    geomcol2 = models.GeometryField(blank=True, null=True)
    time_tx = models.DateTimeField(blank=True, null=True)
    time_rx = models.DateTimeField(blank=True, null=True)
    campaign = models.ForeignKey(V2OfCampaigns, on_delete=models.CASCADE, blank=True, null=True)
    device = models.ForeignKey(V2OfDevices, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'v2of_collections'
        verbose_name_plural = format_lazy('{}', db_table)


class V2OfMeasurements(models.Model):
    collection = models.ForeignKey(V2OfCollections, on_delete=models.CASCADE, blank=True, null=True)
    values = HStoreField()

    class Meta:
        managed = False
        db_table = 'v2of_measurements'
        verbose_name_plural = format_lazy('{}', db_table)


class V2OfMetrics(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    unit = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'v2of_metrics'
        verbose_name_plural = format_lazy('{}', db_table)


# DJANGO ADMIN TABLES
class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey(DjangoContentType, on_delete=models.CASCADE)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, on_delete=models.CASCADE)
    permission = models.ForeignKey(AuthPermission, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    group = models.ForeignKey(AuthGroup, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    permission = models.ForeignKey(AuthPermission, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey(DjangoContentType, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Measurements(models.Model):
    id = models.BigAutoField(primary_key=True)
    geomcol1 = models.BinaryField(db_column='GeomCol1', blank=True, null=True)  # Field name made lowercase.
    timestamp = models.DateTimeField(blank=True, null=True)
    lon = models.DecimalField(max_digits=10, decimal_places=5)
    lat = models.DecimalField(max_digits=10, decimal_places=5)
    level = models.IntegerField(blank=True, null=True)
    speed = models.FloatField(blank=True, null=True)
    operatorname = models.CharField(max_length=50, blank=True, null=True)
    mcc = models.CharField(max_length=3, blank=True, null=True)
    mnc = models.CharField(max_length=3, blank=True, null=True)
    node = models.CharField(max_length=11, blank=True, null=True)
    cellid = models.CharField(max_length=11, blank=True, null=True)
    lac = models.CharField(max_length=11, blank=True, null=True)
    network_type = models.CharField(max_length=2, blank=True, null=True)
    qual = models.IntegerField(blank=True, null=True)
    snr = models.IntegerField(blank=True, null=True)
    cqi = models.IntegerField(blank=True, null=True)
    lterssi = models.IntegerField(blank=True, null=True)
    appversioncode = models.IntegerField(blank=True, null=True)
    psc = models.IntegerField(blank=True, null=True)
    dl_bitrate = models.IntegerField(blank=True, null=True)
    ul_bitrate = models.IntegerField(blank=True, null=True)
    nlac1 = models.IntegerField(blank=True, null=True)
    ncellid1 = models.IntegerField(blank=True, null=True)
    nrxlev1 = models.IntegerField(blank=True, null=True)
    nlac2 = models.IntegerField(blank=True, null=True)
    ncellid2 = models.IntegerField(blank=True, null=True)
    nrxlev2 = models.IntegerField(blank=True, null=True)
    nlac3 = models.IntegerField(blank=True, null=True)
    ncellid3 = models.IntegerField(blank=True, null=True)
    nrxlev3 = models.IntegerField(blank=True, null=True)
    nlac4 = models.IntegerField(blank=True, null=True)
    ncellid4 = models.IntegerField(blank=True, null=True)
    nrxlev4 = models.IntegerField(blank=True, null=True)
    nlac5 = models.IntegerField(blank=True, null=True)
    ncellid5 = models.IntegerField(blank=True, null=True)
    nrxlev5 = models.IntegerField(blank=True, null=True)
    nlac6 = models.IntegerField(blank=True, null=True)
    ncellid6 = models.IntegerField(blank=True, null=True)
    nrxlev6 = models.IntegerField(blank=True, null=True)
    ctime = models.DateTimeField(blank=True, null=True)
    event = models.CharField(max_length=20, blank=True, null=True)
    accuracy = models.IntegerField(blank=True, null=True)
    locationsource = models.CharField(max_length=2, blank=True, null=True)
    altitude = models.IntegerField(blank=True, null=True)
    conntype = models.CharField(max_length=5, blank=True, null=True)
    conninfo = models.CharField(max_length=25, blank=True, null=True)
    avgping = models.IntegerField(blank=True, null=True)
    minping = models.IntegerField(blank=True, null=True)
    maxping = models.IntegerField(blank=True, null=True)
    stdevping = models.IntegerField(blank=True, null=True)
    pingloss = models.IntegerField(blank=True, null=True)
    testdlbitrate = models.IntegerField(blank=True, null=True)
    testulbitrate = models.IntegerField(blank=True, null=True)
    geomcol2 = models.GeometryField(db_column='GeomCol2', srid=0, blank=True, null=True)  # Field name made lowercase.
    devicemanufacturer = models.CharField(db_column='DeviceManufacturer', max_length=30, blank=True,
                                          null=True)  # Field name made lowercase.
    devicemodel = models.CharField(db_column='DeviceModel', max_length=30, blank=True,
                                   null=True)  # Field name made lowercase.
    devicename = models.CharField(db_column='DeviceName', max_length=30, blank=True,
                                  null=True)  # Field name made lowercase.
    versionname = models.CharField(db_column='VersionName', max_length=30, blank=True,
                                   null=True)  # Field name made lowercase.
    brand = models.CharField(db_column='Brand', max_length=30, blank=True, null=True)  # Field name made lowercase.
    androidversion = models.CharField(db_column='AndroidVersion', max_length=30, blank=True,
                                      null=True)  # Field name made lowercase.
    servingcelltime = models.IntegerField(db_column='ServingCellTime', blank=True,
                                          null=True)  # Field name made lowercase.
    os = models.CharField(max_length=30, blank=True, null=True)
    os_id = models.CharField(max_length=128, blank=True, null=True)
    camp = models.ForeignKey(V2OfCampaigns, on_delete=models.CASCADE, blank=True, null=True)
    ssid = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Measurements'
        verbose_name_plural = format_lazy('{}', db_table)
