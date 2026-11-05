import math


class Circle:

    system = "Metric"

    @classmethod
    def create_from_area(cls, area):
        if cls.system == "Metric":
            radius_cm = math.sqrt(area / math.pi)
        else:
            radius_in = math.sqrt(area/math.pi)
            radius_cm = radius_in * 2.54
        new_circle = Circle(radius_cm)
        return new_circle

    def __init__(self, radius_cm):
        self.radius_cm = radius_cm

    def area(self):
        if self.system == "Metric":
            answer = math.pi * self.radius_cm**2
        else:
            radius_to_use = self.radius_cm / 2.54
            answer = math.pi * radius_to_use ** 2
        return answer


def main():
    x = Circle(2)
    print(x.area())

    y = Circle(4)
    print(y.area())

    Circle.system = "Imperial"

    print(x.area())
    print(y.area())

    x.system = "Metric"
    print(x.area())
    print(y.area())

    Circle.system = "Imperial"
    print(x.area())
    print(y.area())

    area = 50
    z = Circle.create_from_area(50)
    print(z.radius_cm)
    print(z.area())


if __name__ == "__main__":
    main()
