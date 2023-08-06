# -*- coding: utf-8 -*-
from os import linesep
from SciDataTool.Classes._check import set_array, check_init_dict, check_var, raise_
from SciDataTool.Functions.save import save
from SciDataTool.Classes.DataND import DataND

# Import all class method
# Try/catch to remove unnecessary dependencies in unused method
try:
    from SciDataTool.Methods.DataFreq.freq_to_time import freq_to_time
except ImportError as error:
    freq_to_time = error
from numpy import array, array_equal
from SciDataTool.Classes._check import InitUnKnowClassError
from SciDataTool.Classes.Data import Data


class DataFreq(DataND):
    """Abstract class for all kinds of data"""

    VERSION = 1
    # Check ImportError to remove unnecessary dependencies in unused method
    # cf Methods.DataFreq.freq_to_time
    if isinstance(freq_to_time, ImportError):
        freq_to_time = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use DataFreq method freq_to_time: " + str(freq_to_time)
                )
            )
        )
    else:
        freq_to_time = freq_to_time
    # save method is available in all object
    save = save

    def __init__(
        self,
        axes=None,
        normalizations={},
        FTparameters={},
        values=None,
        symbol="",
        name="",
        unit="",
        symmetries={},
        init_dict=None,
    ):
        """Constructor of the class. Can be use in two ways :
        - __init__ (arg1 = 1, arg3 = 5) every parameters have name and default values
            for Matrix, None will initialise the property with an empty Matrix
            for SciDataTool type, None will call the default constructor
        - __init__ (init_dict = d) d must be a dictionnary wiht every properties as keys
        ndarray or list can be given for Vector and Matrix
        object or dict can be given for SciDataTool Object"""
        if init_dict is not None:  # Initialisation by dict
            check_init_dict(
                init_dict,
                [
                    "axes",
                    "normalizations",
                    "FTparameters",
                    "values",
                    "symbol",
                    "name",
                    "unit",
                    "symmetries",
                ],
            )
            # Overwrite default value with init_dict content
            if "axes" in list(init_dict.keys()):
                axes = init_dict["axes"]
            if "normalizations" in list(init_dict.keys()):
                normalizations = init_dict["normalizations"]
            if "FTparameters" in list(init_dict.keys()):
                FTparameters = init_dict["FTparameters"]
            if "values" in list(init_dict.keys()):
                values = init_dict["values"]
            if "symbol" in list(init_dict.keys()):
                symbol = init_dict["symbol"]
            if "name" in list(init_dict.keys()):
                name = init_dict["name"]
            if "unit" in list(init_dict.keys()):
                unit = init_dict["unit"]
            if "symmetries" in list(init_dict.keys()):
                symmetries = init_dict["symmetries"]
        # Initialisation by argument
        # Call DataND init
        super(DataFreq, self).__init__(
            axes=axes,
            normalizations=normalizations,
            FTparameters=FTparameters,
            values=values,
            symbol=symbol,
            name=name,
            unit=unit,
            symmetries=symmetries,
        )
        # The class is frozen (in DataND init), for now it's impossible to
        # add new properties

    def __str__(self):
        """Convert this objet in a readeable string (for print)"""
        DataFreq_str = ""
        # Get the properties inherited from DataND
        DataFreq_str += super(DataFreq, self).__str__() + linesep
        return DataFreq_str

    def __eq__(self, other):
        """Compare two objects (skip parent)"""
        if type(other) != type(self):
            return False
        # Check the properties inherited from DataND
        if not super(DataFreq, self).__eq__(other):
            return False
        return True

    def as_dict(self):
        """Convert this objet in a json seriable dict (can be use in __init__)
        """
        # Get the properties inherited from DataND
        DataFreq_dict = super(DataFreq, self).as_dict()
        # The class name is added to the dict fordeserialisation purpose
        # Overwrite the mother class name
        DataFreq_dict["__class__"] = "DataFreq"
        return DataFreq_dict

    def _set_None(self):
        """Set all the properties to None (except SciDataTool object)"""
        # Set to None the properties inherited from DataND
        super(DataFreq, self)._set_None()
