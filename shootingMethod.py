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

            k1 = equation.h * v
            l1 = equation.h * equation.argument(t, u)

            k2 = equation.h * (v + 0.5*l1)
            l2 = equation.h * equation.argument(t + 0.5*equation.h, u + 0.5*k1)

            k3 = equation.h * (v + 0.5*l2)
            l3 = equation.h * equation.argument(t + 0.5*equation.h, u + 0.5*k2)

            k4 = equation.h * (v + l3)
            l4 = equation.h * equation.argument(t + equation.h, u + k3)

            u += (k1 + 2*k2 + 2*k3 + k4)/6
            v += (l1 + 2*l2 + 2*l3 + l4)/6

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

            d_dy_b_k1 = R0[-1]['dy'] - equation.dy_b
            d_dy_b_k2 = R1[-1]['dy'] - equation.dy_b

            df = (d_dy_b_k2 - d_dy_b_k1)/(k2-k1)

            k1, k2 = k2, k2 - d_dy_b_k2 / df

            distance = abs(d_dy_b_k2)

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

k0 = float(input("Pocatecni nastrel y'(a): "))
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