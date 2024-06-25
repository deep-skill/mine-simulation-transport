import simpy

class Storage:
    def __init__(self, env : simpy.Environment, capacity, data, working_time=None):
        self.env = env
        self.queue = simpy.Resource(env, capacity=capacity)
        self.working_time = working_time
        self.data = data

        if not self.data: self.data = {}

        self.data['waiting_time'] = 0
        self.data['using_time'] = 0
        self.data['number_of_server_trucks'] = 0
        self.data['number_of_server_trucks_without_waiting'] = 0

    def get_time(self):
        if self.working_time == None:
            return 0
        else:
            return self.working_time()


class Cruce(Storage):
    def work(self, truck, time=None):
        arrival_time = self.env.now

        with self.queue.request() as request:
            yield request

            start_time = self.env.now
            self.data['waiting_time'] += start_time - arrival_time
            self.data['number_of_server_trucks'] += 1
            if arrival_time == start_time: self.data['number_of_server_trucks_without_waiting'] += 1

            if not time: time = self.get_time()

            yield self.env.timeout(time)

            finish_time = self.env.now
            self.data['using_time'] += finish_time - start_time

    def work_process(self, truck, time):
        return self.env.process(self.work(truck, time))

    def report(self):
        print(f"REPORTE cruce {self.data['name']}:")
        print("Tiempo de espera en el cruce {0}: {1:.3f}".format(self.data['name'], self.data['waiting_time']))
        print(f"Cantidad de camiones atendidos: {self.data['number_of_server_trucks']}")
        print(f"Cantidad de camiones atendidos sin espera: {self.data['number_of_server_trucks_without_waiting']}")
        print("")


class Shovel(Storage):
    def work(self, truck, time=None):
        arrival_time = self.env.now

        with self.queue.request() as request:
            yield request

            start_time = self.env.now
            self.data['waiting_time'] += start_time - arrival_time
            self.data['number_of_server_trucks'] += 1
            if arrival_time == start_time: self.data['number_of_server_trucks_without_waiting'] += 1

            if not time: time = self.get_time()

            yield self.env.timeout(time)

            truck.fill_tons()

            finish_time = self.env.now
            self.data['using_time'] += finish_time - start_time

    def work_process(self, truck, time=None):
        return self.env.process(self.work(truck, time))

    def report(self):
        total_time = self.env.now
        name = self.data['name']

        print(f"REPORTE Pala {self.data['name']}:")
        print("Tiempo de uso en la pala {0}: {1:.3f}".format(name, self.data['using_time']))
        print("Eficiencia de la pala {0}: {1:.3f}%".format(name, self.data['using_time'] / total_time * 100))
        print("Tiempo de espera en la pala {0}: {1:.3f}".format(name, self.data['waiting_time']))
        print(f"Cantidad de camiones atendidos: {self.data['number_of_server_trucks']}")
        print(f"Cantidad de camiones atendidos sin espera: {self.data['number_of_server_trucks_without_waiting']}")
        print("")


class Dump(Storage):
    def __init__(self, env : simpy.Environment, capacity, data, working_time=None):
        super().__init__(env, capacity, data, working_time)
        self.data['reserved_tons'] = 0

    def work(self, truck, time=None):
        arrival_time = self.env.now

        with self.queue.request() as request:
            yield request

            start_time = self.env.now
            self.data['waiting_time'] += start_time - arrival_time
            self.data['number_of_server_trucks'] += 1
            if arrival_time == start_time: self.data['number_of_server_trucks_without_waiting'] += 1

            if not time: time = self.get_time()

            yield self.env.timeout(time)

            self.data['reserved_tons'] += truck.get_tons()
            truck.assign_tons(0)

            finish_time = self.env.now
            self.data['using_time'] += finish_time - start_time

    def work_process(self, truck, time=None):
        return self.env.process(self.work(truck, time))

    def report(self):
        print(f"REPORTE botadero {self.data['name']}:")
        print(f"Desmonte (en toneladas): {self.data['reserved_tons']}")
        print("")


class Placa(Storage):
    def __init__(self, env : simpy.Environment, capacity, data, working_time=None):
        super().__init__(env, capacity, data, working_time)
        self.data['reserved_tons'] = 0

    def work(self, truck, time=None):
        arrival_time = self.env.now

        with self.queue.request() as request:
            yield request

            start_time = self.env.now
            self.data['waiting_time'] += start_time - arrival_time
            self.data['number_of_server_trucks'] += 1
            if arrival_time == start_time: self.data['number_of_server_trucks_without_waiting'] += 1

            if not time: time = self.get_time()

            yield self.env.timeout(time)

            self.data['reserved_tons'] += truck.get_tons()
            truck.assign_tons(0)

            finish_time = self.env.now
            self.data['using_time'] += finish_time - start_time

    def work_process(self, truck, time=None):
        return self.env.process(self.work(truck, time))

    def report(self):
        print(f"REPORTE {self.data['name']}:")
        print(f"Mineral (en toneladas): {self.data['reserved_tons']}")
        print("")

