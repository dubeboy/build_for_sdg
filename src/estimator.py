# data = reported cases
# days, weeks, months
import json


def estimator(data):
    impact = generate_impact(data, 10)
    generate_severe_cases_by_request_time(impact, data['totalHospitalBeds'])

    severe_impact = generate_impact(data, 50)
    generate_severe_cases_by_request_time(severe_impact, data['totalHospitalBeds'])

    data = {'data': data, 'impact': impact, 'severeImpact': severe_impact}
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


# Challenge two
def generate_severe_cases_by_request_time(impact_data, total_hospital_beds):
    infections_by_requested_time = impact_data['infectionsByRequestedTime']

    bed_availability = total_hospital_beds * 0.35
    severe_cases_by_request_time = infections_by_requested_time * 0.15

    impact_data['severeCasesByRequestedTime'] = severe_cases_by_request_time
    impact_data['hospitalBedsByRequestedTime'] = severe_cases_by_request_time - bed_availability


# Challenge 3
def generate_infections_by_request_time(impact_data, avg_daily_income_population, avg_daily_income_in_usd):
    infections_by_requested_time = impact_data['infectionsByRequestedTime']

    cases_for_ICU_by_requested_time = infections_by_requested_time * 0.05
    cases_for_ventilators_by_requested_time = infections_by_requested_time * 0.02

    dollars_in_flight = infections_by_requested_time * avg_daily_income_population * avg_daily_income_in_usd * 30

    impact_data['casesForICUByRequestedTime'] = cases_for_ICU_by_requested_time
    impact_data['casesForVentilatorsByRequestedTime'] = cases_for_ventilators_by_requested_time
    impact_data['dollarsInFlight'] = round(dollars_in_flight, 2)

