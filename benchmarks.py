from math import radians

import requests
import pytest_benchmark

from aptfinder import locator


def big_locate():
    bounds = {'south': radians(43.548689481127205),
              'west': radians(-79.78201725278637),
              'north': radians(43.84062756586321),
              'east': radians(-79.37824735846579)}
    radiusm = 16249.199467987859
    # lat, lng
    center = (radians(43.69465852349521),
              radians(-79.58013230562608))

    return list(locator.apartments_in_radius(center, radiusm, bounds))


def test_big_locate(benchmark):
    bounds = {'south': radians(43.548689481127205),
              'west': radians(-79.78201725278637),
              'north': radians(43.84062756586321),
              'east': radians(-79.37824735846579)}
    radiusm = 16249.199467987859
    # lat, lng
    center = (radians(43.69465852349521),
              radians(-79.58013230562608))

    benchmark(big_locate)
