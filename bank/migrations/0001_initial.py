# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Card'
        db.create_table(u'bank_card', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True, max_length=16)),
            ('pincode', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=4)),
            ('error_attempts', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('rest', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'bank', ['Card'])

        # Adding model 'Operations'
        db.create_table(u'bank_operations', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('card', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bank.Card'])),
            ('code', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('amount', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('rest', self.gf('django.db.models.fields.IntegerField')()),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'bank', ['Operations'])


    def backwards(self, orm):
        # Deleting model 'Card'
        db.delete_table(u'bank_card')

        # Deleting model 'Operations'
        db.delete_table(u'bank_operations')


    models = {
        u'bank.card': {
            'Meta': {'object_name': 'Card'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'error_attempts': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True', 'max_length': '16'}),
            'pincode': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '4'}),
            'rest': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'bank.operations': {
            'Meta': {'object_name': 'Operations'},
            'amount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'card': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bank.Card']"}),
            'code': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rest': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['bank']