
def estimator(data):
    avg_daily_income_population = data['region']['avgDailyIncomePopulation']
    avg_daily_income_in_usd = data['region']['avgDailyIncomeInUSD']
    time_to_elapse = data['timeToElapse']
    period_type = data['periodType']

    impact = generate_impact(data, 10, period_type, time_to_elapse)  # challenge 1
    generate_severe_cases_by_request_time(impact, data['totalHospitalBeds'])  # challenge 2
    generate_infections_by_request_time(impact, avg_daily_income_population,
                                        avg_daily_income_in_usd, period_type, time_to_elapse)  # challenge 3

    severe_impact = generate_impact(data, 50, period_type, time_to_elapse)  # challenge 1
    generate_severe_cases_by_request_time(severe_impact, data['totalHospitalBeds'])  # challenge 2
    generate_infections_by_request_time(severe_impact, avg_daily_income_population,
                                        avg_daily_income_in_usd, period_type, time_to_elapse)  # challenge 3

    data = {'data': data, 'impact': impact, 'severeImpact': severe_impact}
    return data


# Challenge one
def generate_impact(data, multiplier, period_type, time_to_elapse):
    currently_infected = data["reportedCases"] * multiplier
    days = get_days(period_type, time_to_elapse)

    factor = int(days / 3)

    return {'currentlyInfected': currently_infected,
            'infectionsByRequestedTime': currently_infected * (2 ** factor)}


# Challenge two
def generate_severe_cases_by_request_time(impact_data, total_hospital_beds):
    severe_cases_by_request_time = impact_data['infectionsByRequestedTime'] * 0.15
    bed_availability = total_hospital_beds * 0.35

    impact_data['severeCasesByRequestedTime'] = int(severe_cases_by_request_time)
    impact_data['hospitalBedsByRequestedTime'] = int(bed_availability - severe_cases_by_request_time)


# Challenge 3
def generate_infections_by_request_time(impact_data,
                                        avg_daily_income_population,
                                        avg_daily_income_in_usd,
                                        period_type,
                                        time_to_elapse):
    infections_by_requested_time = impact_data['infectionsByRequestedTime']

    cases_for_ICU_by_requested_time = infections_by_requested_time * 0.05
    cases_for_ventilators_by_requested_time = infections_by_requested_time * 0.02

    days = get_days(period_type, time_to_elapse)

    dollars_in_flight = (infections_by_requested_time * avg_daily_income_population * avg_daily_income_in_usd) / days

    impact_data['casesForICUByRequestedTime'] = int(cases_for_ICU_by_requested_time)
    impact_data['casesForVentilatorsByRequestedTime'] = int(cases_for_ventilators_by_requested_time)
    impact_data['dollarsInFlight'] = round(dollars_in_flight, 2)


# Private methods
def get_days(period_type, time_to_elapse):
    if period_type == 'weeks':
        days = time_to_elapse * 7
    elif period_type == 'months':
        days = time_to_elapse * 30
    else:
        days = time_to_elapse

    return int(days)


