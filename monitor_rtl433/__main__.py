from monitor_rtl433 import run
from monitor_rtl433.metrics import Metric, MetricFilter, MetricDescription

def degc2f(x):
    return x * 9.0/5.0 + 32.0

def km2mi(x):
    return x * 0.62137


class AcuriteTower(MetricFilter):
    def __init__(self, id, report_id):
        self.id = id
        self.report_id = report_id
        # The `_match` property will be used to determine which sensor records
        # this filter will be applied to
        self._match = {"model": "Acurite-Tower", "id" : self.id}
        
    def process(self, reading):
        """Takes a single sensor record, and converts it to 0 or more metrics
        """
        sensor_id = "%s" % str(self.report_id) 
        yield Metric('temperature_F', degc2f(reading['temperature_C']), labels={'sensor_id': sensor_id})
        yield Metric('humidity_percent', reading['humidity'], labels={'sensor_id': sensor_id})
        yield Metric('battery_ok', reading['battery_ok'], labels={'sensor_id': sensor_id})

class Unni(MetricFilter):
    def __init__(self, id):
        self.id = id
        self._match = {"model": "Oregon-THGR810", "id" : self.id}
        
    def process(self, reading):
        """Takes a single sensor record, and converts it to 0 or more metrics
        """
        sensor_id = "%s" % str(self.id) 
        yield Metric('temperature_F', degc2f(reading['temperature_C']), labels={'sensor_id': sensor_id})
        yield Metric('humidity_percent', reading['humidity'], labels={'sensor_id': sensor_id})
        yield Metric('battery_ok', reading['battery_ok'], labels={'sensor_id': sensor_id})


class Acurite5n1(MetricFilter):
    def __init__(self, id):
        self.id = id
        self._match = {"model": "Acurite-5n1", "message_type": 56 ,"id": self.id}

    def process(self, reading):
        sensor_id = "2468"
        
        yield Metric('temperature_F', reading['temperature_F'], labels={'sensor_id': sensor_id})
        yield Metric('humidity_percent', reading['humidity'], labels={'sensor_id': sensor_id})
        yield Metric('battery_ok', reading['battery_ok'], labels={'sensor_id': sensor_id})

class Acurite5n1_windnrain(MetricFilter):
    def __init__(self, id):
        self.id = id
        self._match = {"model": "Acurite-5n1", "message_type": 49 ,"id": self.id}

    def process(self, reading):
        sensor_id = "2468"
        
        yield Metric('wind_avg_mph', km2mi(reading['wind_avg_km_h']), labels={'sensor_id': sensor_id})
        yield Metric('wind_dir_deg', reading['wind_dir_deg'], labels={'sensor_id': sensor_id})
        yield Metric('rain_in', reading['rain_in'], labels={'sensor_id': sensor_id})


def main():
    # List all metric names that we will expose
    metric_descriptions = [
        MetricDescription("temperature_F", "gauge", "Temperature in degrees F"),
        MetricDescription("humidity_percent", "gauge", "Relative humidity in percent"),
        MetricDescription("battery_ok", "gauge", "1 when battery normal, 0 when low"),
        MetricDescription("wind_avg_mph", "gauge", "Average wind speed in mph"),
        MetricDescription("wind_dir_deg", "gauge", "Wind direction in degrees"),
        MetricDescription("rain_in", "counter", "Rain accumulation in inches"),
    ]
    # For each sensor that we want to convert to metrics, create a MetricFilter class that will do that
    metric_filters = [
        Acurite5n1(1226),
        Acurite5n1_windnrain(1226),
        AcuriteTower(11825, 11825),
        AcuriteTower(710, 3209),
        AcuriteTower(3935, 3935),
        Unni(196),
        Unni(126),
        Unni(98),
    ]

    run(metric_descriptions, metric_filters)

if __name__ == '__main__':
    main()
