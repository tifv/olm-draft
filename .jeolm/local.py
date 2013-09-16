import re

from jeolm.inrecords import InrecordReviewer as OriginalReviewer
from jeolm.driver import Driver as OriginalDriver

import logging
logger = logging.getLogger(__name__)

class InrecordReviewer(OriginalReviewer):
    def review_tex_content(self, inpath, inrecord, s):
        super().review_tex_content(inpath, inrecord, s)
        self.review_tex_content_test(inpath, inrecord, s)

    def review_tex_content_test(self, inpath, inrecord, s):
        if self.test_pattern.search(s) is not None:
            inrecord['$test'] = True
        else:
            inrecord.pop('$test', None)

    test_pattern = re.compile(
        r'(?m)^% test$' )

class Driver(OriginalDriver):
    def constitute_input(self, inpath, *, inrecord, **kwargs):
        if inrecord.pop('$test', False):
            inrecord['$caption'] = r'\textinterrobang\ ' + inrecord['$caption']
        return super().constitute_input(inpath, inrecord=inrecord, **kwargs)


