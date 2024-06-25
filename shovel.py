import simpy

class Shovel:
    def __init__(self, env : simpy.Environment, capacity, data):
        self.env = env
        self.queue = simpy.Resource(env, capacity=capacity)
        self.data = data

        # data

        self.data['waiting_time'] = 0
        self.data['using_time'] = 0
        self.data['number_of_served_trucks'] = 0
        self.data['number_ofk
