from random import shuffle, randint

def dist(p, q):
    return abs(p[0] - q[0]) + abs(p[1] - q[1])

class Ride:
    def __init__(self, a, b, x, y, s, f):
        self.start = (a, b)
        self.end = (x, y)
        self.stime = s
        self.ftime = f
        self.taken = False
        self.feasible_cars = set(range(F))

    def set_index(self, ind):
        self.index = ind

    def feasible_cars_multiplier(self):
        if len(self.feasible_cars) == 0:
            return 0
        K = 20
        return (K - (K-1)*len(self.feasible_cars)/F)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.index)
        #return 'Start: {:s}  End: {:s}  Times: {:s}-{:s}\n'.format(str(self.start), str(self.end), str(self.stime), str(self.ftime))

class Car:
    def __init__(self, index, pos=(0,0)):
        self.pos = pos
        self.assigned = []
        self.free_at = 0
        self.index = 0

    def calc_free(self, ride):
        fat = self.free_at
        fat += dist(self.pos, ride.start)
        fat = max(fat, ride.stime)
        fat += dist(ride.end, ride.start)
        return fat

    def assign_ride(self, ride):
        self.assigned.append(ride)
        self.free_at = self.calc_free(ride)
        self.pos = ride.end
        ride.taken = True

    def score_ride(self, ride):
        if ride.taken:
            return -float('inf')

        would_end = self.calc_free(ride)
        points_got = 0
        time_taken = would_end - self.free_at

        if would_end <= ride.ftime:
            points_got += dist(ride.start, ride.end)

            if self.free_at + dist(self.pos, ride.start) <= ride.stime:
                points_got += B

        if points_got == 0:
            if self.index in ride.feasible_cars:
                ride.feasible_cars.remove(self.index)

        return (points_got ** 0.75 / time_taken**(1.5 - (rides_assigned/N))) * ride.feasible_cars_multiplier()

R, C, F, N, B, T = map(int, input().split()) # rows, columns, vehicles, rides, bonus, time_of_simulation
rides, cars = [], [Car(f) for f in range(F)]

for ind in range(N):
    rides.append(Ride(*map(int, input().split())))
    rides[-1].set_index(ind)


rides_assigned = 0
while rides_assigned < N:
    cars.sort(key=lambda x: x.free_at)

    firstcars = cars[:F//3]
    shuffle(firstcars)

    for c in firstcars:
        br, bs = -1, -float('inf')
        for r in rides:
            if not r.taken:
                score = c.score_ride(r)
                if score > bs:
                    br, bs = r, score
        if br != -1:
            c.assign_ride(br)
            rides_assigned += 1

# Format output
for car in cars:
    print(str(len(car.assigned)) + ' ' + ' '.join(map(lambda x: str(x.index), car.assigned)))
