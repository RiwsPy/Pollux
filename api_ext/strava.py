from . import call as base_call

BASE_URL = "https://www.strava.com/api/v3"
ACCESS_TOKEN = '18c021e5ae0235256bb279a540f55837f68b7e4b'

"""
        data={
            'bounds': f"{LAT_MIN}, {LNG_MIN}, {LAT_MAX}, {LNG_MAX}",
            'activityType': 'Walk',
            'max_cat': 1,
        })

        url='https://www.strava.com/api/v3/segments/XXXXX/streams'
"""


def call(self, url: str, **kwargs) -> dict:
    url = BASE_URL + url

    return base_call(self,
                     url=url,
                     headers={'Authorization': f'Bearer {ACCESS_TOKEN}'},
                     **kwargs)
