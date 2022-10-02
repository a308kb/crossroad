from xparser import *
from crossroads import *

xml="""<?xml version="1.0" encoding="utf-8" ?>
<crossroad angle="30">
    <segment street="Lomonosov"  angle="0" crosswalk="1" lights="m,w">
        <lane width="3" type="a" direction="i" availa="l,f,b" light="0" stop="0"/>
        <lane width="3" type="a" direction="i" availa="r,f,b" light="0" stop="0"/>
        <lane width="3" type="a" direction="o" availa="l,r,f,b" light="0" stop="0"/>
    </segment>
    <segment street="Pioner"  angle="45" crosswalk="1" lights="m,w">
        <lane width="3" type="a" direction="i" availa="l,r,f,b" light="0" stop="0"/>
        <lane width="3" type="t" direction="i" availa="l,r,f,b" light="0" stop="0"/>
        <lane width="3" type="a" direction="o" availa="l,r,f,b" light="0" stop="0"/>
    </segment>
     <segment street="P2"  angle="225" crosswalk="1" lights="m,w">
        <lane width="3" type="a" direction="i" availa="l,r,f,b" light="0" stop="0"/>
        <lane width="3" type="d" direction="i" availa="l,r,f,b" light="0" stop="0"/>
        <lane width="3" type="a" direction="o" availa="l,r,f,b" light="0" stop="0"/>
    </segment>
   <segment street="Lomonosov2"  angle="180" crosswalk="1">
        <lane width="3" type="a" direction="i" availa="l,r,b" light="0" stop="0"/>
        <lane width="3" type="a" direction="o" availa="l,r,f,b" light="0" stop="0"/>
    </segment>
</crossroad>"""


def test_parse():
    cr=parse(xml)
    assert cr.angle == 30



