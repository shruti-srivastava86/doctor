import json
import csv

from django.conf import settings

from doctor.surrounding import enums

get_for_assessment = {
    "Weight": enums.WEIGHT,
    "Eating/Hydration": enums.FOOD_AND_HYDRATION,
    "Movement": enums.MOTION,
    "Sleep": enums.SLEEP,
    "Mind": enums.MIND
}


def load_surrounding_csv_data():
    file = settings.BASE_DIR + '/doctor/management/commands/surrounding_csv_data.csv'
    output_file = settings.BASE_DIR + '/doctor/management/commands/surrounding_initial_data.py'
    with open(file, 'r', encoding='utf-8') as csv_file:
        surrounding_data = csv.DictReader(csv_file, delimiter=',')
        surrounding_list = list()
        for row in surrounding_data:
            surrounding_dict = dict()
            surrounding_dict["start_range"] = int(row["Day for notification"])
            surrounding_dict["end_range"] = int(row["Day for notification"])
            surrounding_dict["required_completions"] = 1
            surrounding_dict["challenge"] = row["Tasks"]
            surrounding_dict["stage"] = 1
            surrounding_dict["for_assessment"] = get_for_assessment[
                row["Macro category"]
            ]
            surrounding_list.append(surrounding_dict)
        write_dictionary_to_json(
            output_file,
            surrounding_list
        )


def write_dictionary_to_json(file_name, dictionary):
    with open(file_name, 'w') as fp:
        fp.write("surrounding_initial_data = ")
        json.dump(dictionary, fp)
