#!/usr/bin/env python
"""
A Model object is just a container for a set of Parameter.
Implements __getattr__ and __setattr__.

The model has a set of default parameters stored in Model._params. 
Careful, if these are changex, they will be changed for all 
subsequent instances of the Model.

The parameters for a given instance of a model are stored in the
Model.params attribute. This attribute is a deepcopy of 
Model._params created during instantiation.

"""
from collections import OrderedDict as odict
import numpy as np
import copy
import yaml

from pymodeler.parameter import *

def indent(string,width=0): 
    return '{0:>{1}}{2}'.format('',width,string)

class Model(object):
    # `_params` is a tuple of Property objects
    # _params = (('parameter name',Property(...)),...)
    _params = odict([])
    # `_mapping` is an alternative name mapping
    # for the parameters in _params
    _mapping = odict([])

    def __init__(self,*args,**kwargs):
        self.params = self.defaults
        self._init_properties()
        self.set_attributes(**kwargs)
        # In case no properties were set, cache anyway
        self._cache()

    def __getattr__(self,name):
        # Return 'getp' of parameter
        if name in self._params or name in self._mapping:
            return self.getp(name).value
        else:
            # Raises AttributeError
            return object.__getattribute__(self,name)

    def __setattr__(self, name, value):
        # Call 'setp' on parameters
        if name in self._params or name in self._mapping:
            self.setp(name, value=value)
        else:
            # Why is this a return statement
            return object.__setattr__(self, name, value)

    def __str__(self,indent=0):
        ret = '{0:>{2}}{1}'.format('',self.name,indent)
        if len(self.params)==0:
            pass
        else:            
            ret += '\n{0:>{2}}{1}'.format('','Parameters:',indent+2)
            width = len(max(self.params.keys(),key=len))
            for name,value in self.params.items():
                par = '{0!s:{width}} : {1!r}'.format(name,value,width=width)
                ret += '\n{0:>{2}}{1}'.format('',par,indent+4)
        return ret

    @property
    def defaults(self):
        """Ordered dictionary of default parameters."""
        # Deep copy is necessary so that default parameters remain unchanged
        return copy.deepcopy(self._params)

    @property
    def mappings(self):
        """Ordered dictionary of mapping."""
        return copy.deepcopy(self._mapping)

    #@property
    #def name(self):
    #    return self.__class__.__name__

    def getp(self, name):
        """ 
        Get the named parameter.

        Parameters
        ----------
        name : string
            The parameter name.

        Returns
        -------
        param : 
            The parameter object.
        """
        name = self._mapping.get(name,name)
        return self.params[name]

    def setp(self, name, clear_derived=True, value=None, bounds=None, free=None, errors=None):
        """ 
        Set the value (and bounds) of the named parameter.

        Parameters
        ----------
        name : string
            The parameter name.
        value: 
            The value of the parameter
        bounds: None
            The bounds on the parameter
        Returns
        -------
        None
        """
        name = self._mapping.get(name,name)
        self.params[name].set(value=value,bounds=bounds,free=free,errors=errors)
        if clear_derived:
            self.clear_derived()
        self._cache(name)

    def set_attributes(self, **kwargs):
        """
        Set a group of attributes (parameters and members).  Calls
        `setp` directly, so kwargs can include more than just the
        parameter value (e.g., bounds, free, etc.).
        """
        self.clear_derived()
        kwargs = dict(kwargs)
        for name,value in kwargs.items():
            # Raise AttributeError if param not found
            try:
                self.__getattr__(name) 
            except (AttributeError):
                print "Warning: %s does not have attribute %s"%(type(self),name)                
            # Set attributes
            try: self.setp(name,clear_derived=False,**value)
            except TypeError:
                try:  self.setp(name,clear_derived=False,*value)
                except (TypeError,KeyError):  
                    self.__setattr__(name,value)
            # pop this attribued off the list of missing properties
            self._missing.pop(name,None)
        # Check to make sure we got all the required properties
        if len(self._missing) != 0:
            raise ValueError("One or more required properties are missing ",self._missing.keys())


    def _init_properties(self):
        """ Loop through the list of Properties, 
        extract the derived and required properties and do the
        appropriate book-keeping
        """
        self._missing = {}
        for k,p in self.params.items():
            if p.required:
                self._missing[k] = p
            if isinstance(p,Derived):
               if p.loader is None:
                   # Default to using _<param_name>
                   p.loader = self.__getattribute__("_%s"%k)
               elif isinstance(p.loader,str):
                   p.loader = self.__getattribute__(p.loader)
            

    def clear_derived(self):
        """ Reset the value of all Derived properties to None

        This is called by setp (and by extension __setattr__
        """
        for k,p in self.params.items():
           if isinstance(p,Derived):  
               p.clear_value()
        

    def todict(self):
        """ Return self cast as an '~collections.OrderedDict' object 
        """
        ret = odict(name = self.__class__.__name__)
        ret.update(self.params)
        return ret

    def dump(self):
        """ Dump this object as a yaml string
        """
        return yaml.dump(self.todict())

    def _cache(self, name=None):
        """ 
        Method called in _setp to cache any computationally
        intensive properties after updating the parameters.

        Parameters
        ----------
        name : string
           The parameter name.

        Returns
        -------
        None
        """
        pass




        
if __name__ == "__main__":
    import argparse
    description = "python script"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('args',nargs=argparse.REMAINDER)
    opts = parser.parse_args(); args = opts.args
