# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LCOPage'
        db.create_table(u'lcogt_lcopage', (
            (u'page_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['pages.Page'], unique=True, primary_key=True)),
            ('content', self.gf('mezzanine.core.fields.RichTextField')(default='', blank=True)),
            ('extra_info', self.gf('mezzanine.core.fields.RichTextField')(default='', blank=True)),
        ))
        db.send_create_signal(u'lcogt', ['LCOPage'])

        # Adding model 'Activity'
        db.create_table(u'lcogt_activity', (
            (u'page_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['pages.Page'], unique=True, primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'activitys', to=orm['auth.User'])),
            ('full_text', self.gf('mezzanine.core.fields.RichTextField')(default='', blank=True)),
            ('goals', self.gf('mezzanine.core.fields.RichTextField')(default='', blank=True)),
            ('summary', self.gf('mezzanine.core.fields.RichTextField')(default='', blank=True)),
            ('observing_time', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('archive_data', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('planning', self.gf('mezzanine.core.fields.RichTextField')(default='', blank=True)),
            ('background', self.gf('mezzanine.core.fields.RichTextField')(default='', blank=True)),
            ('next_steps', self.gf('mezzanine.core.fields.RichTextField')(default='', blank=True)),
            ('featured_image', self.gf('filebrowser_safe.fields.FileBrowseField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'lcogt', ['Activity'])

        # Adding M2M table for field related_posts on 'Activity'
        m2m_table_name = db.shorten_name(u'lcogt_activity_related_posts')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_activity', models.ForeignKey(orm[u'lcogt.activity'], null=False)),
            ('to_activity', models.ForeignKey(orm[u'lcogt.activity'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_activity_id', 'to_activity_id'])

        # Adding model 'Seminar'
        db.create_table(u'lcogt_seminar', (
            (u'page_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['pages.Page'], unique=True, primary_key=True)),
            ('abstract', self.gf('mezzanine.core.fields.RichTextField')(default='', blank=True)),
            ('seminardate', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2015, 4, 28, 0, 0))),
            ('speaker_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('speaker_institute', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('speaker_picture', self.gf('filebrowser_safe.fields.FileBrowseField')(max_length=200, null=True, blank=True)),
            ('speaker_biog', self.gf('mezzanine.core.fields.RichTextField')(default='', blank=True)),
            ('speaker_link', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal(u'lcogt', ['Seminar'])

        # Adding model 'Profile'
        db.create_table(u'lcogt_profile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('mugshot', self.gf('filebrowser_safe.fields.FileBrowseField')(max_length=200, null=True, blank=True)),
            ('bio', self.gf('mezzanine.core.fields.RichTextField')(default='', blank=True)),
            ('job_title', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('research_interests', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'lcogt', ['Profile'])


    def backwards(self, orm):
        # Deleting model 'LCOPage'
        db.delete_table(u'lcogt_lcopage')

        # Deleting model 'Activity'
        db.delete_table(u'lcogt_activity')

        # Removing M2M table for field related_posts on 'Activity'
        db.delete_table(db.shorten_name(u'lcogt_activity_related_posts'))

        # Deleting model 'Seminar'
        db.delete_table(u'lcogt_seminar')

        # Deleting model 'Profile'
        db.delete_table(u'lcogt_profile')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'lcogt.activity': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'Activity', '_ormbases': [u'pages.Page']},
            'archive_data': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'background': ('mezzanine.core.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            'featured_image': ('filebrowser_safe.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'full_text': ('mezzanine.core.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            'goals': ('mezzanine.core.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            'next_steps': ('mezzanine.core.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            'observing_time': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['pages.Page']", 'unique': 'True', 'primary_key': 'True'}),
            'planning': ('mezzanine.core.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            'related_posts': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_posts_rel_+'", 'blank': 'True', 'to': u"orm['lcogt.Activity']"}),
            'summary': ('mezzanine.core.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'activitys'", 'to': u"orm['auth.User']"})
        },
        u'lcogt.lcopage': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'LCOPage', '_ormbases': [u'pages.Page']},
            'content': ('mezzanine.core.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            'extra_info': ('mezzanine.core.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            u'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['pages.Page']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'lcogt.profile': {
            'Meta': {'object_name': 'Profile'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'bio': ('mezzanine.core.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_title': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'mugshot': ('filebrowser_safe.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'research_interests': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'lcogt.seminar': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'Seminar', '_ormbases': [u'pages.Page']},
            'abstract': ('mezzanine.core.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            u'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['pages.Page']", 'unique': 'True', 'primary_key': 'True'}),
            'seminardate': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 4, 28, 0, 0)'}),
            'speaker_biog': ('mezzanine.core.fields.RichTextField', [], {'default': "''", 'blank': 'True'}),
            'speaker_institute': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'speaker_link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'speaker_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'speaker_picture': ('filebrowser_safe.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'pages.page': {
            'Meta': {'ordering': "(u'titles',)", 'object_name': 'Page'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'content_model': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_menus': ('mezzanine.pages.fields.MenusField', [], {'default': '(1, 2, 3)', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'login_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'children'", 'null': 'True', 'to': u"orm['pages.Page']"}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'titles': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['lcogt']