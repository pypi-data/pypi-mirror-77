"""
Classes related adapter connection tests.
"""

from gaphor import UML
from gaphor.tests import TestCase
from gaphor.UML.classes.dependency import DependencyItem
from gaphor.UML.classes.generalization import GeneralizationItem
from gaphor.UML.classes.interface import InterfaceItem
from gaphor.UML.classes.klass import ClassItem
from gaphor.UML.usecases.actor import ActorItem


class DependencyTestCase(TestCase):
    """
    Dependency item connection adapter tests.
    """

    def test_dependency_glue(self):
        """Test dependency glue to two actor items
        """
        actor1 = self.create(ActorItem, UML.Actor)
        actor2 = self.create(ActorItem, UML.Actor)
        dep = self.create(DependencyItem)

        glued = self.allow(dep, dep.head, actor1)
        assert glued

        self.connect(dep, dep.head, actor1)

        glued = self.allow(dep, dep.tail, actor2)
        assert glued

    def test_dependency_connect(self):
        """Test dependency connecting to two actor items
        """
        actor1 = self.create(ActorItem, UML.Actor)
        actor2 = self.create(ActorItem, UML.Actor)
        dep = self.create(DependencyItem)

        self.connect(dep, dep.head, actor1)
        self.connect(dep, dep.tail, actor2)

        assert dep.subject is not None
        assert isinstance(dep.subject, UML.Dependency)
        assert dep.subject in self.element_factory.select()

        hct = self.get_connected(dep.head)
        tct = self.get_connected(dep.tail)
        assert hct is actor1
        assert tct is actor2

        assert actor1.subject in dep.subject.supplier
        assert actor2.subject in dep.subject.client

    def test_dependency_reconnection(self):
        """Test dependency reconnection
        """
        a1 = self.create(ActorItem, UML.Actor)
        a2 = self.create(ActorItem, UML.Actor)
        a3 = self.create(ActorItem, UML.Actor)
        dep = self.create(DependencyItem)

        # connect: a1 -> a2
        self.connect(dep, dep.head, a1)
        self.connect(dep, dep.tail, a2)

        d = dep.subject

        # reconnect: a1 -> a3
        self.connect(dep, dep.tail, a3)

        assert d is dep.subject
        assert len(dep.subject.supplier) == 1
        assert len(dep.subject.client) == 1
        assert a1.subject in dep.subject.supplier
        assert a3.subject in dep.subject.client
        assert a2.subject not in dep.subject.client, dep.subject.client

    def test_dependency_disconnect(self):
        """Test dependency disconnecting using two actor items
        """
        actor1 = self.create(ActorItem, UML.Actor)
        actor2 = self.create(ActorItem, UML.Actor)
        dep = self.create(DependencyItem)

        self.connect(dep, dep.head, actor1)
        self.connect(dep, dep.tail, actor2)

        dep_subj = dep.subject
        self.disconnect(dep, dep.tail)

        assert dep.subject is None
        assert self.get_connected(dep.tail) is None
        assert dep_subj not in self.element_factory.select()
        assert dep_subj not in actor1.subject.supplierDependency
        assert dep_subj not in actor2.subject.clientDependency

    def test_dependency_reconnect(self):
        """Test dependency reconnection using two actor items
        """
        actor1 = self.create(ActorItem, UML.Actor)
        actor2 = self.create(ActorItem, UML.Actor)
        dep = self.create(DependencyItem)

        self.connect(dep, dep.head, actor1)
        self.connect(dep, dep.tail, actor2)

        dep_subj = dep.subject
        self.disconnect(dep, dep.tail)

        # reconnect
        self.connect(dep, dep.tail, actor2)

        assert dep.subject is not None
        assert dep.subject is not dep_subj  # the old subject has been deleted
        assert dep.subject in actor1.subject.supplierDependency
        assert dep.subject in actor2.subject.clientDependency
        # TODO: test with interface (usage) and component (realization)
        # TODO: test with multiple diagrams (should reuse existing relationships first)

    def test_multi_dependency(self):
        """Test multiple dependencies

        Dependency should appear in a new diagram, bound on a new
        dependency item.
        """
        actoritem1 = self.create(ActorItem, UML.Actor)
        actoritem2 = self.create(ActorItem, UML.Actor)
        actor1 = actoritem1.subject
        actor2 = actoritem2.subject
        dep = self.create(DependencyItem)

        self.connect(dep, dep.head, actoritem1)
        self.connect(dep, dep.tail, actoritem2)

        assert dep.subject
        assert 1 == len(actor1.supplierDependency)
        assert actor1.supplierDependency[0] is dep.subject
        assert 1 == len(actor2.clientDependency)
        assert actor2.clientDependency[0] is dep.subject

        # Do the same thing, but now on a new diagram:

        diagram2 = self.element_factory.create(UML.Diagram)
        actoritem3 = diagram2.create(ActorItem, subject=actor1)
        actoritem4 = diagram2.create(ActorItem, subject=actor2)
        dep2 = diagram2.create(DependencyItem)

        self.connect(dep2, dep2.head, actoritem3)
        cinfo = diagram2.canvas.get_connection(dep2.head)
        assert cinfo is not None
        assert cinfo.connected is actoritem3
        self.connect(dep2, dep2.tail, actoritem4)
        assert dep2.subject is not None
        assert 1 == len(actor1.supplierDependency)
        assert actor1.supplierDependency[0] is dep.subject
        assert 1 == len(actor2.clientDependency)
        assert actor2.clientDependency[0] is dep.subject

        assert dep.subject is dep2.subject

    def test_dependency_type_auto(self):
        """Test dependency type automatic determination
        """
        cls = self.create(ClassItem, UML.Class)
        iface = self.create(InterfaceItem, UML.Interface)
        dep = self.create(DependencyItem)

        assert dep.auto_dependency

        self.connect(dep, dep.tail, cls)  # connect client
        self.connect(dep, dep.head, iface)  # connect supplier

        assert dep.subject is not None
        assert isinstance(dep.subject, UML.Usage), dep.subject
        assert dep.subject in self.element_factory.select()


class GeneralizationTestCase(TestCase):
    """
    Generalization item connection adapter tests.
    """

    def test_glue(self):
        """Test generalization item gluing using two classes."""

        gen = self.create(GeneralizationItem)
        c1 = self.create(ClassItem, UML.Class)
        c2 = self.create(ClassItem, UML.Class)

        glued = self.allow(gen, gen.tail, c1)
        assert glued

        self.connect(gen, gen.tail, c1)
        assert self.get_connected(gen.tail) is c1
        assert gen.subject is None

        glued = self.allow(gen, gen.head, c2)
        assert glued

    def test_connection(self):
        """Test generalization item connection using two classes
        """
        gen = self.create(GeneralizationItem)
        c1 = self.create(ClassItem, UML.Class)
        c2 = self.create(ClassItem, UML.Class)

        self.connect(gen, gen.tail, c1)
        assert self.get_connected(gen.tail) is c1

        self.connect(gen, gen.head, c2)
        assert gen.subject is not None
        assert gen.subject.general is c2.subject
        assert gen.subject.specific is c1.subject

    def test_reconnection(self):
        """Test generalization item connection using two classes

        On reconnection a new Generalization is created.
        """
        gen = self.create(GeneralizationItem)
        c1 = self.create(ClassItem, UML.Class)
        c2 = self.create(ClassItem, UML.Class)

        self.connect(gen, gen.tail, c1)
        assert self.get_connected(gen.tail) is c1

        self.connect(gen, gen.head, c2)
        assert gen.subject is not None
        assert gen.subject.general is c2.subject
        assert gen.subject.specific is c1.subject

        # Now do the same on a new diagram:
        diagram2 = self.element_factory.create(UML.Diagram)
        c3 = diagram2.create(ClassItem, subject=c1.subject)
        c4 = diagram2.create(ClassItem, subject=c2.subject)
        gen2 = diagram2.create(GeneralizationItem)

        self.connect(gen2, gen2.head, c3)
        cinfo = diagram2.canvas.get_connection(gen2.head)
        assert cinfo is not None
        assert cinfo.connected is c3

        self.connect(gen2, gen2.tail, c4)
        assert gen.subject is not gen2.subject
        assert len(c1.subject.generalization) == 1
        assert c1.subject.generalization[0] is gen.subject
        # self.assertEqual(1, len(actor2.clientDependency))
        # self.assertTrue(actor2.clientDependency[0] is dep.subject)

    def test_reconnection2(self):
        """Test reconnection of generalization
        """
        c1 = self.create(ClassItem, UML.Class)
        c2 = self.create(ClassItem, UML.Class)
        c3 = self.create(ClassItem, UML.Class)
        gen = self.create(GeneralizationItem)

        # connect: c1 -> c2
        self.connect(gen, gen.head, c1)
        self.connect(gen, gen.tail, c2)

        s = gen.subject

        # reconnect: c2 -> c3
        self.connect(gen, gen.tail, c3)

        assert s is gen.subject
        assert c1.subject is gen.subject.general
        assert c3.subject is gen.subject.specific
        assert c2.subject is not gen.subject.specific
