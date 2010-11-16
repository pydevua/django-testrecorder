# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse

class TestClass(TestCase):
    def setUp(self):
        self.auth = {
            "username": u"admin",
            "password": u"admin"
        }
    
    def test_func(self):
        self.client.login(**self.auth)
        
        response = self.client.get(reverse("main:index"))
        self.failUnlessEqual(response.status_code, 200)
        
        response = self.client.get(reverse("main:create"))
        self.failUnlessEqual(response.status_code, 200)
        
        data = {
            "content": u"asdasd",
            "name": u"asdasd",
            "image": u""
        }
        response = self.client.post(reverse("main:create"), data)
        self.assertRedirects(response, reverse("main:index"))
        
        response = self.client.get(reverse("main:index"))
        self.failUnlessEqual(response.status_code, 200)