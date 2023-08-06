# -*- coding: utf-8 -*-
# File generated according to Generator/ClassesRef/Machine/Conductor.csv
# WARNING! All changes made in this file will be lost!
"""Method code available at https://github.com/Eomys/pyleecan/tree/master/pyleecan/Methods/Machine/Conductor
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
    from ..Methods.Machine.Conductor.check import check
except ImportError as error:
    check = error


from ._check import InitUnKnowClassError
from .Material import Material


class Conductor(FrozenClass):
    """abstact class for conductors"""

    VERSION = 1

    # cf Methods.Machine.Conductor.check
    if isinstance(check, ImportError):
        check = property(
            fget=lambda x: raise_(
                ImportError("Can't use Conductor method check: " + str(check))
            )
        )
    else:
        check = check
    # save method is available in all object
    save = save

    # generic copy method
    def copy(self):
        """Return a copy of the class
        """
        return type(self)(init_dict=self.as_dict())

    # get_logger method is available in all object
    get_logger = get_logger

    def __init__(self, cond_mat=-1, ins_mat=-1, init_dict=None, init_str=None):
        """Constructor of the class. Can be use in three ways :
        - __init__ (arg1 = 1, arg3 = 5) every parameters have name and default values
            for Matrix, None will initialise the property with an empty Matrix
            for pyleecan type, None will call the default constructor
        - __init__ (init_dict = d) d must be a dictionnary with every properties as keys
        - __init__ (init_str = s) s must be a string
        s is the file path to load

        ndarray or list can be given for Vector and Matrix
        object or dict can be given for pyleecan Object"""

        if cond_mat == -1:
            cond_mat = Material()
        if ins_mat == -1:
            ins_mat = Material()
        if init_str is not None:  # Initialisation by str
            from ..Functions.load import load

            assert type(init_str) is str
            # load the object from a file
            obj = load(init_str)
            assert type(obj) is type(self)
            cond_mat = obj.cond_mat
            ins_mat = obj.ins_mat
        if init_dict is not None:  # Initialisation by dict
            assert type(init_dict) is dict
            # Overwrite default value with init_dict content
            if "cond_mat" in list(init_dict.keys()):
                cond_mat = init_dict["cond_mat"]
            if "ins_mat" in list(init_dict.keys()):
                ins_mat = init_dict["ins_mat"]
        # Initialisation by argument
        self.parent = None
        # cond_mat can be None, a Material object or a dict
        if isinstance(cond_mat, dict):
            self.cond_mat = Material(init_dict=cond_mat)
        elif isinstance(cond_mat, str):
            from ..Functions.load import load

            self.cond_mat = load(cond_mat)
        else:
            self.cond_mat = cond_mat
        # ins_mat can be None, a Material object or a dict
        if isinstance(ins_mat, dict):
            self.ins_mat = Material(init_dict=ins_mat)
        elif isinstance(ins_mat, str):
            from ..Functions.load import load

            self.ins_mat = load(ins_mat)
        else:
            self.ins_mat = ins_mat

        # The class is frozen, for now it's impossible to add new properties
        self._freeze()

    def __str__(self):
        """Convert this objet in a readeable string (for print)"""

        Conductor_str = ""
        if self.parent is None:
            Conductor_str += "parent = None " + linesep
        else:
            Conductor_str += "parent = " + str(type(self.parent)) + " object" + linesep
        if self.cond_mat is not None:
            tmp = self.cond_mat.__str__().replace(linesep, linesep + "\t").rstrip("\t")
            Conductor_str += "cond_mat = " + tmp
        else:
            Conductor_str += "cond_mat = None" + linesep + linesep
        if self.ins_mat is not None:
            tmp = self.ins_mat.__str__().replace(linesep, linesep + "\t").rstrip("\t")
            Conductor_str += "ins_mat = " + tmp
        else:
            Conductor_str += "ins_mat = None" + linesep + linesep
        return Conductor_str

    def __eq__(self, other):
        """Compare two objects (skip parent)"""

        if type(other) != type(self):
            return False
        if other.cond_mat != self.cond_mat:
            return False
        if other.ins_mat != self.ins_mat:
            return False
        return True

    def as_dict(self):
        """Convert this objet in a json seriable dict (can be use in __init__)
        """

        Conductor_dict = dict()
        if self.cond_mat is None:
            Conductor_dict["cond_mat"] = None
        else:
            Conductor_dict["cond_mat"] = self.cond_mat.as_dict()
        if self.ins_mat is None:
            Conductor_dict["ins_mat"] = None
        else:
            Conductor_dict["ins_mat"] = self.ins_mat.as_dict()
        # The class name is added to the dict fordeserialisation purpose
        Conductor_dict["__class__"] = "Conductor"
        return Conductor_dict

    def _set_None(self):
        """Set all the properties to None (except pyleecan object)"""

        if self.cond_mat is not None:
            self.cond_mat._set_None()
        if self.ins_mat is not None:
            self.ins_mat._set_None()

    def _get_cond_mat(self):
        """getter of cond_mat"""
        return self._cond_mat

    def _set_cond_mat(self, value):
        """setter of cond_mat"""
        check_var("cond_mat", value, "Material")
        self._cond_mat = value

        if self._cond_mat is not None:
            self._cond_mat.parent = self

    cond_mat = property(
        fget=_get_cond_mat,
        fset=_set_cond_mat,
        doc=u"""Material of the conductor

        :Type: Material
        """,
    )

    def _get_ins_mat(self):
        """getter of ins_mat"""
        return self._ins_mat

    def _set_ins_mat(self, value):
        """setter of ins_mat"""
        check_var("ins_mat", value, "Material")
        self._ins_mat = value

        if self._ins_mat is not None:
            self._ins_mat.parent = self

    ins_mat = property(
        fget=_get_ins_mat,
        fset=_set_ins_mat,
        doc=u"""Material of the insulation

        :Type: Material
        """,
    )
