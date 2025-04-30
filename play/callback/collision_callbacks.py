"""Collision callbacks for sprites."""

from enum import EnumType

from pymunk import CollisionHandler

from play.callback.callback_helpers import run_callback
from play.physics import physics_space


class CollisionType(EnumType):
    SPRITE = 0
    WALL = 1


class CollisionCallbackRegistry:  # pylint: disable=too-few-public-methods
    """
    A registry for collision callbacks.
    """

    def _handle_collision(self, arbiter, _, __):
        shape_a, shape_b = arbiter.shapes
        if shape_a.collision_type in self.callbacks[True]:
            for shape_b_id, callback in self.callbacks[True][
                shape_a.collision_type
            ].items():
                if shape_b_id == shape_b.collision_type:
                    self.shape_registry[shape_a.collision_type]._touching_callback[
                        shape_a.actual_collision_type
                    ] = callback

        if shape_b.collision_type in self.callbacks[True]:
            for shape_a_id, callback in self.callbacks[True][
                shape_b.collision_type
            ].items():
                if shape_a_id == shape_a.collision_type:
                    self.shape_registry[shape_b.collision_type]._touching_callback[
                        shape_b.actual_collision_type
                    ] = callback
        return True

    def _handle_end_collision(self, arbiter, _, __):
        shape_a, shape_b = arbiter.shapes

        if shape_a.collision_type in self.callbacks[True]:
            for shape_b_id, callback in self.callbacks[True][
                shape_a.collision_type
            ].items():
                if shape_b_id == shape_b.collision_type:
                    self.shape_registry[shape_a.collision_type]._touching_callback[
                        shape_a.actual_collision_type
                    ] = None

        if shape_b.collision_type in self.callbacks[True]:
            for shape_a_id, callback in self.callbacks[True][
                shape_b.collision_type
            ].items():
                if shape_a_id == shape_a.collision_type:
                    self.shape_registry[shape_b.collision_type]._touching_callback[
                        shape_b.actual_collision_type
                    ] = None

        if shape_a.collision_type in self.callbacks[False]:
            for shape_b_id, callback in self.callbacks[False][
                shape_a.collision_type
            ].items():
                if shape_b_id == shape_b.collision_type:
                    run_callback(callback, [], [])
        if shape_b.collision_type in self.callbacks[False]:
            for shape_a_id, callback in self.callbacks[False][
                shape_b.collision_type
            ].items():
                if shape_a_id == shape_a.collision_type:
                    run_callback(callback, [], [])

        return True

    def __init__(self):
        self.callbacks = {True: {}, False: {}}
        self.shape_registry = {}
        handler: CollisionHandler = physics_space.add_default_collision_handler()
        handler.begin = self._handle_collision
        handler.separate = self._handle_end_collision

    def register(
        self, sprite_a, shape_a, shape_b, callback, collision_type, begin=True
    ):
        """
        Register a callback with a name.
        """
        shape_a.collision_type = id(shape_a)
        shape_b.collision_type = id(shape_b)
        self.shape_registry[shape_a.collision_type] = sprite_a
        shape_a.actual_collision_type = collision_type

        if not shape_a.collision_type in self.callbacks[begin]:
            self.callbacks[begin][shape_a.collision_type] = {}
        if shape_b.collision_type in self.callbacks[begin][shape_a.collision_type]:
            raise ValueError(f"Callback already registered for {shape_a} and {shape_b}")
        self.callbacks[begin][shape_a.collision_type][shape_b.collision_type] = callback


collision_registry = CollisionCallbackRegistry()
