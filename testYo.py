#!/usr/bin/env python
'''
Created on 29.11.2011

@author: hinata
'''
from __future__ import print_function,with_statement
import unittest

class Test(unittest.TestCase):
    def qtProgress(self):
        print("[libyo.user.progress.qt Test]")
        from PyQt4 import QtGui
        app=QtGui.QApplication([])
        from libyo.interface.progress.qt import QtProgress
        import time
        print("Test 1: Basic use")
        p=QtProgress()
        print(p)
        p.setName("QtProgress Test")
        p.setTask("Test 1: Basic use")
        p.start()
        for i in range(p.max):
            p.next()
            time.sleep(0.01)
        p.stop()
        print("Test 2: Iterator use")
        p=QtProgress()
        p.dialog.reset()
        p.setTask("Test 2: Iterator")
        p.start()
        for i in p:
            time.sleep(0.01)
        p.stop()
        print("Test 3: TaskList Processing")
        p=QtProgress()
        p.taskList([" ".join(("Test 3: TaskList Processing:",str(i))) for i in range(50)])
        p.start()
        for i in p:
            time.sleep(0.01)
        p.stop()
        print()
    def youtube1(self):
        print("[libyo.youtube Test]")
        pl="98113EFC99B5878C"
        from libyo.youtube import playlist,resolve
        from random import choice
        p=playlist.advanced(pl)
        v=choice(p["data"]["items"])
        x=resolve.resolve3(v["video"]["id"])
        print(x.title)
        print()
    def youtube2(self):
        from libyo.youtube.url import id_from_url
        print("[libyo.youtube.resolve Test]")
        vid = "http://www.youtube.com/watch?v=zUQCgTFSxBE&list=PL037FB54C523B4637&index=6&feature=plpp_video"
        id = id_from_url(vid)
        from libyo.youtube.resolve import resolve3
        v= resolve3(id)
        print (",".join([":".join((str(a),b[:5])) for a,b in v.urlmap.items()]))
        print(v.title)
        print(v.uploader)
    def magic(self):
        print("[libyo.magic Test]")
        import libyo.magic
        print(libyo.magic.from_file(__file__),end="; ")
        print(libyo.magic.from_file(__file__,True))
        buffer="#!/usr/bin/python3\ndef lol():\n\tprint(\"lol\")".encode("ASCII")
        print(libyo.magic.from_buffer(buffer),end="; ")
        print(libyo.magic.from_buffer(buffer,True))
        print()
    def configparser(self):
        print("[libyo.configparser Test]")
        import libyo.configparser
        parser=libyo.configparser.SpecialConfigParser()
        parser.add_section("TEST")
        parser.set("TEST","Comment","This is a test")
        parser.set("TEST","List",["A","B","C"])
        parser.add_section(parser.NOSECT)
        parser.set(parser.NOSECT, "Header", "Welcome")
        with open("testYo.ini","w") as fp:
            parser.write(fp)
        del parser
        parser=libyo.configparser.SpecialConfigParser()
        parser.read("testYo.ini")
        print(dict([(s,dict(parser[s])) for s in parser]))
        del parser
        print()

if __name__ == "__main__":
    import sys
    if len(sys.argv)<2:
        sys.argv.append("Test.magic")
        sys.argv.append("Test.youtube1")
        sys.argv.append("Test.youtube2")
        sys.argv.append("Test.configparser")
    unittest.main()