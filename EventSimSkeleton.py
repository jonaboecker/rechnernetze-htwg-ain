from collections import deque
import heapq

f = open("supermarkt.txt", "w")
fc = open("supermarkt_customer.txt", "w")
fs = open("supermarkt_station.txt", "w")


# print on console and into supermarket log
def my_print(msg):
    print(msg)
    f.write(msg + '\n')


# print on console and into customer log
# k: customer name
# s: station name
def my_print1(k, s, msg):
    t = EvQueue.time
    print(str(round(t, 4)) + ':' + k + ' ' + msg + ' at ' + s)
    fc.write(str(round(t, 4)) + ':' + k + ' ' + msg + ' at ' + s + '\n')


# print on console and into station log
# s: station name
# name: customer name
def my_print2(s, msg, name):
    t = EvQueue.time
    # print(str(round(t,4))+':'+s+' '+msg)
    fs.write(str(round(t, 4)) + ':' + s + ' ' + msg + ' ' + name + '\n')


# prio:
# 1. Verlassen
# 2. Beginn
# 3. Ankunft


# class consists of instance variables:
# t: time stamp
# work: job to be done
# args: list of arguments for job to be done
# prio: used to give leaving, being served, and arrival different priorities
class Ev:
    counter = 0

    def __init__(self, t, work, args=(), prio=255):
        self.t = t
        self.n = Ev.counter
        self.work = work
        self.args = args
        self.prio = prio
        Ev.counter += 1

    def __lt__(self, other):
        # Hier definieren Sie die Vergleichslogik für Instanzen von Ev
        if self.t == other.t:
            return self.prio < other.prio
        return self.t < other.t


# class consists of
# q: event queue
# time: current time
# evCount: counter of all popped events
# methods push, pop, and start as described in the problem description

class EvQueue:
    # please implement here
    ereignisliste = []
    time = 0

    def pop(self) -> Ev:
        event = heapq.heappop(self.ereignisliste)
        EvQueue.time = event.t
        event.work()
        return event

    def push(self, event):
        heapq.heappush(self.ereignisliste, event)

    def start(self):
        while len(self.ereignisliste) != 0:
            self.pop()


# class consists of
# name: station name
# buffer: customer queue
# delay_per_item: service time
# CustomerWaiting, busy: possible states of this station
class Station:
    # please implement here
    def __init__(self, t, name):
        self.name = name
        self.t = t
        self.list = []

    def queue(self, kunde):
        if len(self.list) == 0:
            evQ.push(
                Ev(EvQueue.time + self.t * kunde.stations[kunde.station][0], kunde.verlassen_station, kunde, prio=1))
        self.list.append(kunde)

    def finish(self):
        del self.list[0]
        if len(self.list) != 0:
            evQ.push(Ev(EvQueue.time + self.t * self.list[0].stations[self.list[0].station][2],
                        self.list[0].verlassen_station, self.list[0], prio=1))


# class consists of
# statistics variables
# and methods as described in the problem description
class Customer():
    served = dict()
    dropped = dict()
    complete = 0
    duration = 0
    duration_cond_complete = 0
    count = 0

    # please implement here
    def __init__(self, stations, name, t):
        self.stations = stations
        self.station = 0
        self.name = name
        self.t = t

    def run(self):
        evQ.push(Ev(evQ.time + self.stations[self.station][0], self.ankunft_station, self, 3))

    def ankunft_station(self):
        if len(self.stations[self.station][1].list) <= self.stations[self.station][3]:
            self.stations[self.station][1].queue(self)
        else:
            # drop customer
            self.verlassen_station()
        # evQ.push(Ev(evQ.simulationszeit + self.stations[0][0], self.stations[0][1].queue, self, 2))

    def verlassen_station(self):
        if len(self.stations) - 1 > self.station:
            self.station += 1
            evQ.push(Ev(evQ.time + self.stations[self.station][0], self.ankunft_station, self, 3))


def startCustomers(einkaufsliste, name, sT, dT, mT):
    i = 1
    t = sT
    while t < mT:
        kunde = Customer(list(einkaufsliste), name + str(i), t)
        ev = Ev(t, work=kunde.run, prio=1)
        evQ.push(ev)
        i += 1
        t += dT


evQ = EvQueue()
baecker = Station(10, 'Bäcker')
metzger = Station(30, 'Metzger')
kaese = Station(60, 'Käse')
kasse = Station(5, 'Kasse')
Customer.served['Bäcker'] = 0
Customer.served['Metzger'] = 0
Customer.served['Käse'] = 0
Customer.served['Kasse'] = 0
Customer.dropped['Bäcker'] = 0
Customer.dropped['Metzger'] = 0
Customer.dropped['Käse'] = 0
Customer.dropped['Kasse'] = 0
einkaufsliste1 = [(10, baecker, 10, 10), (30, metzger, 5, 10), (45, kaese, 3, 5), (60, kasse, 30, 20)]
einkaufsliste2 = [(30, metzger, 2, 5), (30, kasse, 3, 20), (20, baecker, 3, 20)]
startCustomers(einkaufsliste1, 'A', 0, 200, 30 * 60 + 1)
startCustomers(einkaufsliste2, 'B', 1, 60, 30 * 60 + 1)
evQ.start()
my_print('Simulationsende: %is' % EvQueue.time)
my_print('Anzahl Kunden: %i' % (Customer.count
                                ))
my_print('Anzahl vollständige Einkäufe %i' % Customer.complete)
x = Customer.duration / Customer.count
my_print(str('Mittlere Einkaufsdauer %.2fs' % x))
x = Customer.duration_cond_complete / Customer.complete
my_print('Mittlere Einkaufsdauer (vollständig): %.2fs' % x)
S = ('Bäcker', 'Metzger', 'Käse', 'Kasse')
for s in S:
    x = Customer.dropped[s] / (Customer.served[s] + Customer.dropped[s]) * 100
    my_print('Drop percentage at %s: %.2f' % (s, x))

f.close()
fc.close()
fs.close()
