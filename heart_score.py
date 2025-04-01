# ========= Copyright 2023-2024 @ CAMEL-AI.org. All Rights Reserved. =========
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ========= Copyright 2023-2024 @ CAMEL-AI.org. All Rights Reserved. =========
r"""
This code is borrowed and modified based on the source code from the
'MedCalc-Bench' repository.
Original repository: https://github.com/ncbi-nlp/MedCalc-Bench

Modifications include:
- rewrite function compute_heart_score_explanation
- translation

Date: March 2025
"""

from camel.toolkits.medcalc_bench.utils.age_conversion import (
    age_conversion_explanation,
)


def compute_heart_score_explanation(input_parameters):
    r"""
    Calculates the patient's heart score and generates a detailed
    explanatory text.

    Parameters:
        input_parameters (dict): A dictionary containing the following
        key-value pairs:
            - "age" (array): The patient's albumin concentration in the
            format (value, unit).
                - Value (float): Age.
                - Unit (str): The unit can be "months", "years".
            - "hypertension" (boolean): The patient's history of hypertension.
            - "history" (str): 'Slightly suspicious', 'Moderately
            suspicious', or 'Highly suspicious'.
            - "diabetes_mellitus" (boolean): The patient's diabetes status.
            - "smoking" (boolean): The patient's history of smoking.
            - "family_with_cvd" (boolean): The patient's parent or sibling
            with Cardiovascular disease before age 65.
            - "atherosclerotic_disease" (boolean): The patient's
            atherosclerotic disease.
            - "initial_troponin" (str): The patient's initial troponin:
            "less than or equal to normal limit",
                "between the normal limit or up to three times the normal
                limit",
                or "greater than three times normal limit".
            - "electrocardiogram" (str): The patient's electrocardiogram
            status: "Normal", "Non-specific repolarization disturbance",
            or "Significant ST deviation".
            - "hypercholesterolemia" (boolean): The patient's
            hypercholesterolemia status.
            - "obesity" (boolean): The patient's obesity (BMI > 30 kg/m²).
            - "risk_factors" (dict): Any above risk factors == True should
            be added in this dictionary.

    Returns:
        dict: Contains two key-value pairs:
            - "Explanation" (str): A detailed description of
            the calculation process.
            - "Answer" (float): The patient's corrected calcium
            concentration (in mg/dL).

    Notes:
        - Uses the `conversion_explanation` function to convert Albumin
        level to standard unit g/dL.
        - Uses the `conversion_explanation` function to convert Calcium
        level to standard unit mg/dL.

    Example:
        test_case = {'age': [60, 'years'],
            'hypertension': False,
            'history': 'Slightly suspicious',
            'diabetes_mellitus': False,
            'smoking': False,
            'family_with_cvd': True,
            'atherosclerotic_disease': False,
            'initial_troponin': 'less than or equal to normal limit',
            'electrocardiogram': 'Normal',
            'hypercholesterolemia': False,
            'obesity': False,
            'risk_factors': {'family_with_cvd'}
         }
        compute_heart_score_explanation(test_case)

        output: "{'Explanation': "\nThe HEART Score for risk stratification
        in patients with chest pain is shown below: \n    \n       1.
        History: Slightly suspicious = 0 points, Moderately suspicious = +1
        point, Highly suspicious = +2 points\n 2. EKG: Normal = 0 points,
        Non-specific repolarization disturbance = +1 point, Significant ST
        deviation = +2 points\n 3. Age: <45 years = 0 points, 45-64 years =
        +1 point, ≥65 years = +2 points\n 4. Risk factors (HTN,
        hypercholesterolemia, DM, obesity (BMI >30 kg/m²), smoking (current
        or cessation within 3 months), positive family history of
        cardiovascular disease before age 65, atherosclerotic disease such
        as prior MI, PCI/CABG, CVA/TIA, or peripheral arterial disease): No
        known risk factors = 0 points, 1-2 risk factors = +1 point, ≥3 risk
        factors or history of atherosclerotic disease = +2 points\n 5.
        Initial troponin level: ≤normal limit = 0 points, 1-3x normal limit
        = +1 point, >3x normal limit = +2 points \n    \n       The total
        score is calculated by summing the points for each criterion.\n\n\n
        The current HEART Score is 0.\nThe value of 'history' in the
        patient's note is determined to be 'Slightly suspicious'. Based on
        the HEART Score criteria, 0 points are added for 'history', keeping
        the current total at 0.\nThe value of 'electrocardiogram' in the
        patient's note is determined to be 'Normal'. Based on the HEART
        Score criteria, 0 points are added for 'electrocardiogram', keeping
        the current total at 0.\nThe patient is 60 years old. The patient's
        age is between 45 and 65 years and so we increment the current
        total by 1, making the current total 0 + 1 = 1.\nThe following risk
        factor(s) are present based on the patient's note: family with cvd.
        The following risk factor(s) are mentioned in the patient's note,
        but these risk factors are noted to be absent from the patient:
        hypertension, hypercholesterolemia, diabetes mellitus, obesity,
        smoking, atherosclerotic disease. Based on the HEART Score risk
        factors criteria, 1 risk factors are present and so 1 point is
        added for the risk factors criteria, making the current total,
        1 + 1 = 2.\nThe value of 'initial troponin' in the patient's
        note is determined to be 'less than or equal to normal limit'.
        Based on the HEART Score criteria, 0 points are added for 'initial
        troponin', keeping the current total at 2.\nBased on the patient's
        data, the HEART Score is 2.\n", 'Answer': 2}"
    """

    explanation = """
       The HEART Score for risk stratification in patients with
       chest pain is shown below:

       1. History: Slightly suspicious = 0 points, Moderately suspicious =
        +1 point, Highly suspicious = +2 points
       2. EKG: Normal = 0 points, Non-specific repolarization disturbance =
        +1 point, Significant ST deviation = +2 points
       3. Age: <45 years = 0 points, 45-64 years = +1 point, ≥65 years =
        +2 points
       4. Risk factors (HTN, hypercholesterolemia, DM, obesity (BMI >30 kg/m²),
        smoking (current or cessation within 3 months), positive family
        history of cardiovascular disease before age 65, atherosclerotic
        disease such as prior MI, PCI/CABG, CVA/TIA, or peripheral arterial
        disease): No known risk factors = 0 points, 1-2 risk factors = +1
        point, ≥3 risk factors or history of atherosclerotic disease = +2
        points
       5. Initial troponin level: ≤normal limit = 0 points, 1~3x normal limit
        = +1 point, >3x normal limit = +2 points

       The total score is calculated by summing the points for each criterion.
    """

    # Define parameters and their default values
    parameters = {
        'history': {
            'Slightly suspicious': 0,
            'Moderately suspicious': 1,
            'Highly suspicious': 2,
        },
        'electrocardiogram': {
            'Normal': 0,
            'Non-specific repolarization disturbance': 1,
            'Significant ST deviation': 2,
        },
        'age': {'< 45': 0, '45 - 65': 1, '> 65': 2},
        'risk_factors': {
            'hypertension': 1,
            'hypercholesterolemia': 1,
            'diabetes_mellitus': 1,
            'obesity': 1,
            'smoking': 1,
            'family_with_cvd': 1,
            'atherosclerotic_disease': 1,
        },
        'initial_troponin': {
            'less than or equal to normal limit': 0,
            'between the normal limit or up to '
            'three times the normal limit': 1,
            'greater than three times normal limit': 2,
        },
    }

    factor_name = {
        'hypertension': 'hypertension',
        'hypercholesterolemia': 'hypercholesterolemia',
        'diabetes_mellitus': 'diabetes mellitus',
        'obesity': 'obesity',
        'smoking': 'smoking',
        'family_with_cvd': "family with cvd",
        'atherosclerotic_disease': "atherosclerotic disease",
        'initial_tropopin': 'initial tropopin',
    }

    default_value = {
        'history': 'Slightly suspicious',
        'electrocardiogram': 'Normal',
        'initial_troponin': 'less than or equal to normal limit',
    }

    # Initialize total score and output explanation
    total_score = 0
    explanation += "The current HEART Score is 0.\n"

    for param, options in parameters.items():
        param_value = input_parameters.get(param)

        if param == 'risk_factors':
            present_factors = [
                factor
                for factor in options.keys()
                if input_parameters.get(factor)
            ]
            present_factors_names = [
                factor_name[factor]
                for factor in options.keys()
                if input_parameters.get(factor)
            ]

            if present_factors:
                explanation += (
                    f"The following risk factor(s) are present based on the "
                    f"patient's note: "
                    f"{', '.join(present_factors_names)}. "
                )

            present_but_false = [
                factor
                for factor in options.keys()
                if factor in input_parameters and not input_parameters[factor]
            ]
            present_but_false_names = [
                factor_name[factor]
                for factor in options.keys()
                if factor in input_parameters and not input_parameters[factor]
            ]

            if present_but_false:
                explanation += (
                    f"The following risk factor(s) are mentioned in the "
                    f"patient's note, but these risk factors are noted "
                    f"to be absent from the patient: "
                    f"{', '.join(present_but_false_names)}. "
                )
                for item in present_but_false:
                    input_parameters[item] = False

            missing_factors = [
                factor
                for factor in options.keys()
                if factor not in input_parameters
            ]
            missing_factors_names = [
                factor_name[factor]
                for factor in options.keys()
                if factor in input_parameters and not input_parameters[factor]
            ]

            if missing_factors:
                explanation += (
                    f"The following risk factor(s) are missing from the "
                    f"patient's data: {', '.join(missing_factors_names)}. "
                    f"We will assume that these are all absent from the "
                    f"patient. "
                )

            for factor in missing_factors:
                input_parameters[factor] = False

            factors = present_factors + missing_factors + present_but_false

        elif param in ['history', 'electrocardiogram', 'initial_troponin']:
            if param == 'initial_troponin':
                param_name = 'initial troponin'
            else:
                param_name = param

            if param not in input_parameters:
                explanation += (
                    f"'{param_name}' is missing from the patient's data and "
                    f"so we assume it's value is {default_value[param]}."
                )
                input_parameters[param] = default_value[param]
            else:
                explanation += (
                    f"The value of '{param_name}' in the "
                    f"patient's note is determined to be '"
                    f"{param_value}'. "
                )

        elif param == "age":
            age_explanation, age = age_conversion_explanation(
                input_parameters["age"]
            )
            explanation += age_explanation

        # Add points based on parameter value
        if param == 'risk_factors':
            # Compute the number of risk factors
            risk_factors_count = sum(
                1 for factor in factors if input_parameters[factor]
            )
            explanation += (
                f"Based on the HEART Score risk factors criteria, "
                f"{risk_factors_count} risk factors are present and so "
            )

            if risk_factors_count == 0:
                explanation += (
                    f"0 points are added for the risk factors criteria, "
                    f"keeping the current total at {total_score}.\n"
                )
            elif 1 <= risk_factors_count <= 2:
                explanation += (
                    f"1 point is added for the risk factors criteria, "
                    f"making the current total, {total_score} + 1 = "
                    f"{total_score + 1}.\n"
                )
                total_score += 1
            elif (
                risk_factors_count < 3
                and input_parameters['atherosclerotic_disease']
            ):
                explanation += (
                    f"2 points are added for the risk factors criteria as "
                    f"atherosclerotic disease is present,"
                    f" making the current total {total_score} + 2 = "
                    f"{total_score + 2}.\n"
                )
                total_score += 2
            elif risk_factors_count >= 3:
                explanation += (
                    f"2 points are added as 3 or more risk factors are "
                    f"present, making the current total {total_score} + 2 = "
                    f"{total_score + 2}.\n"
                )
                total_score += 2

        elif param == "age":
            if age < 45:
                explanation += (
                    f"The patient's age is less than 45 years "
                    f"and so keep the current total at "
                    f"{total_score}.\n"
                )
            elif 45 <= age < 65:
                explanation += (
                    f"The patient's age is between 45 and 65 years "
                    f"and so we increment the current total by 1, "
                    f"making the current total {total_score} + 1 = "
                    f"{total_score + 1}.\n"
                )
                total_score += 1
            else:
                explanation += (
                    f"The patient's age is greater than 65 years "
                    f"and so we increment the current total by 2, "
                    f"making the current total {total_score} + 2 = "
                    f"{total_score + 2}.\n"
                )
                total_score += 2
        else:
            points = options[input_parameters[param]]

            if param == 'initial_troponin':
                param = 'initial troponin'

            if points == 0:
                explanation += (
                    f"Based on the HEART Score criteria, 0 points are added "
                    f"for '{param}', keeping the current total at "
                    f"{total_score}.\n"
                )
            elif points == 1:
                explanation += (
                    f"Based on the HEART Score criteria, 1 point is added "
                    f"for '{param}', increasing the current total to"
                    f" {total_score} + 1 = {total_score + 1}.\n"
                )
                total_score += 1
            else:
                explanation += (
                    f"Based on the HEART Score criteria, 2 points are added "
                    f"for '{param}', increasing the current total to"
                    f" {total_score} + 2 = {total_score + 2}.\n"
                )
                total_score += 2

    explanation += (
        f"Based on the patient's data, the HEART Score is {total_score}.\n"
    )

    return {"Explanation": explanation, "Answer": total_score}


if __name__ == "__main__":
    # Defining test cases
    test_cases = [
        {
            'age': [25, 'years'],
            'hypertension': False,
            'history': 'Slightly suspicious',
            'electrocardiogram': 'Normal',
            'diabetes_mellitus': False,
            'smoking': False,
            'atherosclerotic_disease': False,
            'hypercholesterolemia': False,
            'obesity': False,
            'family_with_cvd': False,
            'initial_troponin': 'less than or equal to normal limit',
            'risk_factors': {},
        },
        {
            'age': [57, 'years'],
            'history': 'Moderately suspicious',
            'electrocardiogram': 'Normal',
            'hypertension': True,
            'hypercholesterolemia': True,
            'diabetes_mellitus': False,
            'obesity': False,
            'smoking': False,
            'family_with_cvd': False,
            'atherosclerotic_disease': False,
            'initial_troponin': 'less than or equal to normal limit',
            'risk_factors': {'hypertension', 'hypercholesterolemia'},
        },
        {
            'age': [60, 'years'],
            'hypertension': False,
            'history': 'Slightly suspicious',
            'diabetes_mellitus': False,
            'smoking': False,
            'family_with_cvd': True,
            'atherosclerotic_disease': False,
            'initial_troponin': 'less than or equal to normal limit',
            'electrocardiogram': 'Normal',
            'hypercholesterolemia': False,
            'obesity': False,
            'risk_factors': {'family_with_cvd'},
        },
    ]

    # Iterate the test cases and print the results
    for i, input_variables in enumerate(test_cases, 1):
        print(f"Test Case {i}: Input = {input_variables}")
        result = compute_heart_score_explanation(input_variables)
        print(result)
        print("-" * 50)
