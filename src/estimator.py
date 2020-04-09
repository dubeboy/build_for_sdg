# data = reported cases
# days, weeks, months
import json


def estimator(data):
    data = {'data': data, 'impact': generate_impact(data, 10), 'severeImpact': generate_impact(data, 50)}
    return data


def generate_impact(data, multiplier):
    currentlyInfected = data["reportedCases"] * multiplier
    infections_by_requested_time = data['timeToElapse']
    period_type = data['periodType']

    if period_type == 'weeks':
        days = infections_by_requested_time * 7
    elif period_type == 'months':
        days = infections_by_requested_time * 30
    else:
        days = infections_by_requested_time

    return {'currentlyInfected': currentlyInfected,
            'infectionsByRequestedTime': currentlyInfected * (2 ** int(days / 3))}


def main():
    js = """
      {
    "region": {
      "name": "Africa",
      "avgAge": 19.7,
      "avgDailyIncomeInUSD": 5,
      "avgDailyIncomePopulation": 0.71
    },
    "periodType": "days",
    "timeToElapse": 28,
    "reportedCases": 50,
    "population": 66622705,
    "totalHospitalBeds": 1380614
  }
    """
    js = json.loads(js)
    print(estimator(js))


main()
