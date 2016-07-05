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
    _params = Parent._params 
    _params.update(odict([('z', Param(value=None            , help='variable z'))]))
    _mapping = odict([('zed','z')])

class test_class(Model):
    _params = odict([('req', Property(dtype=float,format='%.1f',required=True,help="A required parameter")),
                     ('opt', Property(dtype=float,format='%.1f',default=1.0,help="An optional parameter")),
                     ('var', Param(default=1.0,help="A variable parameter")),
                     ('der', Derived(dtype=float,format='%.1f',help="A derived parameter"))])            
                
    def _der(self):
        return self.req * self.opt * self.var
 


if __name__ == "__main__":
    import argparse
    description = __doc__
    parser = argparse.ArgumentParser(description=description)
    args = parser.parse_args()

    a = Parent()
    print(a)

    a.x = 3
    a.y = 4
    print(a)

    b = Child()
    print(b)
    for k,v in a.params.items():
        b.setp(k,v)
    b.z = 100
    print(b)

    
    t = test_class(req=2.,var=2.)
    
    check = t.der
    assert(check==4.)

    t.req = 4.
    check = t.der
    assert(check==8.)
    
    try:
        t2 = test_class(var=2.)
        check = t.der
        assert(False)
    except (ValueError):
        pass

