"""
Use case extension relationship.
"""

from gaphor import UML
from gaphor.diagram.presentation import LinePresentation
from gaphor.diagram.shapes import Text, draw_arrow_head
from gaphor.diagram.support import represents
from gaphor.UML.modelfactory import stereotypes_str


@represents(UML.Extend)
class ExtendItem(LinePresentation):
    """
    Use case extension relationship.
    """

    def __init__(self, id=None, model=None):
        super().__init__(id, model, style={"dash-style": (7.0, 5.0)})

        self.shape_middle = Text(
            text=lambda: stereotypes_str(self.subject, ("extend",)),
        )
        self.watch("subject.appliedStereotype.classifier.name")
        self.draw_head = draw_arrow_head
