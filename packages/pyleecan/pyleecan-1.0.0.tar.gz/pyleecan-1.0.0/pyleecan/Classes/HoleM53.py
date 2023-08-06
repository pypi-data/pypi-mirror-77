# -*- coding: utf-8 -*-
# File generated according to Generator/ClassesRef/Slot/HoleM53.csv
# WARNING! All changes made in this file will be lost!
"""Method code available at https://github.com/Eomys/pyleecan/tree/master/pyleecan/Methods/Slot/HoleM53
"""

from os import linesep
from logging import getLogger
from ._check import check_var, raise_
from ..Functions.get_logger import get_logger
from ..Functions.save import save
from .HoleMag import HoleMag

# Import all class method
# Try/catch to remove unnecessary dependencies in unused method
try:
    from ..Methods.Slot.HoleM53.build_geometry import build_geometry
except ImportError as error:
    build_geometry = error

try:
    from ..Methods.Slot.HoleM53.check import check
except ImportError as error:
    check = error

try:
    from ..Methods.Slot.HoleM53.comp_alpha import comp_alpha
except ImportError as error:
    comp_alpha = error

try:
    from ..Methods.Slot.HoleM53.comp_mass_magnets import comp_mass_magnets
except ImportError as error:
    comp_mass_magnets = error

try:
    from ..Methods.Slot.HoleM53.comp_radius import comp_radius
except ImportError as error:
    comp_radius = error

try:
    from ..Methods.Slot.HoleM53.comp_surface_magnets import comp_surface_magnets
except ImportError as error:
    comp_surface_magnets = error

try:
    from ..Methods.Slot.HoleM53.comp_volume_magnets import comp_volume_magnets
except ImportError as error:
    comp_volume_magnets = error

try:
    from ..Methods.Slot.HoleM53.comp_W5 import comp_W5
except ImportError as error:
    comp_W5 = error

try:
    from ..Methods.Slot.HoleM53.get_height_magnet import get_height_magnet
except ImportError as error:
    get_height_magnet = error

try:
    from ..Methods.Slot.HoleM53.remove_magnet import remove_magnet
except ImportError as error:
    remove_magnet = error

try:
    from ..Methods.Slot.HoleM53.has_magnet import has_magnet
except ImportError as error:
    has_magnet = error


from ._check import InitUnKnowClassError
from .Magnet import Magnet
from .Material import Material


class HoleM53(HoleMag):
    """V shape slot for buried magnet"""

    VERSION = 1
    IS_SYMMETRICAL = 1

    # Check ImportError to remove unnecessary dependencies in unused method
    # cf Methods.Slot.HoleM53.build_geometry
    if isinstance(build_geometry, ImportError):
        build_geometry = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use HoleM53 method build_geometry: " + str(build_geometry)
                )
            )
        )
    else:
        build_geometry = build_geometry
    # cf Methods.Slot.HoleM53.check
    if isinstance(check, ImportError):
        check = property(
            fget=lambda x: raise_(
                ImportError("Can't use HoleM53 method check: " + str(check))
            )
        )
    else:
        check = check
    # cf Methods.Slot.HoleM53.comp_alpha
    if isinstance(comp_alpha, ImportError):
        comp_alpha = property(
            fget=lambda x: raise_(
                ImportError("Can't use HoleM53 method comp_alpha: " + str(comp_alpha))
            )
        )
    else:
        comp_alpha = comp_alpha
    # cf Methods.Slot.HoleM53.comp_mass_magnets
    if isinstance(comp_mass_magnets, ImportError):
        comp_mass_magnets = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use HoleM53 method comp_mass_magnets: "
                    + str(comp_mass_magnets)
                )
            )
        )
    else:
        comp_mass_magnets = comp_mass_magnets
    # cf Methods.Slot.HoleM53.comp_radius
    if isinstance(comp_radius, ImportError):
        comp_radius = property(
            fget=lambda x: raise_(
                ImportError("Can't use HoleM53 method comp_radius: " + str(comp_radius))
            )
        )
    else:
        comp_radius = comp_radius
    # cf Methods.Slot.HoleM53.comp_surface_magnets
    if isinstance(comp_surface_magnets, ImportError):
        comp_surface_magnets = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use HoleM53 method comp_surface_magnets: "
                    + str(comp_surface_magnets)
                )
            )
        )
    else:
        comp_surface_magnets = comp_surface_magnets
    # cf Methods.Slot.HoleM53.comp_volume_magnets
    if isinstance(comp_volume_magnets, ImportError):
        comp_volume_magnets = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use HoleM53 method comp_volume_magnets: "
                    + str(comp_volume_magnets)
                )
            )
        )
    else:
        comp_volume_magnets = comp_volume_magnets
    # cf Methods.Slot.HoleM53.comp_W5
    if isinstance(comp_W5, ImportError):
        comp_W5 = property(
            fget=lambda x: raise_(
                ImportError("Can't use HoleM53 method comp_W5: " + str(comp_W5))
            )
        )
    else:
        comp_W5 = comp_W5
    # cf Methods.Slot.HoleM53.get_height_magnet
    if isinstance(get_height_magnet, ImportError):
        get_height_magnet = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use HoleM53 method get_height_magnet: "
                    + str(get_height_magnet)
                )
            )
        )
    else:
        get_height_magnet = get_height_magnet
    # cf Methods.Slot.HoleM53.remove_magnet
    if isinstance(remove_magnet, ImportError):
        remove_magnet = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use HoleM53 method remove_magnet: " + str(remove_magnet)
                )
            )
        )
    else:
        remove_magnet = remove_magnet
    # cf Methods.Slot.HoleM53.has_magnet
    if isinstance(has_magnet, ImportError):
        has_magnet = property(
            fget=lambda x: raise_(
                ImportError("Can't use HoleM53 method has_magnet: " + str(has_magnet))
            )
        )
    else:
        has_magnet = has_magnet
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
        H0=0.003,
        H1=0,
        W1=0.013,
        H2=0.02,
        W2=0.01,
        H3=0.01,
        W3=0.01,
        W4=0.01,
        magnet_0=-1,
        magnet_1=-1,
        Zh=36,
        mat_void=-1,
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

        if magnet_0 == -1:
            magnet_0 = Magnet()
        if magnet_1 == -1:
            magnet_1 = Magnet()
        if mat_void == -1:
            mat_void = Material()
        if init_str is not None:  # Initialisation by str
            from ..Functions.load import load

            assert type(init_str) is str
            # load the object from a file
            obj = load(init_str)
            assert type(obj) is type(self)
            H0 = obj.H0
            H1 = obj.H1
            W1 = obj.W1
            H2 = obj.H2
            W2 = obj.W2
            H3 = obj.H3
            W3 = obj.W3
            W4 = obj.W4
            magnet_0 = obj.magnet_0
            magnet_1 = obj.magnet_1
            Zh = obj.Zh
            mat_void = obj.mat_void
        if init_dict is not None:  # Initialisation by dict
            assert type(init_dict) is dict
            # Overwrite default value with init_dict content
            if "H0" in list(init_dict.keys()):
                H0 = init_dict["H0"]
            if "H1" in list(init_dict.keys()):
                H1 = init_dict["H1"]
            if "W1" in list(init_dict.keys()):
                W1 = init_dict["W1"]
            if "H2" in list(init_dict.keys()):
                H2 = init_dict["H2"]
            if "W2" in list(init_dict.keys()):
                W2 = init_dict["W2"]
            if "H3" in list(init_dict.keys()):
                H3 = init_dict["H3"]
            if "W3" in list(init_dict.keys()):
                W3 = init_dict["W3"]
            if "W4" in list(init_dict.keys()):
                W4 = init_dict["W4"]
            if "magnet_0" in list(init_dict.keys()):
                magnet_0 = init_dict["magnet_0"]
            if "magnet_1" in list(init_dict.keys()):
                magnet_1 = init_dict["magnet_1"]
            if "Zh" in list(init_dict.keys()):
                Zh = init_dict["Zh"]
            if "mat_void" in list(init_dict.keys()):
                mat_void = init_dict["mat_void"]
        # Initialisation by argument
        self.H0 = H0
        self.H1 = H1
        self.W1 = W1
        self.H2 = H2
        self.W2 = W2
        self.H3 = H3
        self.W3 = W3
        self.W4 = W4
        # magnet_0 can be None, a Magnet object or a dict
        if isinstance(magnet_0, dict):
            # Check that the type is correct (including daughter)
            class_name = magnet_0.get("__class__")
            if class_name not in [
                "Magnet",
                "MagnetFlat",
                "MagnetPolar",
                "MagnetType10",
                "MagnetType11",
                "MagnetType12",
                "MagnetType13",
                "MagnetType14",
            ]:
                raise InitUnKnowClassError(
                    "Unknow class name " + class_name + " in init_dict for magnet_0"
                )
            # Dynamic import to call the correct constructor
            module = __import__("pyleecan.Classes." + class_name, fromlist=[class_name])
            class_obj = getattr(module, class_name)
            self.magnet_0 = class_obj(init_dict=magnet_0)
        elif isinstance(magnet_0, str):
            from ..Functions.load import load

            magnet_0 = load(magnet_0)
            # Check that the type is correct (including daughter)
            class_name = magnet_0.__class__.__name__
            if class_name not in [
                "Magnet",
                "MagnetFlat",
                "MagnetPolar",
                "MagnetType10",
                "MagnetType11",
                "MagnetType12",
                "MagnetType13",
                "MagnetType14",
            ]:
                raise InitUnKnowClassError(
                    "Unknow class name " + class_name + " in init_dict for magnet_0"
                )
            self.magnet_0 = magnet_0
        else:
            self.magnet_0 = magnet_0
        # magnet_1 can be None, a Magnet object or a dict
        if isinstance(magnet_1, dict):
            # Check that the type is correct (including daughter)
            class_name = magnet_1.get("__class__")
            if class_name not in [
                "Magnet",
                "MagnetFlat",
                "MagnetPolar",
                "MagnetType10",
                "MagnetType11",
                "MagnetType12",
                "MagnetType13",
                "MagnetType14",
            ]:
                raise InitUnKnowClassError(
                    "Unknow class name " + class_name + " in init_dict for magnet_1"
                )
            # Dynamic import to call the correct constructor
            module = __import__("pyleecan.Classes." + class_name, fromlist=[class_name])
            class_obj = getattr(module, class_name)
            self.magnet_1 = class_obj(init_dict=magnet_1)
        elif isinstance(magnet_1, str):
            from ..Functions.load import load

            magnet_1 = load(magnet_1)
            # Check that the type is correct (including daughter)
            class_name = magnet_1.__class__.__name__
            if class_name not in [
                "Magnet",
                "MagnetFlat",
                "MagnetPolar",
                "MagnetType10",
                "MagnetType11",
                "MagnetType12",
                "MagnetType13",
                "MagnetType14",
            ]:
                raise InitUnKnowClassError(
                    "Unknow class name " + class_name + " in init_dict for magnet_1"
                )
            self.magnet_1 = magnet_1
        else:
            self.magnet_1 = magnet_1
        # Call HoleMag init
        super(HoleM53, self).__init__(Zh=Zh, mat_void=mat_void)
        # The class is frozen (in HoleMag init), for now it's impossible to
        # add new properties

    def __str__(self):
        """Convert this objet in a readeable string (for print)"""

        HoleM53_str = ""
        # Get the properties inherited from HoleMag
        HoleM53_str += super(HoleM53, self).__str__()
        HoleM53_str += "H0 = " + str(self.H0) + linesep
        HoleM53_str += "H1 = " + str(self.H1) + linesep
        HoleM53_str += "W1 = " + str(self.W1) + linesep
        HoleM53_str += "H2 = " + str(self.H2) + linesep
        HoleM53_str += "W2 = " + str(self.W2) + linesep
        HoleM53_str += "H3 = " + str(self.H3) + linesep
        HoleM53_str += "W3 = " + str(self.W3) + linesep
        HoleM53_str += "W4 = " + str(self.W4) + linesep
        if self.magnet_0 is not None:
            tmp = self.magnet_0.__str__().replace(linesep, linesep + "\t").rstrip("\t")
            HoleM53_str += "magnet_0 = " + tmp
        else:
            HoleM53_str += "magnet_0 = None" + linesep + linesep
        if self.magnet_1 is not None:
            tmp = self.magnet_1.__str__().replace(linesep, linesep + "\t").rstrip("\t")
            HoleM53_str += "magnet_1 = " + tmp
        else:
            HoleM53_str += "magnet_1 = None" + linesep + linesep
        return HoleM53_str

    def __eq__(self, other):
        """Compare two objects (skip parent)"""

        if type(other) != type(self):
            return False

        # Check the properties inherited from HoleMag
        if not super(HoleM53, self).__eq__(other):
            return False
        if other.H0 != self.H0:
            return False
        if other.H1 != self.H1:
            return False
        if other.W1 != self.W1:
            return False
        if other.H2 != self.H2:
            return False
        if other.W2 != self.W2:
            return False
        if other.H3 != self.H3:
            return False
        if other.W3 != self.W3:
            return False
        if other.W4 != self.W4:
            return False
        if other.magnet_0 != self.magnet_0:
            return False
        if other.magnet_1 != self.magnet_1:
            return False
        return True

    def as_dict(self):
        """Convert this objet in a json seriable dict (can be use in __init__)
        """

        # Get the properties inherited from HoleMag
        HoleM53_dict = super(HoleM53, self).as_dict()
        HoleM53_dict["H0"] = self.H0
        HoleM53_dict["H1"] = self.H1
        HoleM53_dict["W1"] = self.W1
        HoleM53_dict["H2"] = self.H2
        HoleM53_dict["W2"] = self.W2
        HoleM53_dict["H3"] = self.H3
        HoleM53_dict["W3"] = self.W3
        HoleM53_dict["W4"] = self.W4
        if self.magnet_0 is None:
            HoleM53_dict["magnet_0"] = None
        else:
            HoleM53_dict["magnet_0"] = self.magnet_0.as_dict()
        if self.magnet_1 is None:
            HoleM53_dict["magnet_1"] = None
        else:
            HoleM53_dict["magnet_1"] = self.magnet_1.as_dict()
        # The class name is added to the dict fordeserialisation purpose
        # Overwrite the mother class name
        HoleM53_dict["__class__"] = "HoleM53"
        return HoleM53_dict

    def _set_None(self):
        """Set all the properties to None (except pyleecan object)"""

        self.H0 = None
        self.H1 = None
        self.W1 = None
        self.H2 = None
        self.W2 = None
        self.H3 = None
        self.W3 = None
        self.W4 = None
        if self.magnet_0 is not None:
            self.magnet_0._set_None()
        if self.magnet_1 is not None:
            self.magnet_1._set_None()
        # Set to None the properties inherited from HoleMag
        super(HoleM53, self)._set_None()

    def _get_H0(self):
        """getter of H0"""
        return self._H0

    def _set_H0(self, value):
        """setter of H0"""
        check_var("H0", value, "float", Vmin=0)
        self._H0 = value

    H0 = property(
        fget=_get_H0,
        fset=_set_H0,
        doc=u"""Slot depth

        :Type: float
        :min: 0
        """,
    )

    def _get_H1(self):
        """getter of H1"""
        return self._H1

    def _set_H1(self, value):
        """setter of H1"""
        check_var("H1", value, "float", Vmin=0)
        self._H1 = value

    H1 = property(
        fget=_get_H1,
        fset=_set_H1,
        doc=u"""Distance from the lamination Bore

        :Type: float
        :min: 0
        """,
    )

    def _get_W1(self):
        """getter of W1"""
        return self._W1

    def _set_W1(self, value):
        """setter of W1"""
        check_var("W1", value, "float", Vmin=0)
        self._W1 = value

    W1 = property(
        fget=_get_W1,
        fset=_set_W1,
        doc=u"""Tooth width (at V bottom)

        :Type: float
        :min: 0
        """,
    )

    def _get_H2(self):
        """getter of H2"""
        return self._H2

    def _set_H2(self, value):
        """setter of H2"""
        check_var("H2", value, "float", Vmin=0)
        self._H2 = value

    H2 = property(
        fget=_get_H2,
        fset=_set_H2,
        doc=u"""Magnet Height

        :Type: float
        :min: 0
        """,
    )

    def _get_W2(self):
        """getter of W2"""
        return self._W2

    def _set_W2(self, value):
        """setter of W2"""
        check_var("W2", value, "float", Vmin=0)
        self._W2 = value

    W2 = property(
        fget=_get_W2,
        fset=_set_W2,
        doc=u"""Distance Magnet to bottom of the V

        :Type: float
        :min: 0
        """,
    )

    def _get_H3(self):
        """getter of H3"""
        return self._H3

    def _set_H3(self, value):
        """setter of H3"""
        check_var("H3", value, "float", Vmin=0)
        self._H3 = value

    H3 = property(
        fget=_get_H3,
        fset=_set_H3,
        doc=u"""Additional depth for the magnet

        :Type: float
        :min: 0
        """,
    )

    def _get_W3(self):
        """getter of W3"""
        return self._W3

    def _set_W3(self, value):
        """setter of W3"""
        check_var("W3", value, "float", Vmin=0)
        self._W3 = value

    W3 = property(
        fget=_get_W3,
        fset=_set_W3,
        doc=u"""Magnet Width

        :Type: float
        :min: 0
        """,
    )

    def _get_W4(self):
        """getter of W4"""
        return self._W4

    def _set_W4(self, value):
        """setter of W4"""
        check_var("W4", value, "float", Vmin=0)
        self._W4 = value

    W4 = property(
        fget=_get_W4,
        fset=_set_W4,
        doc=u"""Slot angle

        :Type: float
        :min: 0
        """,
    )

    def _get_magnet_0(self):
        """getter of magnet_0"""
        return self._magnet_0

    def _set_magnet_0(self, value):
        """setter of magnet_0"""
        check_var("magnet_0", value, "Magnet")
        self._magnet_0 = value

        if self._magnet_0 is not None:
            self._magnet_0.parent = self

    magnet_0 = property(
        fget=_get_magnet_0,
        fset=_set_magnet_0,
        doc=u"""First Magnet

        :Type: Magnet
        """,
    )

    def _get_magnet_1(self):
        """getter of magnet_1"""
        return self._magnet_1

    def _set_magnet_1(self, value):
        """setter of magnet_1"""
        check_var("magnet_1", value, "Magnet")
        self._magnet_1 = value

        if self._magnet_1 is not None:
            self._magnet_1.parent = self

    magnet_1 = property(
        fget=_get_magnet_1,
        fset=_set_magnet_1,
        doc=u"""Second Magnet

        :Type: Magnet
        """,
    )
