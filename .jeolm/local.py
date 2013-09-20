import re

from jeolm.inrecords import InrecordReviewer as OriginalReviewer
from jeolm.driver import Driver as OriginalDriver

import logging
logger = logging.getLogger(__name__)

class Driver(OriginalDriver):
    def filter_autofluid(self, inpath, inrecord, *, fluid_opt):
        if fluid_opt.get('exclude test', False):
            if inrecord.get('$test', False):
                return False
        return super().filter_autofluid(inpath, inrecord,
            fluid_opt=fluid_opt )

    def extract_inrecord_caption(self, inpath, inrecord):
        caption = super().extract_inrecord_caption(inpath, inrecord)
        if inrecord.get('$test', False):
            caption = r'\textinterrobang\ ' + caption
        return caption


