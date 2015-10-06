import unittest
from freezegun import freeze_time

from furl import furl
import pytest
from nzbhydra import config

from nzbhydra.database import Provider
from nzbhydra.searchmodules.binsearch import Binsearch
from nzbhydra.tests.db_prepare import set_and_drop
from nzbhydra.tests.providerTest import ProviderTestcase


class MyTestCase(ProviderTestcase):
    
    @pytest.fixture
    def setUp(self):
        set_and_drop()
         
        

    def testUrlGeneration(self):
        w = Binsearch(config.providerBinsearchSettings)
        self.args.update({"query": "a showtitle", "season": 1, "episode": 2})
        urls = w.get_showsearch_urls(self.args)
        self.assertEqual(2, len(urls))
        self.assertEqual('a showtitle s01e02', furl(urls[0]).args["q"])
        self.assertEqual('a showtitle 1x02', furl(urls[1]).args["q"])

        self.args.update({"query": "a showtitle", "season": 1, "episode": None})
        urls = w.get_showsearch_urls(self.args)
        self.assertEqual(2, len(urls))
        self.assertEqual('a showtitle s01', furl(urls[0]).args["q"])
        self.assertEqual('a showtitle "season 1"', furl(urls[1]).args["q"])

    @freeze_time("2015-09-30 14:00:00", tz_offset=-4)
    def testProcess_results(self):
        w = Binsearch(config.providerBinsearchSettings)
        with open("mock/binsearch--q-avengers.html", encoding="latin-1") as f:
            body = f.read()
            entries = w.process_query_result(body, "aquery").entries
            self.assertEqual('MARVELS.AVENGERS.AGE.OF.ULTRON. 3D.TOPBOT.TrueFrench.1080p.X264.AC3.5.1-JKF.mkv', entries[0].title)
            self.assertEqual("https://www.binsearch.info/fcgi/nzb.fcgi?q=176073735", entries[0].link)
            self.assertEqual(13110387671, entries[0].size)
            self.assertEqual("176073735", entries[0].guid)
            self.assertEqual(1443312000, entries[0].epoch)
            self.assertEqual("2015-09-27T00:00:00+00:00", entries[0].pubdate_utc)
            self.assertEqual(3, entries[0].age_days)
            self.assertFalse(entries[0].age_precise)
            self.assertEqual("Ramer@marmer.com <Clown_nez>", entries[0].poster)
            self.assertFalse(entries[0].has_nfo)
            
            self.assertTrue(entries[8].has_nfo)
            
                
    def testGetNzbLink(self):
        n = Binsearch(config.providerBinsearchSettings)
        link = n.get_nzb_link("guid", "title")
        assert "action=nzb" in link
        assert "guid=1" in link
        
