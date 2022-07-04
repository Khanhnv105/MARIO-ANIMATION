import pygame

from data.engine.VFX.particles_manager import ParticlesManager
from data.engine.entity.collideable_entities_group import CollideableEntitiesGroup


class CollideableGroupWithParticles(CollideableEntitiesGroup):

    def __init__(self, game_scene, map_size):
        super().__init__(game_scene, map_size)
        self.particles_manager = ParticlesManager(game_scene)

    def clear(self):
        super().clear()
        self.particles_manager.clear()

    def update(self, **kwargs):
        super().update(**kwargs)
        self.particles_manager.update(**kwargs)

    def draw(self, surface: pygame.Surface, offset=(0, 0), rect=False):

        visible_entities = self._visible_entities
        particles = self.particles_manager.get_particles()
        layers = sorted(list(visible_entities.keys()) + list(particles.keys()))

        for layer in layers:
            if layer in visible_entities:
                for entity in visible_entities[layer]:
                    entity.draw(surface, offset)

            if layer in particles:
                for particle in particles[layer]:
                    particle.draw(surface, offset)

        if rect:
            for layer in layers:
                if layer in visible_entities:
                    for entity in visible_entities[layer]:
                        pygame.draw.rect(
                            surface,
                            (0, 0, 0),
                            (
                                entity.rectangle.x - offset.x,
                                entity.rectangle.y - offset.y,
                                entity.rectangle.w,
                                entity.rectangle.h
                            ),
                            2
                        )