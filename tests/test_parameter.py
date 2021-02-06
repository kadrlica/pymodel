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
    assert str_prop.value == str_prop()

    # A more complex property
    dict_prop = Property(value={'x':3},default={'y':2}, dtype=dict,
                        required=True, help="a dict property")

    dict_check = dict_prop.todict()
    assert dict_check['value']['x'] == 3

    print(dict_prop)
    print(repr(dict_prop))

    # Check that yaml works
    print(dict_prop.dump())

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

    deriv = Derived(dtype=int, loader=loader)
    try: deriv.value
    except TypeError: pass
    else: raise AssertionError()


def test_parameter():
    # Simple parameter
    param = Parameter(value=10)
    assert param.value == 10

    print(param)
    print(repr(param))

    # No dtype set, so this should be ok
    param.set_value(100.)
    assert param.value == 100.
    assert param.symmetric_error == 0.

    # But this shouldn't be...
    param = Parameter(value=10,dtype=int)
    try: param.set_value(1.0)
    except TypeError as e: pass
    else: raise AssertionError("Only integer types should be allowed")

    # This shouldn't be either
    try: param_bad = Parameter(value=(10, 3), dtype=tuple)
    except TypeError as e: pass
    else: raise AssertionError("Only scalar types should be allowed")

    # This shouldn't be either
    try: param_bad = Parameter(value=10, bad="aa")
    except AttributeError as e: pass
    else: raise AssertionError("Did not catch bad attribute to Parameter c'tor")

    # We only allow numeric types by default
    try: param.set_value('hello')
    except TypeError: pass
    else: raise AssertionError("Only numeric types should be allowed")

    param = Parameter(value=1,bounds=[1,10],errors=0.5,dtype=int)
    assert param.symmetric_error == 0.5

    param = Parameter(value=1,bounds=[1,10],errors=[0.5,0.5],dtype=int)
    assert param.symmetric_error == 0.5
    try: param.set_value(11)
    except ValueError: pass
    else: raise ValueError("Failed to catch bounds error")
    param.set_free(True)
    assert param.free
    param.set_free(None)
    assert not param.free

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


def test_parameter_operators():
    # Simple parameter
    param = Parameter(value=10)

    assert param == 10
    assert param.value == 10
    assert param != 9
    assert param > 9
    assert param < 11
    assert param >= 10
    assert param <= 11

    assert 1 + param == 11
    assert param + 1 == 11
    assert 11 - param == 1
    assert param - 1 == 9

    assert param * 2 == 20
    assert 2 * param == 20

    assert param / 2 == 5
    assert 20 / param == 2

    assert param // 3 == 3
    assert 25 // param == 2

    assert param % 2 == 0
    assert 15 % param == 5

    assert param ** 2 == 100
    assert 2 ** param == 1024

    assert divmod(param, 4) == (2, 2)
    assert divmod(15, param) == (1, 5)

    assert param & 15 == 10
    assert 15 & param == 10

    assert param | 5 == 15
    assert 5 | param == 15

    assert param ^ 15 == 5
    assert 15 ^ param == 5

    assert param << 1 == 20
    assert 1 << param == 1024

    assert param >> 1 == 5
    assert 1024 >> param == 1

    assert ~param == ~10

    assert param.__index__() == 10
    assert param.__nonzero__()

    assert int(param) == 10
    assert float(param) == 10.
    assert bool(param) == True

    param = Parameter(value=-10)
    assert abs(param) == 10
    assert param.__pos__() == -10
    assert param.__neg__() == 10

    param = Parameter(value=10.3)
    try: param.__index__()
    except AttributeError: pass
    else: raise AttributeError("float shouldn't have __index__ method")

    assert param.__trunc__() == 10





def test_docs():

    prop_docs = Property.defaults_docstring()
    assert prop_docs.index('dtype') >= 0

    der_docs = Derived.defaults_docstring()
    assert der_docs.index('loader') >= 0

    par_docs = Parameter.defaults_docstring()
    assert par_docs.index('errors') >= 0





if __name__ == "__main__":
    test_property()
    test_derived()
    test_parameter()
    test_parameter_operators()
