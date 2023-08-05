from typing import Optional
import attr

from .action_abstract_test_summary import ActionAbstractTestSummary
from . import helpers


@attr.s
class ActionTestSummaryIdentifiableObject(ActionAbstractTestSummary):
    identifier: Optional[str] = attr.ib()

    @classmethod
    def convert_identifier_field(cls, report: dict) -> Optional[str]:
        return helpers.string_from_report(report.get("identifier"), dict(default=None))
