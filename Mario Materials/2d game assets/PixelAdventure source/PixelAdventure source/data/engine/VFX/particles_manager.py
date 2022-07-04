

class ParticlesManager:
    """
    Clase basica de particulas usada para
    organizar las mismas en layers
    """
    def __init__(self, scene):
        self.scene = scene
        self._particles = {}
        self._amount = 0

    def __iter__(self):
        return self._particles

    def clear(self):
        self._particles.clear()

    def get_particles(self):
        return self._particles

    def amount(self):
        return self._amount

    def destroy(self, particle):
        self._particles[particle.get_layer()].remove(particle)
        self._amount -= 1

    def add(self, particle):
        if not particle.get_layer() in self._particles:
            self._particles[particle.get_layer()] = []

        self._particles[particle.get_layer()].append(particle)
        self._amount += 1

    def update(self, **kwargs):
        for layer in self._particles:
            for particle in self._particles[layer]:
                particle.update(**kwargs)

    def draw(self, surface, offset=None):
        for layer in self._particles:
            for particle in self._particles[layer]:
                particle.draw(surface, offset)
