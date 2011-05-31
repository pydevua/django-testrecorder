# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse

class BaseTestCase(TestCase):
    fixtures = ["test1.json", "test2.json", "test3.json", "test4.json"]
    
    def test_redirect(self):
        response = self.client.get(reverse("main:create"))
        
        from testrecorder.middleware import toolbar
        
        #get last RequestRecord
        rr = toolbar.records[-1][-1]
        self.assertTrue(rr.redirect_url)
        self.assertEqual(rr.redirect_url_reverse, 'reverse("login")+u"?next=/create/"')
