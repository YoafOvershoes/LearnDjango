from datetime import datetime

import pytz
from neomodel import StructuredRel, DateTimeProperty


class DataRecoveryRelation(StructuredRel):
    since = DateTimeProperty(
        default=lambda: datetime.now(pytz.utc)
    )
