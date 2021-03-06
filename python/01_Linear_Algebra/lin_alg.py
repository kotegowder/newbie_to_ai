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

            if u1.dot_product(u2) <= -1:
                angle_in_radians = math.acos(-1.0)
            else:
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

    def is_zero(self, tolerance=1e-10):
        return self.magnitude() < tolerance

    def is_parallel_to(self,v):
        if self.is_zero() or v.is_zero() or self.angle_with(v) == 0 or self.angle_with(v) == math.pi:
            return True
        else:
            return False

    def is_orthogonal_to(self,v, tolerance=1e-10):
        return abs(self.dot_product(v)) < tolerance

    def component_parallel_to(self,basis):
        try:
            u = basis.normalized()
            weight = self.dot_product(u)
            return u.times_scalar(weight)
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e

    def component_orthogonal_to(self,basis):
        try:
            projection = self.component_parallel_to(basis)
            return self.minus(projection)

        except Exception as e:
            if str(e) == self.NO_UNIQUE_PARALLEL_COMPONENT_MSG:
                raise Exception(self.NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG)
            else:
                raise e

    def cross_product(self, v):
        new_coordinates = []
        arg1 = self.coordinates[1]*v.coordinates[2] - v.coordinates[1]*self.coordinates[2]
        new_coordinates.append(arg1)
        arg2 = -1*(self.coordinates[0]*v.coordinates[2] - v.coordinates[0]*self.coordinates[2])
        new_coordinates.append(arg2)
        arg3 = self.coordinates[0]*v.coordinates[1] - v.coordinates[0]*self.coordinates[1]
        new_coordinates.append(arg3)
        return Vector(new_coordinates)

    def area_of_parallelogram(self, v):
        cross_product = self.cross_product(v)
        return cross_product.magnitude()

    def are_of_triangle_with(self, v):
        return self.area_of_parallelogram(v) / 2.0


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

# Parallelism and Orthogonality
print('')
print('Vector Parallelism and Orthogonality')
v = Vector([-7.579, -7.88])
w = Vector([22.737, 23.64])
print('First Pair')
print('is parallel to: ' + str(v.is_parallel_to(w)))
print('is orthogonal to: '+ str(v.is_orthogonal_to(w)))
v = Vector([-2.029, 9.97, 4.172])
w = Vector([-9.231, -6.639, -7.245])
print('Second pair')
print('is parallel to: '+ str(v.is_parallel_to(w)))
print('is orthogonal to: ' + str(v.is_orthogonal_to(w)))
v = Vector([-2.328, -7.284, -1.214])
w = Vector([-1.821, 1.072, -2.94])
print('Third pair')
print('is parallel to: ' + str(v.is_parallel_to(w)))
print('is orthogonal to: ' + str(v.is_orthogonal_to(w)))
v = Vector([2.118, 4.827])
w = Vector([0,0])
print('Fourth pair')
print('is parallel to: ' + str(v.is_parallel_to(w)))
print('is orthogonal to: '+ str(v.is_orthogonal_to(w)))

# Projecting Vectors
print('')
print('Projection of Vectors')
v = Vector([3.039, 1.879])
w = Vector([0.825, 2.036])
print(v.component_parallel_to(w))
v = Vector([-9.88, -3.264, -8.159])
w = Vector([-2.155, -9.353, -9.473])
print(v.component_orthogonal_to(w))
v = Vector([3.009, -6.172, 3.692, -2.51])
w = Vector([6.404, -9.144, 2.759, 8.718])
vpar = v.component_parallel_to(w)
vort = v.component_orthogonal_to(w)
print('Parallel component: ' + str(vpar))
print('Orthogonal component: ' + str(vort))

# Cross Products
print('')
print('Cross Products')
v = Vector([8.462, 7.893, -8.187])
w = Vector([6.984, -5.975, 4.778])
print(v.cross_product(w))
v = Vector([-8.987, -9.838, 5.031])
w = Vector([-4.268, -1.861, -8.866])
print(v.area_of_parallelogram(w))
v = Vector([1.5, 9.547, 3.691])
w = Vector([-6.007, 0.124, 5.772])
print(v.are_of_triangle_with(w))