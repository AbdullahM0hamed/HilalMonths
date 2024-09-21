import json
import re

from datetime import datetime

sightings = open('hilal-months.json', 'r').read()
jsonified = {}

def get_groups(text):
    return re.findall('"(.*?)"', re.search("groups.:\s\[(.*)\]", text, re.S).group(1))

def get_group(group, text):
    group_data = ""

    try:
        group_data = "".join(re.search(f'"{group}"' + ':\s*(\{.*?)(,\n\s*"[A-Za-z]+)', text, re.S).group(1))
    except AttributeError:
        group_data = "".join(re.search(f'"{group}"' + ':\s*(\{.*?.*)\}\s*\Z', text, re.S).group(1))

    return group_data

def calculate_acceptable_date_diff(curr, previous):
    year_diff = int(curr[0]) - int(previous[0])
    later_month = (year_diff * 12) + int(curr[1])
    month_diff = later_month - int(previous[1])
    return [29 * month_diff, 30 * month_diff]

def validate_group(group, jsonified, text):
    group_data = None
    group_json = None
    if jsonified:
        found = group in jsonified.keys()
        if found:
            group_json = jsonified[group]
            print(f'✅ - {group} Data Exists')
            print(f'✅ - {group} Valid JSON')
        else:
            print(f'❎ - {group} Data Exists')
            print(f'❎ - {group} Valid JSON')
    else:
        try:
            group_data = get_group(group, text)
            print(f'✅ - {group} Data Exists')
            group_json = json.loads(group_data)
            print(f'✅ - {group} Valid JSON')
        except (Exception, json.decoder.JSONDecodeError) as e:
            if type(e) is json.decoder.JSONDecodeError:
                print(f'❎ - {group} Valid JSON')
            else:
                print(f'❎ - {group} Data Exists')

    if group_json:
        years = [*group_json.keys()]
        if [x for x in years if re.search('^\d+$', x)] == years:
            print(f'✅ - {group} Numeric Years')
        else:
            print(f'❎ - {group} Numeric Years')
            print('Invalid Year(s): ' + ' and '.join([x for x in years if not re.search('^\d+$', x)]) + f' for {group}')

        years.sort(key=int)
        years = years[::-1]

        numeric = True
        non_numeric = []
        invalid_dates = []
        valid_diffs = True
        invalid_diffs = []

        # Cases where the mistake is from the committee and not a mistake from the json
        suppressed = [
                ("Supreme Court Of Afghanistan", ["1445", "9"], ["1445", "8"]),
                ("All Ceylon Jamiyyathul Ulama", ["1445", "7"], ["1445", "6"])
        ]

        for y_index, year in enumerate(years):
            months = [*group_json[year].keys()]
            if [x for x in months if re.search('^\d+$', x)] != months:
                numeric = False
                non_numeric.extend([f'{x}/{year}' for x in months if not re.search('^\d+$', x)])

            months.sort(key=int)
            months = months[::-1]
            skip = False
            for index, month in enumerate(months):
                date = group_json[year][month]
                curr = [year, month]
                previous = None
                try:
                    parsed_curr = datetime.strptime(date, '%d/%m/%Y')
                    if index < len(months) - 1 or y_index < len(years) - 1:
                        prev = None

                        try:
                            prev = group_json[year][months[index + 1]]
                            previous = [year, months[index + 1]]
                        except:
                            prev_index = years[y_index + 1]
                            prev_year = group_json[prev_index]
                            prev_months = [*prev_year.keys()]
                            prev_months.sort(key=int)
                            prev_months = prev_months[::-1]
                            prev = prev_year[prev_months[0]]
                            previous = [prev_index, prev_months[0]]

                        if len(curr) == 2 and len(previous) == 2:
                            min_max = calculate_acceptable_date_diff(curr, previous)
                            parsed_prev = datetime.strptime(prev, '%d/%m/%Y')
                            day_diff = abs(parsed_curr - parsed_prev).days

                            if day_diff < min_max[0] or day_diff > min_max[1]:
                                for to_ignore in suppressed:
                                    skip = group == to_ignore[0] and to_ignore[1] == curr and to_ignore[2] == previous

                                    if skip:
                                        break

                                if not skip:
                                    if valid_diffs:
                                        valid_diffs = False
                                        print(f'❎ - {group} Valid Distance Between Dates')

                                    invalid_diffs.append(f'{curr[0]}/{curr[1]}: {date} to {previous[0]}/{previous[1]}: {prev}')
                                else:
                                    print(f'❗ - Suppressed Known Erroneous Date From Committee: {group}, Date: {previous[0]}/{previous[1]} to {curr[0]}/{curr[1]}')
                except ValueError:
                    invalid_dates.append(f'Hijri {month}/{year} - Gregorian {date}')

        if not skip:
            if valid_diffs:
                print(f'✅ - {group} Valid Distance Between Dates')
            else:
                print('Invalid Distances Between The Following Dates: ' + ', '.join(invalid_diffs))

        if numeric:
            print(f'✅ - {group} Numeric Months')
        else:
            print(f'❎ - {group} Numeric Months')
            print(f'Invalid Month(s) For {group}: ' + ','.join(non_numeric))

        if not invalid_dates:
            print(f'✅ - {group} Valid Dates')
        else:
            print(f'❎ - {group} Valid Dates')
            print(f'Invalid Date(s) For {group}: ' + ', '.join(invalid_dates))


jsonified = None
try:
    jsonified = json.loads(sightings)
    print('✅ - Valid JSON')
except json.decoder.JSONDecodeError:
    print('❎ - Valid JSON')

groups = []

try:
    if jsonified:
        groups = jsonified["groups"]
    else:
        groups = get_groups(sightings)

    print('✅ - Valid Groups')

    for group in groups:
        validate_group(group, jsonified, sightings)
except (KeyError, AttributeError):
    print('❎ - Valid Groups')
