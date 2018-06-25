# Course Name : Lnear Algebra a Refresher Course
import math
from decimal import Decimal, getcontext

getcontext().prec = 30

class Vector(object):
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
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
        new_coordinates = [Decimal(c)*x for x in self.coordinates]
        return Vector(new_coordinates)

    def magnitude(self):
        coordinates_squared = [x**2 for x in self.coordinates]
        return math.sqrt(sum(coordinates_squared))

    def normalized(self):
        try:
            magnitude = self.magnitude()
            return self.times_scalar(1.0/magnitude)

        except ZeroDivisionError:
            raise Exception('Cannot normalize the zero vector')

    def dot_product(self,v):
        coordinates_squared = [x*y for x,y in zip(self.coordinates, v.coordinates)]
        return sum(coordinates_squared)

    def angle_with(self,v, in_degrees=False):
        try:
            u1 = self.normalized()
            u2 = v.normalized()

            angle_in_radians = math.acos(u1.dot_product(u2))

            if in_degrees:
                degrees_per_radian = 180./math.pi
                return angle_in_radians * degrees_per_radian
            else:
                return angle_in_radians

        except ZeroDivisionError as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception('Cannot compute an angle with the zero vector')
            else:
                raise e


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

# Inner products
print('')
print('Vector Dot product')
v = Vector([7.887, 4.138])
w = Vector([-8.802, 6.776])
print(v.dot_product(w))
v = Vector([-5.955, -4.904, -1.874])
w = Vector([-4.496, -8.755, 7.103])
print(v.dot_product(w))

print('')
print('Vector Finding Angle between vectors')
v = Vector([3.183, -7.627])
w = Vector([-2.668, 5.319])
print('Angle in radians : ' + str(v.angle_with(w)))
print('Angle in degrees : ' + str(v.angle_with(w, True)))
v = Vector([7.35, 0.221, 5.188])
w = Vector([2.751, 8.259, 3.985])
print('Angle in radians : ' + str(v.angle_with(w)))
print('Angle in degrees : ' + str(v.angle_with(w, True)))

