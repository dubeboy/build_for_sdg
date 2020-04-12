

def estimator(data):
    avg_daily_income_population = data['region']['avgDailyIncomePopulation']
    avg_daily_income_in_usd = data['region']['avgDailyIncomeInUSD']

    impact = generate_impact(data, 10)  # challenge 1
    generate_severe_cases_by_request_time(impact, data['totalHospitalBeds'])  # challenge 2
    generate_infections_by_request_time(impact, avg_daily_income_population, avg_daily_income_in_usd)  # challenge 3

    severe_impact = generate_impact(data, 50)  # challenge 1
    generate_severe_cases_by_request_time(severe_impact, data['totalHospitalBeds'])  # challenge 2
    generate_infections_by_request_time(severe_impact, avg_daily_income_population,
                                        avg_daily_income_in_usd)  # challenge 3

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
            'infectionsByRequestedTime': currentlyInfected * int(2 ** (days / 3))}


# Challenge two
def generate_severe_cases_by_request_time(impact_data, total_hospital_beds):
    infections_by_requested_time = impact_data['infectionsByRequestedTime']

    bed_availability = int(total_hospital_beds * 0.35)
    severe_cases_by_request_time = int(infections_by_requested_time * 0.15)

    impact_data['severeCasesByRequestedTime'] = severe_cases_by_request_time
    impact_data['hospitalBedsByRequestedTime'] = severe_cases_by_request_time - bed_availability


# Challenge 3
def generate_infections_by_request_time(impact_data, avg_daily_income_population, avg_daily_income_in_usd):
    infections_by_requested_time = impact_data['infectionsByRequestedTime']

    cases_for_ICU_by_requested_time = infections_by_requested_time * 0.05
    cases_for_ventilators_by_requested_time = infections_by_requested_time * 0.02

    dollars_in_flight = infections_by_requested_time * avg_daily_income_population * avg_daily_income_in_usd * 30

    impact_data['casesForICUByRequestedTime'] = int(cases_for_ICU_by_requested_time)
    impact_data['casesForVentilatorsByRequestedTime'] = int(cases_for_ventilators_by_requested_time)
    impact_data['dollarsInFlight'] = round(dollars_in_flight, 2)

