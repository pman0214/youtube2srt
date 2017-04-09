# -*- coding: utf-8 -*-
#
# Copyright (c) 2017, Shigemi ISHIDA
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the Institute nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE INSTITUTE AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE INSTITUTE OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

import sys
import datetime
import pytz
import xml.etree.ElementTree as ET
import codecs

#======================================================================
class SubsXML():
    def __init__(self, filename):
        # load XML file
        try:
            self.xmltree = ET.parse(filename)
        except IOError:
            sys.stderr.write("Cannot load XML file: %s\n" % filename)
            quit()

        # get root element
        self.root = self.xmltree.getroot()
        return

    #--------------------------------------------------
    def parse(self):
        seq = 0                         # sequence number
        self.subs = []
        for text in self.root:
            # extract subtitle information
            sub = {'seq': seq,
                   'start': float(text.attrib['start']),
                   'dur': float(text.attrib['dur']),
                   'text': text.text,
                   }
            # calculate end time
            sub['end'] = sub['start'] + sub['dur']

            # convert time into datetime.datetime object
            #   we ignore year,month,day as we use unixtime conversion method
            sub['start'] = datetime.datetime.fromtimestamp(sub['start'], tz=pytz.utc)
            sub['end'] = datetime.datetime.fromtimestamp(sub['end'], tz=pytz.utc)

            # store and increment sequence number
            self.subs.append(sub)
            seq += 1

        return

    #--------------------------------------------------
    def write_to_file(self, outfile):
        with codecs.open(outfile, 'w', 'utf-8') as f:
            for sub in self.subs:
                f.write("%d\n" % sub['seq'])
                f.write("%s,%02d --> %s,%02d\n" % (sub['start'].strftime('%H:%M:%S'),
                                                   sub['start'].microsecond / 10000,
                                                   sub['end'].strftime('%H:%M:%S'),
                                                   sub['end'].microsecond / 10000))
                # insert blank line after a subtitle entry
                f.write(sub['text']+"\n\n")
        f.close()
        return

    #--------------------------------------------------
    def write_to_disp(self):
        for sub in self.subs:
            print "%d" % sub['seq']
            print "%s,%02d --> %s,%02d" % (sub['start'].strftime('%H:%M:%S'),
                                           sub['start'].microsecond / 10000,
                                           sub['end'].strftime('%H:%M:%S'),
                                           sub['end'].microsecond / 10000)
            print sub['text']
            # insert blank line after a subtitle entry
            print ""

        return

#======================================================================
def arg_parser():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input_xml", type=str, action="store",
                        help="subtitle input XML file",
                        )
    parser.add_argument("-o", "--output", type=str, action="store",
                        dest="outfile",
                        nargs="?",
                        default=None,
                        help="SRT output filename",
                        )
    return parser

#----------------------------------------------------------------------
if __name__ == '__main__':
    # parse arguments
    args = arg_parser().parse_args()

    # parse XML file
    subsxml = SubsXML(args.input_xml)
    subsxml.parse()

    # write to file / display
    if args.outfile is not None:
        print "Writing to %s ..." % args.outfile,
        subsxml.write_to_file(args.outfile)
        print "done"
    else:
        subsxml.write_to_disp()
