from cubefactory import cube_factory

cube1 = cube_factory("string")
cube2 = cube_factory("group")

cube1("R U R' U'")
print(cube1)
cube2("R U R' U'")
print(cube2)

cube3 = cube_factory("string", new_solved_state = list(' '*9+'b'*9+"r"*9+"g"*9+'o'*9+' '*9)) # pylint: disable=unexpected-keyword-arg
cube3("F2 M2 F2 M2")
print(cube3)
print(cube3.is_solved())

cube4 = cube_factory("string")
print(cube4)