#!/usr/bin/env python
"""
Test the parameters
"""

from pymodeler import Parameter, Param, Property, Derived
from collections import OrderedDict as odict

def test_property():
    int_prop = Property(default=10,dtype=int,
                        help="I'm an int property")
    int_prop.set_value(3)

    # Shouldn't be able to set to a different type
    try: int_prop.set_value(3.2)
    except TypeError as e: pass
    else: raise Exception()
        
    float_prop = Property(value=1.3e6,
                          help="I'm a float parameter")
    float_prop.set(value=0)
    float_prop.clear_value()
    assert float_prop.value is None

    str_prop = Property(value='hello',default='world',
                        help="I'm a str property")

    assert str_prop.value == 'hello'
    assert str_prop.innertype() is str

def test_derived():
    prop = Property(value='hello',help="Base propert")
    loader = lambda: 'world'

    # This property has nothing set
    deriv = Derived(loader=loader)
    assert deriv.value == loader()

    # These properties are initialized
    deriv = Derived(value='value',loader=loader)
    assert deriv.value != loader()

    deriv = Derived(default='default',loader=loader)
    assert deriv.value != loader()

    # Allow a derived property without a loader?
    deriv = Derived()
    assert deriv.value is None

def test_parameter():
    # Simple parameter
    param = Parameter(value=10)
    assert param.value == 10

    # No dtype set, so this should be ok
    param.set_value(100.)
    assert param.value == 100.

    # We currently allow any type
    param.set_value(1.0)

    # We currently allow any type (this should probably fail)
    param.set_value('hello')

    param = Parameter(value=1,bounds=[1,10],errors=[0.5,0.5],dtype=int)

    print(param)
    print(repr(param))

    # We currently allow any type (this should probably fail)
    #param.set_value('hello')


if __name__ == "__main__":
    test_property()
    test_derived()
    test_parameter()
