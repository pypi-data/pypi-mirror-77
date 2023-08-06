# -*- coding: utf-8 -*-
# File generated according to Generator/ClassesRef/Mesh/MeshSolution.csv
# WARNING! All changes made in this file will be lost!
"""Method code available at https://github.com/Eomys/pyleecan/tree/master/pyleecan/Methods/Mesh/MeshSolution
"""

from os import linesep
from logging import getLogger
from ._check import check_var, raise_
from ..Functions.get_logger import get_logger
from ..Functions.save import save
from ._frozen import FrozenClass

# Import all class method
# Try/catch to remove unnecessary dependencies in unused method
try:
    from ..Methods.Mesh.MeshSolution.get_mesh import get_mesh
except ImportError as error:
    get_mesh = error

try:
    from ..Methods.Mesh.MeshSolution.get_solution import get_solution
except ImportError as error:
    get_solution = error

try:
    from ..Methods.Mesh.MeshSolution.get_field import get_field
except ImportError as error:
    get_field = error

try:
    from ..Methods.Mesh.MeshSolution.plot_mesh import plot_mesh
except ImportError as error:
    plot_mesh = error

try:
    from ..Methods.Mesh.MeshSolution.plot_contour import plot_contour
except ImportError as error:
    plot_contour = error

try:
    from ..Methods.Mesh.MeshSolution.plot_deflection import plot_deflection
except ImportError as error:
    plot_deflection = error

try:
    from ..Methods.Mesh.MeshSolution.plot_deflection_animated import (
        plot_deflection_animated,
    )
except ImportError as error:
    plot_deflection_animated = error

try:
    from ..Methods.Mesh.MeshSolution.plot_glyph import plot_glyph
except ImportError as error:
    plot_glyph = error

try:
    from ..Methods.Mesh.MeshSolution.get_group import get_group
except ImportError as error:
    get_group = error


from numpy import array, empty
from ._check import InitUnKnowClassError
from .Mesh import Mesh
from .Solution import Solution


class MeshSolution(FrozenClass):
    """Abstract class to associate a mesh with one or several solutions"""

    VERSION = 1

    # Check ImportError to remove unnecessary dependencies in unused method
    # cf Methods.Mesh.MeshSolution.get_mesh
    if isinstance(get_mesh, ImportError):
        get_mesh = property(
            fget=lambda x: raise_(
                ImportError("Can't use MeshSolution method get_mesh: " + str(get_mesh))
            )
        )
    else:
        get_mesh = get_mesh
    # cf Methods.Mesh.MeshSolution.get_solution
    if isinstance(get_solution, ImportError):
        get_solution = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use MeshSolution method get_solution: " + str(get_solution)
                )
            )
        )
    else:
        get_solution = get_solution
    # cf Methods.Mesh.MeshSolution.get_field
    if isinstance(get_field, ImportError):
        get_field = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use MeshSolution method get_field: " + str(get_field)
                )
            )
        )
    else:
        get_field = get_field
    # cf Methods.Mesh.MeshSolution.plot_mesh
    if isinstance(plot_mesh, ImportError):
        plot_mesh = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use MeshSolution method plot_mesh: " + str(plot_mesh)
                )
            )
        )
    else:
        plot_mesh = plot_mesh
    # cf Methods.Mesh.MeshSolution.plot_contour
    if isinstance(plot_contour, ImportError):
        plot_contour = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use MeshSolution method plot_contour: " + str(plot_contour)
                )
            )
        )
    else:
        plot_contour = plot_contour
    # cf Methods.Mesh.MeshSolution.plot_deflection
    if isinstance(plot_deflection, ImportError):
        plot_deflection = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use MeshSolution method plot_deflection: "
                    + str(plot_deflection)
                )
            )
        )
    else:
        plot_deflection = plot_deflection
    # cf Methods.Mesh.MeshSolution.plot_deflection_animated
    if isinstance(plot_deflection_animated, ImportError):
        plot_deflection_animated = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use MeshSolution method plot_deflection_animated: "
                    + str(plot_deflection_animated)
                )
            )
        )
    else:
        plot_deflection_animated = plot_deflection_animated
    # cf Methods.Mesh.MeshSolution.plot_glyph
    if isinstance(plot_glyph, ImportError):
        plot_glyph = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use MeshSolution method plot_glyph: " + str(plot_glyph)
                )
            )
        )
    else:
        plot_glyph = plot_glyph
    # cf Methods.Mesh.MeshSolution.get_group
    if isinstance(get_group, ImportError):
        get_group = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use MeshSolution method get_group: " + str(get_group)
                )
            )
        )
    else:
        get_group = get_group
    # save method is available in all object
    save = save

    # generic copy method
    def copy(self):
        """Return a copy of the class
        """
        return type(self)(init_dict=self.as_dict())

    # get_logger method is available in all object
    get_logger = get_logger

    def __init__(
        self,
        label=None,
        mesh=list(),
        is_same_mesh=True,
        solution=list(),
        dimension=3,
        group=dict(),
        init_dict=None,
        init_str=None,
    ):
        """Constructor of the class. Can be use in three ways :
        - __init__ (arg1 = 1, arg3 = 5) every parameters have name and default values
            for Matrix, None will initialise the property with an empty Matrix
            for pyleecan type, None will call the default constructor
        - __init__ (init_dict = d) d must be a dictionnary with every properties as keys
        - __init__ (init_str = s) s must be a string
        s is the file path to load

        ndarray or list can be given for Vector and Matrix
        object or dict can be given for pyleecan Object"""

        if init_str is not None:  # Initialisation by str
            from ..Functions.load import load

            assert type(init_str) is str
            # load the object from a file
            obj = load(init_str)
            assert type(obj) is type(self)
            label = obj.label
            mesh = obj.mesh
            is_same_mesh = obj.is_same_mesh
            solution = obj.solution
            dimension = obj.dimension
            group = obj.group
        if init_dict is not None:  # Initialisation by dict
            assert type(init_dict) is dict
            # Overwrite default value with init_dict content
            if "label" in list(init_dict.keys()):
                label = init_dict["label"]
            if "mesh" in list(init_dict.keys()):
                mesh = init_dict["mesh"]
            if "is_same_mesh" in list(init_dict.keys()):
                is_same_mesh = init_dict["is_same_mesh"]
            if "solution" in list(init_dict.keys()):
                solution = init_dict["solution"]
            if "dimension" in list(init_dict.keys()):
                dimension = init_dict["dimension"]
            if "group" in list(init_dict.keys()):
                group = init_dict["group"]
        # Initialisation by argument
        self.parent = None
        self.label = label
        # mesh can be None or a list of Mesh object
        self.mesh = list()
        if type(mesh) is list:
            for obj in mesh:
                if obj is None:  # Default value
                    self.mesh.append(Mesh())
                elif isinstance(obj, dict):
                    # Check that the type is correct (including daughter)
                    class_name = obj.get("__class__")
                    if class_name not in ["Mesh", "MeshMat", "MeshVTK"]:
                        raise InitUnKnowClassError(
                            "Unknow class name " + class_name + " in init_dict for mesh"
                        )
                    # Dynamic import to call the correct constructor
                    module = __import__(
                        "pyleecan.Classes." + class_name, fromlist=[class_name]
                    )
                    class_obj = getattr(module, class_name)
                    self.mesh.append(class_obj(init_dict=obj))
                else:
                    self.mesh.append(obj)
        elif mesh is None:
            self.mesh = list()
        else:
            self.mesh = mesh
        self.is_same_mesh = is_same_mesh
        # solution can be None or a list of Solution object
        self.solution = list()
        if type(solution) is list:
            for obj in solution:
                if obj is None:  # Default value
                    self.solution.append(Solution())
                elif isinstance(obj, dict):
                    # Check that the type is correct (including daughter)
                    class_name = obj.get("__class__")
                    if class_name not in [
                        "Solution",
                        "Mode",
                        "SolutionData",
                        "SolutionMat",
                        "SolutionVector",
                    ]:
                        raise InitUnKnowClassError(
                            "Unknow class name "
                            + class_name
                            + " in init_dict for solution"
                        )
                    # Dynamic import to call the correct constructor
                    module = __import__(
                        "pyleecan.Classes." + class_name, fromlist=[class_name]
                    )
                    class_obj = getattr(module, class_name)
                    self.solution.append(class_obj(init_dict=obj))
                else:
                    self.solution.append(obj)
        elif solution is None:
            self.solution = list()
        else:
            self.solution = solution
        self.dimension = dimension
        # group can be None or a dict of ndarray
        self.group = dict()
        if type(group) is dict:
            for key, obj in group.items():
                if obj is None:  # Default value
                    value = empty(0)
                elif isinstance(obj, list):
                    value = array(obj)
                self.group[key] = value
        elif group is None:
            self.group = dict()
        else:
            self.group = group  # Should raise an error

        # The class is frozen, for now it's impossible to add new properties
        self._freeze()

    def __str__(self):
        """Convert this objet in a readeable string (for print)"""

        MeshSolution_str = ""
        if self.parent is None:
            MeshSolution_str += "parent = None " + linesep
        else:
            MeshSolution_str += (
                "parent = " + str(type(self.parent)) + " object" + linesep
            )
        MeshSolution_str += 'label = "' + str(self.label) + '"' + linesep
        if len(self.mesh) == 0:
            MeshSolution_str += "mesh = []" + linesep
        for ii in range(len(self.mesh)):
            tmp = self.mesh[ii].__str__().replace(linesep, linesep + "\t") + linesep
            MeshSolution_str += "mesh[" + str(ii) + "] =" + tmp + linesep + linesep
        MeshSolution_str += "is_same_mesh = " + str(self.is_same_mesh) + linesep
        if len(self.solution) == 0:
            MeshSolution_str += "solution = []" + linesep
        for ii in range(len(self.solution)):
            tmp = self.solution[ii].__str__().replace(linesep, linesep + "\t") + linesep
            MeshSolution_str += "solution[" + str(ii) + "] =" + tmp + linesep + linesep
        MeshSolution_str += "dimension = " + str(self.dimension) + linesep
        if len(self.group) == 0:
            MeshSolution_str += "group = dict()"
        for key, obj in self.group.items():
            MeshSolution_str += (
                "group[" + key + "] = " + str(self.group[key]) + linesep + linesep
            )
        return MeshSolution_str

    def __eq__(self, other):
        """Compare two objects (skip parent)"""

        if type(other) != type(self):
            return False
        if other.label != self.label:
            return False
        if other.mesh != self.mesh:
            return False
        if other.is_same_mesh != self.is_same_mesh:
            return False
        if other.solution != self.solution:
            return False
        if other.dimension != self.dimension:
            return False
        if other.group != self.group:
            return False
        return True

    def as_dict(self):
        """Convert this objet in a json seriable dict (can be use in __init__)
        """

        MeshSolution_dict = dict()
        MeshSolution_dict["label"] = self.label
        MeshSolution_dict["mesh"] = list()
        for obj in self.mesh:
            MeshSolution_dict["mesh"].append(obj.as_dict())
        MeshSolution_dict["is_same_mesh"] = self.is_same_mesh
        MeshSolution_dict["solution"] = list()
        for obj in self.solution:
            MeshSolution_dict["solution"].append(obj.as_dict())
        MeshSolution_dict["dimension"] = self.dimension
        MeshSolution_dict["group"] = dict()
        for key, obj in self.group.items():
            MeshSolution_dict["group"][key] = obj.tolist()
        # The class name is added to the dict fordeserialisation purpose
        MeshSolution_dict["__class__"] = "MeshSolution"
        return MeshSolution_dict

    def _set_None(self):
        """Set all the properties to None (except pyleecan object)"""

        self.label = None
        for obj in self.mesh:
            obj._set_None()
        self.is_same_mesh = None
        for obj in self.solution:
            obj._set_None()
        self.dimension = None
        self.group = dict()

    def _get_label(self):
        """getter of label"""
        return self._label

    def _set_label(self, value):
        """setter of label"""
        check_var("label", value, "str")
        self._label = value

    label = property(
        fget=_get_label,
        fset=_set_label,
        doc=u"""(Optional) Descriptive name of the mesh

        :Type: str
        """,
    )

    def _get_mesh(self):
        """getter of mesh"""
        for obj in self._mesh:
            if obj is not None:
                obj.parent = self
        return self._mesh

    def _set_mesh(self, value):
        """setter of mesh"""
        check_var("mesh", value, "[Mesh]")
        self._mesh = value

        for obj in self._mesh:
            if obj is not None:
                obj.parent = self

    mesh = property(
        fget=_get_mesh,
        fset=_set_mesh,
        doc=u"""A list of Mesh objects. 

        :Type: [Mesh]
        """,
    )

    def _get_is_same_mesh(self):
        """getter of is_same_mesh"""
        return self._is_same_mesh

    def _set_is_same_mesh(self, value):
        """setter of is_same_mesh"""
        check_var("is_same_mesh", value, "bool")
        self._is_same_mesh = value

    is_same_mesh = property(
        fget=_get_is_same_mesh,
        fset=_set_is_same_mesh,
        doc=u"""1 if the mesh is the same at each step (time, mode etc.)

        :Type: bool
        """,
    )

    def _get_solution(self):
        """getter of solution"""
        for obj in self._solution:
            if obj is not None:
                obj.parent = self
        return self._solution

    def _set_solution(self, value):
        """setter of solution"""
        check_var("solution", value, "[Solution]")
        self._solution = value

        for obj in self._solution:
            if obj is not None:
                obj.parent = self

    solution = property(
        fget=_get_solution,
        fset=_set_solution,
        doc=u"""A list of Solution objects

        :Type: [Solution]
        """,
    )

    def _get_dimension(self):
        """getter of dimension"""
        return self._dimension

    def _set_dimension(self, value):
        """setter of dimension"""
        check_var("dimension", value, "int", Vmin=1, Vmax=3)
        self._dimension = value

    dimension = property(
        fget=_get_dimension,
        fset=_set_dimension,
        doc=u"""Dimension of the physical problem

        :Type: int
        :min: 1
        :max: 3
        """,
    )

    def _get_group(self):
        """getter of group"""
        return self._group

    def _set_group(self, value):
        """setter of group"""
        if type(value) is dict:
            for key, obj in value.items():
                if obj is None:
                    obj = array([])
                elif type(obj) is list:
                    try:
                        obj = array(obj)
                    except:
                        pass
        check_var("group", value, "{ndarray}")
        self._group = value

    group = property(
        fget=_get_group,
        fset=_set_group,
        doc=u"""Dict sorted by groups name with cells indices. 

        :Type: {ndarray}
        """,
    )
