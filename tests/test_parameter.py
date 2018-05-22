#!/usr/bin/env python
"""
Test the parameters
"""

from pymodeler import Parameter, Param, Property, Derived
from collections import OrderedDict as odict
import yaml

def test_property():
    int_prop = Property(default=10,dtype=int,help="I'm an `int` property")
    int_prop.set_value(3)

    # We shouldn't be able to set to a different type
    try: int_prop.set_value(3.2)
    except TypeError: pass
    else: raise TypeError

    float_prop = Property(value=1.3e6, help="I'm a float parameter")
    float_prop.set(value=0)
    float_prop.clear_value()
    assert float_prop.value is None

    str_prop = Property(value='hello',default='world',help="a `str` property")
    assert str_prop.value == 'hello'
    assert str_prop.innertype() is str

    # A more complex property
    dict_prop = Property(value={'x':3},default={'y':2}, dtype=dict,
                        required=True, help="a dict property")

    assert dict_prop.required == True
    try: dict_prop.set(value=[1,3])
    except TypeError: pass
    else: raise TypeError

    # This should be ok
    Property(value={'x':3},default=['y',2])

    # but this should fail...
    try: Property(value={'x':3},default=['y',2], dtype=dict)
    except TypeError: pass
    else: raise TypeError


def test_derived():
    prop = Property(value='hello',help="Base property")
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
    assert deriv.loader is None

    try: deriv.value
    except TypeError: pass
    else: raise AssertionError()


def test_parameter():
    # Simple parameter
    param = Parameter(value=10)
    assert param.value == 10

    # No dtype set, so this should be ok
    param.set_value(100.)
    assert param.value == 100.

    # But this shouldn't be...
    param = Parameter(value=10,dtype=int)
    try: param.set_value(1.0)
    except TypeError as e: pass
    else: raise AssertionError("Only integer types should be allowed")

    # We only allow numeric types by default
    try: param.set_value('hello')
    except TypeError: pass
    else: raise AssertionError("Only numeric types should be allowed")

    param = Parameter(value=1,bounds=[1,10],errors=[0.5,0.5],dtype=int)

    print(param)
    print(repr(param))

    # Check that yaml works
    print(param.dump())

    # Boolean parameter
    param = Parameter(value=False,dtype=bool)
    if param: raise TypeError
    param.set_value(True)

    ## For right now we can only set with bools
    try: param.set_value(1)
    except TypeError: pass
    else: raise AssertionError("Only boolean types should be allowed")


if __name__ == "__main__":
    test_property()
    test_derived()
    test_parameter()
