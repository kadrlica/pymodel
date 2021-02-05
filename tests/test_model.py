#!/usr/bin/env python
"""
Test the model build
"""
from pymodeler import Model
from pymodeler import Param, Property, Derived
from collections import OrderedDict as odict

class Parent(Model):
    _params = odict([('x', Param(value=1               , help='variable x')),
                     ('y', Param(value=2, bounds=[0,10], help='variable y'))])

class Child(Parent):
    _params = Parent._params.copy()
    _params.update(odict([('z', Param(value=None            , help='variable z'))]))
    _mapping = odict([('zed','z')])

class test_class(Model):
    _params = odict([('req', Property(dtype=float,format='%.1f',required=True,help="A required parameter")),
                     ('opt', Property(dtype=float,format='%.1f',default=1.0,help="An optional parameter")),
                     ('var', Param(default=1.0,help="A variable parameter")),
                     ('der', Derived(dtype=float,format='%.1f',help="A derived parameter")),
                     ('der2', Derived(dtype=float,format='%.1f', loader="_loader2", help="A derived parameter"))])

    def _der(self):
        return self.req * self.opt * self.var

    def _loader2(self):
        return self.req * self.opt * self.var



def test_model():

    a = Parent()

    a.x = 3
    a.y = 4

    b = Child()
    for k,v in a.params.items():
        b.setp(k,value=v)
    b.z = 100

    t = test_class(req=2.,var=2.)

    test_val = t.req * t.opt * t.var
    check = t.der
    assert check==test_val

    check = t.der2
    assert check==test_val

    t.req = 4.
    check = t.der
    assert check==8.

    try:
        t2 = test_class(var=2.)
        check = t.der
        assert False
    except ValueError:
        pass


    try: a.f == 2
    except AttributeError: pass
    else: raise TypeError("Failed to catch AttributeError in Model.__getatt__")

    params = a.get_params()
    assert len(params) == 2

    params = a.get_params(['x'])
    assert len(params) == 1

    vals = a.param_values()
    assert len(vals) == 2
    assert vals[0] == 3.

    vals = a.param_values(['x'])
    assert len(vals) == 1
    assert vals[0] == 3.

    errs = a.param_errors()
    assert len(errs) == 2
    assert errs[0] is None

    errs = a.param_errors(['x'])
    assert len(errs) == 1
    assert errs[0] is None

    a_dict = a.todict()
    a_yaml = a.dump()
    a_str = str(a)

    for key in ['name', 'x', 'y']:
        assert key in a_dict
        assert a_yaml.index(key) >= 0
    for key in ['x', 'y']:
        assert a_str.index(key) >= 0

    assert b.zed == b.z
    assert 'zed' in b.mappings

    try: a.setp('x', value='afda')
    except TypeError: pass
    else: raise TypeError("Failed to catch TypeError in Model.setp")



    aa = Child(x=dict(value=2))
    aa.x == 2

    aa = test_class(req=5.3)
    assert aa.req == 5.3

    try: bad = test_class(req=5)
    except TypeError: pass
    else: raise TypeError("Failed to catch TypeError in Model.set_attributes")

    try: bad = Child(vv=dict(value=3))
    except KeyError: pass
    else: raise TypeError("Failed to catch KeyError in Model.set_attributes")
