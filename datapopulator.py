import json

import ijson
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

database = client["pill_dispenser"]

medicine_collection = database["medicines"]


amount_of_medicines_added = 0
for i in range(1, 9):
    with open('drug-label-000{0}-of-0008.json'.format(i)) as json_file:
        print('Reading ', 'drug-label-000{0}-of-0008.json'.format(i))
        objects = ijson.items(json_file, 'results.item')

        for drug in objects:
            openfda_info = drug.get('openfda')

            if openfda_info is None:
                continue;

            product_type = openfda_info.get('product_type')

            if product_type is None:
                continue;

            if 'HUMAN OTC DRUG' not in product_type and 'HUMAN PRESCRIPTION DRUG' not in product_type:
                continue

            medicine_result = {
                'product_type': product_type
            }

            other_open_fda_keys = ['route', 'brand_name', 'generic_name']
            for fda_key in other_open_fda_keys:
                info = openfda_info.get(fda_key)
                if not info:
                    continue
                medicine_result[fda_key] = info

            additional_keys = ['drug_interactions', 'precautions', 'dosage_and_administration_table', 'warnings', 'purpose',
                               'drug_interactions_table']

            for k in additional_keys:
                info = drug.get(k)
                if not info:
                    continue
                medicine_result[k] = info

            medicine_collection.insert_one(medicine_result)
            amount_of_medicines_added += 1


print("Added {0} medicines".format(amount_of_medicines_added))
