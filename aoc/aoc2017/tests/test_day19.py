from ..solutions import day19

EXAMPLE_INPUT = """     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ 

"""


def test_part1_example():
    assert day19.part1(EXAMPLE_INPUT) == "ABCDEF"


def test_part2_example():
    assert day19.part2(EXAMPLE_INPUT) == 38
