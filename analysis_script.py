import csv
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import json
import diagrams


FILE_PATH_1 = 'data/secound_run_bamk_150.csv'
FILE_PATH_2 = 'data/secound_run_alkl_150.csv'
FILE_PATH_COMMENTS = 'data/merged.json'
ANONYMIZE = False


def gen_dict(file_path):
    with open(file_path, mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file, delimiter=';')
        categories = {key: [] for key in reader.fieldnames}
        for row in reader:
            for key in categories:
                if row[key]:
                    categories[key].append(row[key])
    return categories

def gen_diagram_comment_owner(dict_id_sub, N):
    sub_dict = replace_id_with_owner(dict_id_sub)
    dict_id_main = merge_sub_categories(dict_id_sub)
    main_dict = replace_id_with_owner(dict_id_main)

    for k, v in sub_dict.items():
        sub_dict[k] = {arr[0]: arr for arr in split_into_subarrays(v)}
    diagrams.stacked_bar_chart(sub_dict,f"Sub-Categories Induvedual Reviwers - {N} Comments")
 
def split_into_subarrays(arr):
    groups = {}
    for item in arr:
        groups.setdefault(item, []).append(item)
    return list(groups.values())

def distribution_comments_category_per_reviewer(dict_id_sub, N):
    sub_dict = replace_id_with_owner(dict_id_sub)

    percentage_distribution = {category: {} for category in dict_id_sub}
    for category, comments in dict_id_sub.items():
        category_total = len(comments)
        if category_total > 0:
            for reviewer in comments:
                if reviewer in percentage_distribution[category]:
                    percentage_distribution[category][reviewer] += (1 / category_total) * 100
                else:
                    percentage_distribution[category][reviewer] = (1 / category_total) * 100

    diagrams.distribution_comments_category_per_reviewer(percentage_distribution, f"Distribution of Comments in Each Category pr. Reviewer - {N} Comments")

def noprocent_distribution_comments_category_per_reviewer(dict_id_sub, N):
    sub_dict = replace_id_with_owner(dict_id_sub)
    # Initialize a dictionary to store the absolute distribution
    absolute_distribution = {category: {} for category in dict_id_sub}

    # Calculate the distribution
    for category, comments in dict_id_sub.items():
        for reviewer in comments:
            if reviewer in absolute_distribution[category]:
                absolute_distribution[category][reviewer] += 1
            else:
                absolute_distribution[category][reviewer] = 1

    diagrams.noprocent_distribution_comments_category_per_reviewer(absolute_distribution, f"TEST of Comments in Each Category pr. Reviewer - {N} Comments")

#distribution of comments in each category per reviewer

def replace_id_with_owner(dict):

    with open(FILE_PATH_COMMENTS, "r", encoding="utf-8-sig") as json_file:
        data = json.load(json_file)

    id_to_display_name = {}
    for entry in data:
        for comment in data[entry]["comment_list"]:
            user_info = comment.get("user", {})
            display_name = ''.join(word[0] for word in user_info.get("display_name").split())
            comment_id = comment.get("id")
            if display_name and comment_id:
                id_to_display_name[str(comment_id)] = display_name

    for key in dict:
        dict[key] = [id_to_display_name.get(str(item), item) for item in dict[key]]

    if ANONYMIZE:
        unique = {}
        for k, v in dict.items():
            for item in v:
                unique[item] = ""
        
        for index, (key, value) in enumerate(unique.items()):
            unique[key] = f"R_{index}"

        for key, value in dict.items():
            for i in range(len(value)):
                value[i] = unique[value[i]]
    
    return dict


def percentage_contributions(dict_id_sub):
    sub_dict = replace_id_with_owner(dict_id_sub)
    sub_precentage = _calculate_percentage_contributions(sub_dict)

    dict_id_main = merge_sub_categories(dict_id_sub)
    main_dict = replace_id_with_owner(dict_id_main)
    main_precentage = _calculate_percentage_contributions(main_dict)
    return main_precentage, sub_precentage


def _calculate_percentage_contributions(dict):
    total_counts = {}
    for category in dict:
        for name in dict[category]:
            total_counts[name] = total_counts.get(name, 0) + 1

    category_percentages = {}
    for category in dict:
        category_percentages[category] = {}
        for name in dict[category]:
            category_count = dict[category].count(name)
            total_count = total_counts[name]
            category_percentages[category][name] = (category_count / total_count) * 100

    return category_percentages

def total_percentage_contributions(dict_id_sub):
    sub_dict = replace_id_with_owner(dict_id_sub)
    precentage = _calculate_total_percentage_contributions(sub_dict)
    return precentage


def _calculate_total_percentage_contributions(dict):
    total_comments = sum(len(comments) for comments in dict.values())
    individual_comments = {}
    for comments in dict.values():
        for name in comments:
            individual_comments[name] = individual_comments.get(name, 0) + 1

    # Calculate the percentage contribution of each individual
    return {name: (count / total_comments) * 100 for name, count in individual_comments.items()}

def common_elements_count(counter1, counter2):
    return counter1 & counter2

def calculate_p_o(dict1, dict2, N):
    observed_agreement = 0
    for key in dict1:
        observed_agreement += sum(common_elements_count(Counter(dict1[key]), Counter(dict2[key])).values())
    return observed_agreement / N

def calculate_p_e(dict1, dict2, N):
    expected_agreement = sum((len(v) / N) * (len(dict2[k]) / N) for k, v in dict1.items())
    return expected_agreement

def calculate_kappa(p_o, p_e):
    return (p_o - p_e) / (1 - p_e)

def agreement_categories(dict1, dict2, N):
    p_o = calculate_p_o(dict1, dict2, N)
    print("p_o", p_o)
    p_e = calculate_p_e(dict1, dict2, N)
    print("p_e", p_e)
    kappa = calculate_kappa(p_o, p_e)
    print("kappa", kappa)

def merge_sub_categories(input_dict):
    merged_dict = {}
    for key in input_dict:
        first_letter = key[0]
        if first_letter in merged_dict:
            merged_dict[first_letter].extend(input_dict[key])
        else:
            merged_dict[first_letter] = input_dict[key].copy()
    return merged_dict

def comments_count(dict):
    total = 0
    for key in dict:
        total += len(dict[key])
    return total

def kappa_value(dict1_sub, dict2_sub, N, dict1_main, dict2_main):
    print("Subcategories")
    agreement_categories(dict1_sub, dict2_sub, N)

    print("\nCategories")
    agreement_categories(dict1_main, dict2_main, N)

def categorization_diagram(dict1_sub, dict2_sub, N, dict1_main, dict2_main):
    diagrams.generate_bar_chart(dict1_sub, dict2_sub, f'Sub-Categories Cassification - {N} Comments')
    diagrams.generate_bar_chart(dict1_main, dict2_main, f'Categories Cassification Comparison - {N} Comments')

def gen_data():
    sub_categories_bamk = gen_dict(FILE_PATH_1)
    sub_categories_alkl = gen_dict(FILE_PATH_2)

    N = comments_count(sub_categories_bamk)
    print ("N", N)

    categories_bamk = merge_sub_categories(sub_categories_bamk)
    categories_alkl = merge_sub_categories(sub_categories_alkl)
    return sub_categories_bamk,sub_categories_alkl,N,categories_bamk,categories_alkl


def main():
    # Generate data
    sub_categories_bamk, sub_categories_alkl, N, categories_bamk, categories_alkl = gen_data()

    noprocent_distribution_comments_category_per_reviewer(sub_categories_bamk,N)

    #Diagram for main and sub-categories
    categorization_diagram(sub_categories_bamk, sub_categories_alkl, N, categories_bamk, categories_alkl)

    #Kappa agreement level
    kappa_value(sub_categories_bamk, sub_categories_alkl, N, categories_bamk, categories_alkl)

    # Generate owner diagram
    gen_diagram_comment_owner(sub_categories_alkl, N)

    # Generate procentage diagrams and csv's
    sub_precentage_bamk, main_precentage_bamk = percentage_contributions(sub_categories_bamk)
    diagrams.generate_calculate_percentage_contributions(main_precentage_bamk, f'Categories Percentage Contributions in {N} Comments - bamk')
    diagrams.generate_calculate_percentage_contributions(sub_precentage_bamk, f'Sub-Categories Percentage Contributions in {N} Comments - bamk')

    sub_precentage_alkl, main_precentage_alkl= percentage_contributions(sub_categories_alkl)
    diagrams.generate_calculate_percentage_contributions(main_precentage_alkl,  f'Categories Percentage Contributions in {N} Comments - alkl')
    diagrams.generate_calculate_percentage_contributions(sub_precentage_alkl,  f'Sub-Categories Percentage Contributions in {N} Comments - alkl')

    #Total precentage of contributions
    diagrams.percentage_contributions_pie_chart(total_percentage_contributions(sub_categories_alkl), f'Total Percentage Contributions in {N} Comments')


    

if __name__ == "__main__":
    main()