import pytest
import requests
import pytest_benchmark


def request_big_url():
    url = 'http://localhost:8000/get_apts?south=43.548689481127205&west=-79.78201725278637&north=43.84062756586321&east=-79.37824735846579&radius=16249.199467987859&center_lat=43.69465852349521&center_lng=-79.58013230562608&coordtype=degrees'
    r = requests.get(url)
    return r.json()


def test_big_request(benchmark):
    benchmark(request_big_url)
