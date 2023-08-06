"""
This module contains the actions used in the Toolbox (lower left section
of the main window.

The Toolbox is bound to a diagram. When a diagram page (tab) is switched,
the actions bound to the toolbuttons should change as well.
"""

from typing import Callable, NamedTuple, Optional, Sequence, Tuple

from gaphor.core.modeling import Diagram, Presentation

ItemFactory = Callable[[Diagram, Optional[Presentation]], Presentation]


class ToolDef(NamedTuple):
    id: str
    name: str
    icon_name: str
    shortcut: Optional[str]
    item_factory: Optional[ItemFactory]
    handle_index: int = -1


ToolboxDefinition = Sequence[Tuple[str, Sequence[ToolDef]]]
