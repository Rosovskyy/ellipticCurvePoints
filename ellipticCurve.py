class Helper:
    @staticmethod
    def modularSqrt(s, mod):
        if Helper.multiplicative(s, mod) != 1 or s == 0:
            return 0
        part, number = mod - 1, 0
        while part % 2 == 0:
            part /= 2
            number += 1
        nWithLegend = 2
        while Helper.multiplicative(nWithLegend, mod) != -1:
            nWithLegend += 1
        guess = pow(s, (int(s) + 1) // 2, mod)
        fudgeFac = pow(s, int(s), mod)
        power = pow(nWithLegend, int(s), mod)
        exponent = number
        while True:
            t, m = fudgeFac, 0
            for m in range(exponent):
                if t == 1:
                    break
                t = pow(t, 2, mod)
            if m == 0:
                return guess
            gs = pow(power, 2 ** (exponent - m - 1), mod)
            g = (gs * gs) % mod
            guess = (guess * gs) % mod
            fudgeFac = (power * g) % mod
            exponent = m

    @staticmethod
    def multiplicative(a, p):  # legend symbol
        ls = pow(a, (p - 1) // 2, p)
        return ls if ls != p - 1 else -1

    @staticmethod
    def modOfValue(a, m):  # mod of inverse value
        g, x, y = Helper.egcd(a % m, m)
        if g != 1:
            print("x is not on the curve.")
            return
        else:
            return x % m

    @staticmethod
    def egcd(a, b):  # Euclidian algo
        if a == 0:
            return b, 0, 1
        else:
            g, y, x = Helper.egcd(b % a, a)
            return g, x - (b // a) * y, y


class EllipticCurve:
    def __init__(self, a, b, mod):
        self.a = a
        self.b = b
        self.mod = mod


class PointOnTheEllipticCurve:
    def __init__(self, x, y, curve):
        self.x = x
        self.y = y
        self.curve = curve
        self.prepareData()

    def prepareData(self):
        self.y1 = Helper.modularSqrt((self.x ** 3 + self.curve.a * self.x + self.curve.b) % self.curve.mod,
                                     self.curve.mod)
        if self.y1 == 0:
            raise Exception("No solution for y1 on curve.")

    def addition(self, point):
        z = (point.x ** 3 + self.curve.a * point.x + self.curve.b) % self.curve.mod
        y2 = Helper.modularSqrt(z, self.curve.mod)

        if y2 != 0 and self.x != point.x:
            s = (point.y - self.y) * Helper.modOfValue(point.x - self.x, self.curve.mod)
            x3 = (s ** 2 - point.x - self.x) % self.curve.mod
            y3 = (s * (point.x - x3) - point.y) % self.curve.mod
            return PointOnTheEllipticCurve(x3, y3, self.curve)
        if y2 != 0 and self.x == point.x:
            s = ((3 * self.x ** 2) + self.curve.a) * Helper.modOfValue(2 * self.y, self.curve.mod)
            x2 = (s ** 2 - 2 * self.x) % self.curve.mod
            y2 = ((s * (self.x - x2)) - self.y) % self.curve.mod
            return PointOnTheEllipticCurve(x2, y2, self.curve)

    def multiplication(self, k):
        point = self
        for _ in range(k):
            point = self.addition(self)
        return point


def main():
    curve = EllipticCurve(0, 7, 37)
    point1 = PointOnTheEllipticCurve(6, 1, curve)
    point2 = PointOnTheEllipticCurve(3, 16, curve)

    pointAdd = point1.addition(point2)
    print("x: {}, y: {}".format(pointAdd.x, pointAdd.y))

    pointMull = point1.multiplication(7)
    print("x: {}, y: {}".format(pointMull.x, pointMull.y))


main()
