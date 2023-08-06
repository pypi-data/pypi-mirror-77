# -*- coding: utf-8 -*-
# File generated according to Generator/ClassesRef/Output/OutForce.csv
# WARNING! All changes made in this file will be lost!
"""Method code available at https://github.com/Eomys/pyleecan/tree/master/pyleecan/Methods/Output/OutForce
"""

from os import linesep
from logging import getLogger
from ._check import set_array, check_var, raise_
from ..Functions.get_logger import get_logger
from ..Functions.save import save
from ._frozen import FrozenClass

from numpy import array, array_equal
from cloudpickle import dumps, loads
from ._check import CheckTypeError

try:
    from SciDataTool.Classes.VectorField import VectorField
except ImportError:
    VectorField = ImportError
from ._check import InitUnKnowClassError


class OutForce(FrozenClass):
    """Gather the structural module outputs"""

    VERSION = 1

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
        time=None,
        angle=None,
        Nt_tot=None,
        Na_tot=None,
        P=None,
        logger_name="Pyleecan.OutStruct",
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
            time = obj.time
            angle = obj.angle
            Nt_tot = obj.Nt_tot
            Na_tot = obj.Na_tot
            P = obj.P
            logger_name = obj.logger_name
        if init_dict is not None:  # Initialisation by dict
            assert type(init_dict) is dict
            # Overwrite default value with init_dict content
            if "time" in list(init_dict.keys()):
                time = init_dict["time"]
            if "angle" in list(init_dict.keys()):
                angle = init_dict["angle"]
            if "Nt_tot" in list(init_dict.keys()):
                Nt_tot = init_dict["Nt_tot"]
            if "Na_tot" in list(init_dict.keys()):
                Na_tot = init_dict["Na_tot"]
            if "P" in list(init_dict.keys()):
                P = init_dict["P"]
            if "logger_name" in list(init_dict.keys()):
                logger_name = init_dict["logger_name"]
        # Initialisation by argument
        self.parent = None
        # time can be None, a ndarray or a list
        set_array(self, "time", time)
        # angle can be None, a ndarray or a list
        set_array(self, "angle", angle)
        self.Nt_tot = Nt_tot
        self.Na_tot = Na_tot
        # Check if the type VectorField has been imported with success
        if isinstance(VectorField, ImportError):
            raise ImportError("Unknown type VectorField please install SciDataTool")
        self.P = P
        self.logger_name = logger_name

        # The class is frozen, for now it's impossible to add new properties
        self._freeze()

    def __str__(self):
        """Convert this objet in a readeable string (for print)"""

        OutForce_str = ""
        if self.parent is None:
            OutForce_str += "parent = None " + linesep
        else:
            OutForce_str += "parent = " + str(type(self.parent)) + " object" + linesep
        OutForce_str += (
            "time = "
            + linesep
            + str(self.time).replace(linesep, linesep + "\t")
            + linesep
            + linesep
        )
        OutForce_str += (
            "angle = "
            + linesep
            + str(self.angle).replace(linesep, linesep + "\t")
            + linesep
            + linesep
        )
        OutForce_str += "Nt_tot = " + str(self.Nt_tot) + linesep
        OutForce_str += "Na_tot = " + str(self.Na_tot) + linesep
        OutForce_str += "P = " + str(self.P) + linesep + linesep
        OutForce_str += 'logger_name = "' + str(self.logger_name) + '"' + linesep
        return OutForce_str

    def __eq__(self, other):
        """Compare two objects (skip parent)"""

        if type(other) != type(self):
            return False
        if not array_equal(other.time, self.time):
            return False
        if not array_equal(other.angle, self.angle):
            return False
        if other.Nt_tot != self.Nt_tot:
            return False
        if other.Na_tot != self.Na_tot:
            return False
        if other.P != self.P:
            return False
        if other.logger_name != self.logger_name:
            return False
        return True

    def as_dict(self):
        """Convert this objet in a json seriable dict (can be use in __init__)
        """

        OutForce_dict = dict()
        if self.time is None:
            OutForce_dict["time"] = None
        else:
            OutForce_dict["time"] = self.time.tolist()
        if self.angle is None:
            OutForce_dict["angle"] = None
        else:
            OutForce_dict["angle"] = self.angle.tolist()
        OutForce_dict["Nt_tot"] = self.Nt_tot
        OutForce_dict["Na_tot"] = self.Na_tot
        if self.P is None:
            OutForce_dict["P"] = None
        else:  # Store serialized data (using cloudpickle) and str to read it in json save files
            OutForce_dict["P"] = {
                "__class__": str(type(self._P)),
                "__repr__": str(self._P.__repr__()),
                "serialized": dumps(self._P).decode("ISO-8859-2"),
            }
        OutForce_dict["logger_name"] = self.logger_name
        # The class name is added to the dict fordeserialisation purpose
        OutForce_dict["__class__"] = "OutForce"
        return OutForce_dict

    def _set_None(self):
        """Set all the properties to None (except pyleecan object)"""

        self.time = None
        self.angle = None
        self.Nt_tot = None
        self.Na_tot = None
        self.P = None
        self.logger_name = None

    def _get_time(self):
        """getter of time"""
        return self._time

    def _set_time(self, value):
        """setter of time"""
        if value is None:
            value = array([])
        elif type(value) is list:
            try:
                value = array(value)
            except:
                pass
        check_var("time", value, "ndarray")
        self._time = value

    time = property(
        fget=_get_time,
        fset=_set_time,
        doc=u"""Structural time vector (no symmetry)

        :Type: ndarray
        """,
    )

    def _get_angle(self):
        """getter of angle"""
        return self._angle

    def _set_angle(self, value):
        """setter of angle"""
        if value is None:
            value = array([])
        elif type(value) is list:
            try:
                value = array(value)
            except:
                pass
        check_var("angle", value, "ndarray")
        self._angle = value

    angle = property(
        fget=_get_angle,
        fset=_set_angle,
        doc=u"""Structural position vector (no symmetry)

        :Type: ndarray
        """,
    )

    def _get_Nt_tot(self):
        """getter of Nt_tot"""
        return self._Nt_tot

    def _set_Nt_tot(self, value):
        """setter of Nt_tot"""
        check_var("Nt_tot", value, "int")
        self._Nt_tot = value

    Nt_tot = property(
        fget=_get_Nt_tot,
        fset=_set_Nt_tot,
        doc=u"""Length of the time vector

        :Type: int
        """,
    )

    def _get_Na_tot(self):
        """getter of Na_tot"""
        return self._Na_tot

    def _set_Na_tot(self, value):
        """setter of Na_tot"""
        check_var("Na_tot", value, "int")
        self._Na_tot = value

    Na_tot = property(
        fget=_get_Na_tot,
        fset=_set_Na_tot,
        doc=u"""Length of the angle vector

        :Type: int
        """,
    )

    def _get_P(self):
        """getter of P"""
        return self._P

    def _set_P(self, value):
        """setter of P"""
        try:  # Check the type
            check_var("P", value, "dict")
        except CheckTypeError:
            check_var("P", value, "SciDataTool.Classes.VectorField.VectorField")
            # property can be set from a list to handle loads
        if (
            type(value) == dict
        ):  # Load type from saved dict {"type":type(value),"str": str(value),"serialized": serialized(value)]
            self._P = loads(value["serialized"].encode("ISO-8859-2"))
        else:
            self._P = value

    P = property(
        fget=_get_P,
        fset=_set_P,
        doc=u"""Air-gap surface force

        :Type: SciDataTool.Classes.VectorField.VectorField
        """,
    )

    def _get_logger_name(self):
        """getter of logger_name"""
        return self._logger_name

    def _set_logger_name(self, value):
        """setter of logger_name"""
        check_var("logger_name", value, "str")
        self._logger_name = value

    logger_name = property(
        fget=_get_logger_name,
        fset=_set_logger_name,
        doc=u"""Name of the logger to use

        :Type: str
        """,
    )
