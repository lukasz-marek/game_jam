import math
import random


class DataConverter(object):
    def __init__(self, display_height, display_width, wall_width, wall_height):
        self._display_height = display_height
        self._display_width = display_width
        self._wall_width = wall_width
        self._wall_height = wall_height

    def width(self):
        return int(self._display_width / self._wall_width)

    def height(self):
        return int(self._display_height / self._wall_height)

    def coordinates(self, array_x, array_y):
        return array_x * self._wall_width, array_y * self._wall_height


class Map(object):
    WALL = 1
    ROAD = 0

    def __init__(self, converter):
        array = []
        for x in range(converter.width):
            array.append([])
            for y in range(converter.height):
                array[x].append(Map.ROAD)
        self._schema = array

    @property
    def schema(self):
        return self._schema


class MapEvaluator(object):
    ACCEPTABLE = 1
    UNACCEPTABLE = 0

    def __init__(self):
        pass

    def evaluate(self, map_schema):
        schema = map_schema.schema
        return MapEvaluator.ACCEPTABLE, self._compute_cumulated_entropy(schema), self._compute_entropy(schema)

    def _compute_entropy(self, schema):  # maximize
        walls = 0
        roads = 0
        for row in schema:
            for brick in row:
                if brick == Map.WALL:
                    walls += 1
                else:
                    roads += 1

        wall_probability = walls / (walls + roads)
        road_probability = roads / (walls + roads)

        return wall_probability * (math.log(wall_probability, 2) if wall_probability > 0 else 0) + road_probability * (
            math.log(road_probability, 2) if road_probability > 0 else 0)

    def _compute_cumulated_entropy(self, schema):  # minimize
        entropy = 0
        for x in xrange(len(schema)):
            for y in xrange(len(schema[x])):
                entropy += self._compute_local_entropy(schema, x, y)
        return entropy

    def _compute_local_entropy(self, schema, x, y):
        walls = 0
        roads = 0
        for i in range(x - 1, x + 1):
            for j in range(y - 1, y + 1):
                if 0 <= i < len(schema) and 0 <= j < len(schema[i]):
                    if schema[i][j] == Map.WALL:
                        walls += 1
                    else:
                        roads += 1

        wall_probability = walls / (walls + roads)
        road_probability = roads / (walls + roads)

        return wall_probability * (math.log(wall_probability, 2) if wall_probability > 0 else 0) + road_probability * (
            math.log(road_probability, 2) if road_probability > 0 else 0)


class MapGenerator(object):

    _WALL_FREQUENCY = 20

    _OBJECT_TYPES = [Map.WALL] * _WALL_FREQUENCY + [Map.ROAD] * (100 - _WALL_FREQUENCY)

    def __init__(self, converter, evaluator):
        self._converter = converter
        self._evaluator = evaluator

    def generate(self):
        subject = Map(self._converter)
        for x in xrange(len(subject.schema)):
            for y in xrange(len(subject.schema[x])):
                subject.schema[x][y] = random.choice(MapGenerator._OBJECT_TYPES)







