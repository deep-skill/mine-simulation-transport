import simpy

class Truck:
    def __init__(self, env : simpy.Environment, capacity_tons, data):
        self.env = env
        self.capacity_tons = capacity_tons
        self.data = data

        self.tons = 0
        self.route = None

    def get_tons(self):
        return self.tons

    def assign_tons(self, tons):
        self.tons = tons

    def fill_tons(self):
        self.tons = self.capacity_tons

    def set_route(self, route):
        self.route = route

    def move(self):
        self.report_position()

        while self.route:
            yield self.env.process(self.route(self))
            self.report_position()

    def report_position(self):
        pass
