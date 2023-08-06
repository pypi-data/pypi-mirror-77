from gaphor import UML
from gaphor.diagram.grouping import AbstractGroup, Group
from gaphor.UML.actions.action import ActionItem
from gaphor.UML.actions.activitynodes import ActivityNodeItem, ForkNodeItem
from gaphor.UML.actions.objectnode import ObjectNodeItem
from gaphor.UML.actions.partition import PartitionItem


@Group.register(PartitionItem, PartitionItem)
class ActivityPartitionsGroup(AbstractGroup):
    """
    Group activity partitions.
    """

    def can_contain(self):
        return not self.parent.subject or (
            self.parent.subject and len(self.parent.subject.node) == 0
        )

    def group(self):
        assert self.item.canvas

        p = self.parent.subject
        model = self.item.model
        sp = model.create(UML.ActivityPartition)
        self.item.subject = sp
        sp.name = "Swimlane"
        if p:
            p.subpartition = sp
        for k in self.item.canvas.get_children(self.item):
            sp.subpartition = k.subject

    def ungroup(self):
        assert self.item.canvas

        p = self.parent.subject
        sp = self.item.subject
        if p:
            p.subpartition.remove(sp)
        self.item.subject = None
        for s in sp.subpartition:
            sp.subpartition.remove(s)
        assert len(sp.node) == 0

        # ungroup activity nodes
        canvas = self.item.canvas
        nodes = [
            n
            for n in canvas.get_children(self.item)
            if isinstance(
                n, (ActivityNodeItem, ActionItem, ObjectNodeItem, ForkNodeItem)
            )
        ]
        for n in nodes:
            canvas.reparent(n, None)

        sp.unlink()


class ActivityNodePartitionGroup(AbstractGroup):
    """
    Group activity nodes within activity partition.
    """

    def can_contain(self):
        return self.parent.subject and len(self.parent.subject.subpartition) == 0

    def group(self):
        partition = self.parent.subject
        node = self.item.subject
        partition.node = node

    def ungroup(self):
        partition = self.parent.subject
        node = self.item.subject
        partition.node.remove(node)


Group.register(PartitionItem, ActivityNodeItem)(ActivityNodePartitionGroup)
Group.register(PartitionItem, ActionItem)(ActivityNodePartitionGroup)
Group.register(PartitionItem, ObjectNodeItem)(ActivityNodePartitionGroup)
Group.register(PartitionItem, ForkNodeItem)(ActivityNodePartitionGroup)
