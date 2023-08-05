import asyncio
from cprint import *
import time

from argox.scoketscanner.socketscanner import portscanner
from argox.pyffuf.pyffuf import FUZZER
from argox.spider.spider import WebSpider
from argox.reverse.reverse import DnsEnum
from argox.cmsDetect.cmsDetect import analyzier


class Argo:
    def __init__(self,url):
        self.url = url
        self.now = time.time()
        
    def scanport(self, host=None, fullscan=False):
        if host is None:
            host = self.url
        pscan = portscanner(host,fullscan)
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(pscan.main())
        loop.run_until_complete(future)
        cprint.info(str('Total time: {time}'.format(time=time.time() - self.now)))
        return future.result()
        
        
    def fuzzer(self):
        fuzz = FUZZER(self.url, r"/usr/share/wordlists/dirb/common.txt")
        if "PUFF" not in self.url:
            return ["PUFF keyword not found!"]
        #data = fuzz.main()
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(fuzz.main())
        loop.run_until_complete(future)
        cprint.info(str('Total time: {time}'.format(time=time.time() - self.now)))
        return future.result()
        
    def webspider(self):
        spider = WebSpider(self.url)
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(spider.run())
        loop.run_until_complete(future)
        cprint.info(str('Total time: {time}'.format(time=time.time() - self.now)))
        return future.result()
    
    def DnsEnum(self):
        denum = DnsEnum(self.url)
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(denum.run())
        loop.run_until_complete(future)
        cprint.info(str('Total time: {time}'.format(time=time.time() - self.now)))
        return future.result()

    def analyze(self):
        cms = analyzier(self.url)
        data = cms.run()
        return data.replace("\t","").split(), data