"""
Tests for grouping functionality in Gaphor.
"""

from gaphor import UML
from gaphor.tests import TestCase
from gaphor.UML.actions import ActionItem, PartitionItem


class PartitionGroupTestCase(TestCase):
    def test_no_subpartition_when_nodes_in(self):
        """Test adding subpartition when nodes added
        """
        p = self.create(PartitionItem)
        a1 = self.create(ActionItem, UML.Action)
        p1 = self.create(PartitionItem)
        p2 = self.create(PartitionItem)

        self.group(p, p1)
        self.group(p1, a1)
        assert not self.can_group(p1, p2)

    def test_no_nodes_when_subpartition_in(self):
        """Test adding nodes when subpartition added
        """
        p = self.create(PartitionItem)
        a1 = self.create(ActionItem, UML.Action)
        p1 = self.create(PartitionItem)

        self.group(p, p1)
        assert not self.can_group(p, a1)

    def test_action_grouping(self):
        """Test adding action to partition
        """
        p1 = self.create(PartitionItem)
        p2 = self.create(PartitionItem)
        a1 = self.create(ActionItem, UML.Action)
        a2 = self.create(ActionItem, UML.Action)

        assert not self.can_group(p1, a1)  # cannot add to dimension

        self.group(p1, p2)
        self.group(p2, a1)

        assert self.can_group(p2, a1)
        assert len(p2.subject.node) == 1
        self.group(p2, a2)
        assert len(p2.subject.node) == 2

    def test_subpartition_grouping(self):
        """Test adding subpartition to partition
        """
        p = self.create(PartitionItem)
        p1 = self.create(PartitionItem)
        p2 = self.create(PartitionItem)

        self.group(p, p1)
        assert p.subject is None
        assert p1.subject is not None

        self.group(p, p2)
        assert p.subject is None
        assert p2.subject is not None

    def test_ungrouping(self):
        """Test action and subpartition removal
        """
        p1 = self.create(PartitionItem)
        p2 = self.create(PartitionItem)
        a1 = self.create(ActionItem, UML.Action)
        a2 = self.create(ActionItem, UML.Action)

        self.group(p1, p2)

        # group to p2, it is disallowed to p1
        self.group(p2, a1)
        self.group(p2, a2)

        self.ungroup(p2, a1)
        assert len(p2.subject.node) == 1
        self.ungroup(p2, a2)
        assert len(p2.subject.node) == 0

        self.ungroup(p1, p2)
        assert p1.subject is None, p1.subject
        assert p2.subject is None, p2.subject
        assert len(self.kindof(UML.ActivityPartition)) == 0

    def test_ungrouping_with_actions(self):
        """Test subpartition with actions removal
        """
        p1 = self.create(PartitionItem)
        p2 = self.create(PartitionItem)
        a1 = self.create(ActionItem, UML.Action)
        a2 = self.create(ActionItem, UML.Action)

        self.group(p1, p2)

        # group to p2, it is disallowed to p1
        self.group(p2, a1)
        self.group(p2, a2)

        partition = p2.subject
        assert len(partition.node) == 2, partition.node
        assert len(p2.canvas.get_children(p2)) == 2, p2.canvas.get_children(p2)

        self.ungroup(p1, p2)

        assert 0 == len(partition.node)
        assert len(p2.canvas.get_children(p2)) == 0
        assert len(partition.node) == 0

    def test_nested_subpartition_ungrouping(self):
        """Test removal of subpartition with swimlanes
        """
        p1 = self.create(PartitionItem)
        p2 = self.create(PartitionItem)
        p3 = self.create(PartitionItem)
        p4 = self.create(PartitionItem)

        self.group(p1, p2)
        self.group(p2, p3)
        self.group(p2, p4)
        assert p2.subject is not None, p2.subject
        assert p3.subject is not None, p3.subject
        assert p4.subject is not None, p4.subject

        self.ungroup(p1, p2)
        assert p1.subject is None, p1.subject
        assert p2.subject is None, p2.subject
        assert p3.subject is not None, p3.subject
        assert p4.subject is not None, p4.subject
        assert len(self.kindof(UML.ActivityPartition)) == 2

    def test_nested_subpartition_regrouping(self):
        """Test regrouping of subpartition with swimlanes
        """
        p1 = self.create(PartitionItem)
        p2 = self.create(PartitionItem)
        p3 = self.create(PartitionItem)
        p4 = self.create(PartitionItem)

        self.group(p1, p2)
        self.group(p2, p3)
        self.group(p2, p4)
        assert p2.subject is not None, p2.subject
        assert p3.subject is not None, p3.subject
        assert p4.subject is not None, p4.subject

        self.ungroup(p1, p2)
        assert p1.subject is None, p1.subject
        assert p2.subject is None, p2.subject
        assert p3.subject is not None, p3.subject
        assert p4.subject is not None, p4.subject
        assert len(self.kindof(UML.ActivityPartition)) == 2

        self.group(p1, p2)
        assert len(self.kindof(UML.ActivityPartition)) == 3
        assert p2.subject is not None, p2.subject
        assert p3.subject is not None, p3.subject
        assert p4.subject is not None, p4.subject
        assert p3.subject in p2.subject.subpartition, p2.subject.subpartition
        assert p4.subject in p2.subject.subpartition, p2.subject.subpartition
