from ..solutions import day19

EXAMPLE_INPUT = """     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ 

"""


def test_part1_example():
    assert "ABCDEF" == day19.part1(EXAMPLE_INPUT)


def test_part2_example():
    assert 38 == day19.part2(EXAMPLE_INPUT)
