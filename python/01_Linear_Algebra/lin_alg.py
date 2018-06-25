# Course Name : Lnear Algebra a Refresher Course
import math

class Vector(object):
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple(coordinates)
            self.dimention   = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an interable')

    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self,v):
        return self.coordinates == v.coordinates

    def plus(self, v):
        new_coordinates = []
        n = len(self.coordinates)
        for i in range(n):
            new_coordinates.append(self.coordinates[i] + v.coordinates[i])
        return Vector(new_coordinates)

    def minus(self, v):
        new_coordinates = [x-y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def times_scalar(self, c):
        new_coordinates = [c*x for x in self.coordinates]
        return Vector(new_coordinates)

    def magnitude(self):
        coordinates_squared = [x**2 for x in self.coordinates]
        return math.sqrt(sum(coordinates_squared))

    def normalized(self):
        try:
            magnitude = self.magnitude()
            return self.times_scalar(1/magnitude)

        except ZeroDivisionError:
            raise Exception('Cannot normalize the zero vector')

my_vector = Vector([1,2,3])
print(my_vector)
my_vector2 = Vector([1,2,3])
my_vector3 = Vector([-1,2,3])
print('Vector Comparison')
print(my_vector == my_vector2)
print(my_vector == my_vector3)


# Basic operations on vectors

print('')
print('Vector Addition')
v1 = Vector([8.218, -9.341])
v2 = Vector([-1.129, 2.111])
print(v1.plus(v2))

print('')
print('Vector Subtraction')
v1 = Vector([7.119, 8.215])
v2 = Vector([-8.223, 0.878])
print(v1.minus(v2))

print('')
print('Vector Multiplication')
v1 = Vector([1.671, -1.012, -0.318])
c  = 7.41
print(v1.times_scalar(c))

# Magnitude and Direction

print('')
print('Vector Magnitude')
v = Vector([-0.221, 7.437])
print(v.magnitude())
v = Vector([8.813, -1.331, -6.247])
print(v.magnitude())

print('')
print('Vector Normalization')
v = Vector([5.581, -2.136])
print(v.normalized())
v = Vector([1.996, 3.108, -4.554])
print(v.normalized())


