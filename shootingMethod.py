import math

class Equation:

    a = 0
    b = 1
    h = 0.01

    p = None
    y_a = None
    dy_b = None

    def __init__(self): pass

    def points(self):
        m = int(1+(self.b - self.a)/self.h)
        points = []
        for i in range(0,m):
            points.append(self.a + self.h*i)
        return points

    def argument(self, x, y):
        return -self.p*y + self.p*(math.cos(x))**2

class RungeKutta:

    def __init__(self): pass

    @staticmethod
    def solve(equation, u0, v0, points):

        u = u0
        v = v0

        result = []

        for t in points:

            # v - derivace v(x)
            # u - hledana funkce u(x)

            # k - hodnota f -   v'
            # l - derivace -    v

            result.append({'t': t, 'y': u, 'dy': v})

            k1 = equation.argument(t, u0)
            l1 = v

            k2 = equation.argument(t + equation.h/2, u0)
            l2 = (v+k1/2)

            k3 = equation.argument(t + equation.h/2, u0)
            l3 = (v+k2/2)

            k4 = equation.argument(t + equation.h, u0)
            l4 = (v+k3)

            u += equation.h*(l1 + 2*l2 + 2*l3 + l4)/6
            v += equation.h*(k1 + 2*k2 + 2*k3 + k4)/6

        return result

class ShootingMethod:

    def __init__(self): pass

    @staticmethod
    def solve(equation, k0, eps, maxIterations):

        k1 = k0 + 0.001
        k2 = k0

        for i in range(1, maxIterations):

            R0 = RungeKutta.solve(
                equation,
                equation.y_a,
                k1,
                equation.points()
            )
            R1 = RungeKutta.solve(
                equation,
                equation.y_a,
                k2,
                equation.points()
            )

            dy_b_k1 = R0[-1]['dy'] - equation.dy_b
            dy_b_k2 = R1[-1]['dy'] - equation.dy_b

            df = (dy_b_k2 - dy_b_k1)/(k2-k1)

            k1, k2 = k2, k2 - dy_b_k2 / df

            distance = abs(dy_b_k2)

            if distance <= eps:
                print ("Vzdalenost:", distance)
                print ("Spravny nastrel y'(a):", k2)
                print ("Pocet iteraci:", i)

                return R1


##################################################################


print("Rovnice -py + p(cos(x))^2")

equation = Equation()

equation.a = 0 # float(input("Zacatek intervalu a: "))
equation.b = 1 # float(input("Konec intervalu b: "))
equation.h = 0.01 # float(input("Delka kroku: "))
equation.p = float(input("Parametr p = "))
equation.y_a = float(input("Okrajova podminka y(a): "))
equation.dy_b = float(input("Okrajova podminka y'(b): "))

k0 = float(input("Finalni hodnota y'(a): "))
eps = 0.000001 # float(input("Tolerance: "))
maxIterations = 100000 # int(input("Maximalni pocet iteraci : "))


result = ShootingMethod.solve(equation, k0, eps, maxIterations)


f = open('result.csv','w')
f.write('# x, dy, y')
f.write('\n')
for r in result:
    f.write(str(r['t']))
    f.write(',')
    f.write(str(r['dy']))
    f.write(',')
    f.write(str(r['y']))
    f.write('\n')
f.close()