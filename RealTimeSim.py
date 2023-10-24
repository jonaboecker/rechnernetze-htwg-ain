import time
from collections import deque
import heapq
import threading
from time import sleep

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
    t = time.time() - t0
    print(str(round(t, 4)) + ':' + k + ' ' + msg + ' at ' + s)
    fc.write(str(round(t, 4)) + ':' + k + ' ' + msg + ' at ' + s + '\n')


# print on console and into station log
# s: station name
# name: customer name
def my_print2(s, msg, name):
    t = time.time() - t0
    # print(str(round(t,4))+':'+s+' '+msg)
    fs.write(str(round(t, 4)) + ':' + s + ' ' + msg + ' ' + name + '\n')


# prio:
# 1. Verlassen
# 2. Beginn
# 3. Ankunft


# class consists of
# name: station name
# buffer: customer queue
# delay_per_item: service time
# CustomerWaiting, busy: possible states of this station
class Station(threading.Thread):
    pass

    def __init__(self, t, name):
        super().__init__()
        self.name = name
        self.delay_per_item = t
        self.buffer = []
        self._lock = threading.Lock()
        self.current_customer = None
        self.CustomerWaitingEv = threading.Event

    def run(self):
        while time.time() - t0 < runtime:
            if len(self.buffer) != 0:
                self.current_customer = self.buffer[0]
                del self.buffer[0]
                my_print2(self.name, 'bedient', self.current_customer.name)
                sleep(self.delay_per_item * self.current_customer.stations[self.current_customer.station][2])
                my_print2(self.name, 'verabschiedet', self.current_customer.name)
                self.current_customer.cond.notify()
            else:
                #self.CustomerWaitingEv.clear()
                self.CustomerWaitingEv.wait() #=0

    def queue(self, kunde):
        my_print2(self.name, 'stellt an', self.current_customer.name)
        self.buffer.append(kunde)
        if not self.CustomerWaitingEv.is_set():
            self.CustomerWaitingEv.set() #=1

    # def queue(self, kunde):
    #     self._lock.acquire()
    #     if self.current_customer is None:
    #         self.current_customer = kunde
    #         self._lock.release()
    #         my_print2(self.name, 'bedient', self.current_customer.name)
    #         sleep(self.delay_per_item * self.current_customer.stations[self.current_customer.station][2])
    #         self.finish()
    #     else:
    #         self._lock.release()
    #         self.buffer.append(kunde)
    #         my_print2(self.name, 'stellt an', self.current_customer.name)


# class consists of
# statistics variables
# and methods as described in the problem description
class Customer(threading.Thread):
    pass
    served = dict()
    dropped = dict()
    complete = 0
    duration = 0
    duration_cond_complete = 0
    count = 0

    # please implement here
    def __init__(self, stations, name, t):
        super().__init__()
        self.stations = stations
        self.station = 0
        self.name = name
        self.has_been_dropped = False
        self.start_time = time.time()
        self.cond = threading.Condition()

    def run(self):
        for station in self.stations:
            my_print1(self.name, station[1].name, 'walks')
            sleep(station[0])
            my_print1(self.name, station[1].name, 'arrives')
            station[1].queue()
            self.cond.wait()
            my_print1(self.name, station[1].name, 'finished')
        my_print1(self.name, 'None', 'finished')

def startCustomers(einkaufsliste, name, sT, dT):
    i = 1
    t = sT
    while t < runtime:
        kunde = Customer(list(einkaufsliste), name + str(i), t)
        threading.Thread(target=kunde.run).start()
        i += 1
        sleep(dT)
        t = time.time() -t0


#evQ = EvQueue()
baecker = Station(10, 'Bäcker')
metzger = Station(30, 'Metzger')
kaese = Station(60, 'Käse')
kasse = Station(5, 'Kasse')
thread_baecker = threading.Thread(target=baecker.run)
thread_metzger = threading.Thread(target=metzger.run)
thread_kaese = threading.Thread(target=kaese.run)
thread_kasse = threading.Thread(target=kasse.run)
thread_baecker.start()
thread_metzger.start()
thread_kaese.start()
thread_kasse.start()
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
runtime = 30 * 60
t0 = time.time()
thread_K1 = threading.Thread(target=startCustomers, args=(einkaufsliste1, 'A', 0, 200))
thread_K2 = threading.Thread(target=startCustomers, args=(einkaufsliste2, 'B', 1, 60))
thread_K1.start()
thread_K2.start()
thread_baecker.join()
thread_metzger.join()
thread_kaese.join()
thread_kasse.join()
t1 = time.time()
my_print('Simulationsende: %is' % t1)
print(Customer.dropped)
print(Customer.served)
my_print('Anzahl Kunden: %i' % Customer.count)
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
