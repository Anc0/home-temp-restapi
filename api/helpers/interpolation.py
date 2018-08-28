from datetime import timedelta, datetime

import pytz
from numpy import mean
from scipy.interpolate import interp1d


class Interpolation:

    def __init__(self, ticks: int = 13):
        """
        Initialize parameters
        :param ticks: number of ticks to interpolate to (start and finish time are already 2 ticks).
        """
        self.epoch = datetime(1970, 1, 1, tzinfo=pytz.UTC)
        self.ticks = ticks - 2
        if self.ticks < 0:
            raise ValueError("There should be at least 2 ticks - start and finish")

    def tick(self, data: list):
        """
        Take data and create self.ticks number of aggregated data.
        :param data: list of dicts with created and value attributes
        :return: interpolated data
        """
        # Sort data to get minimum and maximum
        data.sort(key=lambda x: x['created'])

        # Get min and max time
        minTime = data[0]['created']
        maxTime = data[len(data) - 1]['created']

        # Calculate time range and tick step
        range = (maxTime - minTime).total_seconds()
        step = range / (self.ticks + 1)

        # Create results list with datetimes already calculated
        results = [{'created': minTime}]
        currTime = minTime + timedelta(seconds=step)
        while currTime <= maxTime:
            results.append({'created': currTime})
            currTime += timedelta(seconds=step)

        # Fill results with values if there is no data in a tick, leave it empty for now
        for result in results:
            currData = [x['value'] for x in data if
                        result['created'] - timedelta(seconds=(step / 2)) <= x['created'] <= result[
                               'created'] + timedelta(seconds=(step / 2))]
            if len(currData) > 0:
                result['value'] = mean(currData)

        # Initialize interpolation object
        interpolate = interp1d(x=[(x['created'] - self.epoch).total_seconds() for x in data],
                               y=[x['value'] for x in data])

        # Interpolate results with no value key
        for result in results:
            if not 'value' in result:
                result['value'] = float(interpolate((result['created'] - self.epoch).total_seconds()))

        # Fill the missing remaining values and return the results
        return results
