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
- rewrite function compute_wells_criteria_dvt_explanation
- translation

Date: March 2025
"""


def compute_wells_criteria_dvt_explanation(input_parameters):
    r"""
    Calculates the patient's score of Wells' criteria for DVT and generates
    a detailed explanatory text.

    Parameters:
        input_parameters (dict): A dictionary containing the following
        key-value pairs:
            - "active_cancer" (boolean): Whether the patient has active
            cancer or not.
            - "bedridden_for_atleast_3_days" (boolean): bedridden recently
            >3 days.
            - "major_surgery_in_last_12_weeks" (boolean): major surgery
            within 12 weeks.
            - "calf_swelling_3cm" (boolean): calf swelling >3 cm compared
            to the other leg.
            - "collateral_superficial_veins" (boolean): collateral (
            nonvaricose) superficial veins present.
            - "leg_swollen" (boolean): entire leg swollen.
            - "localized_tenderness_on_deep_venuous_system" (boolean):
            localized tenderness along the deep venous
            system.
            - "pitting_edema_on_symptomatic_leg" (boolean): pitting edema,
            confined to symptomatic leg.
            - "paralysis_paresis_immobilization_in_lower_extreme" (boolean):
            paralysis, paresis, or recent plaster
            immobilization of the lower extremity
            - "previous_dvt" (boolean): Previous, objectively diagnosed DVT:
            No = 0 points, Yes = +1.5 points.
            - "alternative_to_dvt_diagnosis" (boolean): alternative
            diagnosis to DVT as likely or more likely.

    Returns:
        dict: Contains two key-value pairs:
            - "Explanation" (str): A detailed description of
            the calculation process.
            - "Answer" (float): The patient's score of Wells' criteria for
            Pulmonary Embolism.

    Notes:
        - None.

    Example:
        calculate_pe_wells_explanation({
            "active_cancer": False,
            "bedridden_for_atleast_3_days": False,
            "major_surgery_in_last_12_weeks": False,
            "calf_swelling_3cm": False,
            "collateral_superficial_veins": True,
            "leg_swollen": False,
            "localized_tenderness_on_deep_venuous_system": False,
            "pitting_edema_on_symptomatic_leg": False,
            "paralysis_paresis_immobilization_in_lower_extreme": False,
            "previous_dvt": True,
            "alternative_to_dvt_diagnosis": False,
        })

        output: "{'Explanation': "\n    The criteria for the Wells' Criteria
        for Deep Vein Thrombosis (DVT) score are listed below:\n\n
        1. Active cancer (treatment or palliation within 6 months):
        No = 0 points, Yes = +1 point\n       2. Bedridden recently >3 days
        or major surgery within 12 weeks: No = 0 points, Yes = +1 point
        \n       3. Calf swelling >3 cm compared to the other leg (measured
        10 cm below tibial tuberosity): No = 0 points, Yes = +1 point
        \n       4. Collateral (nonvaricose) superficial veins present:
        No = 0 points, Yes = +1 point\n       5. Entire leg swollen:
        No = 0 points, Yes = +1 point\n 6. Localized tenderness along the
        deep venous system: No = 0 points, Yes = +1 point\n 7. Pitting
        edema, confined to symptomatic leg: No = 0 points, Yes = +1 point
        \n 8. Paralysis, paresis, or recent plaster immobilization of the
        lower extremity: No = 0 points, Yes = +1 point\n
        9. Previously documented DVT: No = 0 points, Yes = +1 point\n 10.
        Alternative diagnosis to DVT as likely or more likely: No = 0
        points, Yes = -2 points\n \n    The total score is calculated by
        summing the points for each criterion.\\n\\n\n The current Well's
        DVT Score is 0.\nFrom the patient's note, the issue, 'active cancer,
        ' is absent. By the Well's DVT rule, a point should not be given,
        and so the score remains unchanged and so total remains at 0.\nFrom
        the patient's note, the issue, 'bedridden recently >3 days,
        ' is absent. From the patient's note, the issue, 'major surgery
        within 12 weeks,' is absent. Based on the Well's DVT rule, at least
        one of the issues, 'bedridden recently >3 days' or 'major surgery
        within 12 weeks' must be true for this criteria to be met for the
        score to increase by 1. This is not the case for this patient,
        and so the score remains unchanged at 0.\nFrom the patient's note,
        the issue, 'calf swelling >3 cm compared to the other leg,'
        is absent. By the Well's DVT rule, a point should not be given,
        and so the score remains unchanged and so total remains at 0.\nFrom
        the patient's note, the issue, 'collateral (nonvaricose)
        superficial veins present,' is present. By Well's DVT rule, a point
        should be given, and so we increment the score by one, making
        the total 0 + 1 =  1.\nFrom the patient's note, the issue, 'entire
        leg swollen,' is absent. By the Well's DVT rule, a point should not
        be given, and so the score remains unchanged and so total remains
        at 1.\nFrom the patient's note, the issue, 'localized tenderness
        along the deep venous system,' is absent. By the Well's DVT rule,
        a point should not be given, and so the score remains unchanged and
        so total remains at 1. \nFrom the patient's note, the issue,
        'pitting edema, confined to symptomatic leg,' is absent. By the
        Well's DVT rule, a point should not be given, and so the score
        remains unchanged and so total remains at 1.\nFrom the patient's
        note, the issue, 'paralysis, paresis, or recent plaster
        immobilization of the lower extremity,' is absent. By the Well's
        DVT rule, a point should not be given, and so the score remains
        unchanged and so total remains at 1.\nFrom the patient's note,
        the issue, 'previously documented DVT,' is present. By Well's DVT
        rule, a point should be given, and so we increment the score by
        one, making the total 1 + 1 =  2.\nFrom the patient's note,
        the issue, 'alternative diagnosis to DVT as likely or more likely,
        ' is absent. By the Well's DVT rule, a point should not be given,
        and so the score remains unchanged and so total remains at 2.\nThe
        Well's DVT score for the patient is 2.\n", 'Answer': 2}"
    """

    # List of parameters and their default values
    parameters = [
        ('active_cancer', "active cancer"),
        ('bedridden_for_atleast_3_days', "bedridden recently >3 days"),
        ('major_surgery_in_last_12_weeks', "major surgery within 12 weeks"),
        ('calf_swelling_3cm', "calf swelling >3 cm compared to the other leg"),
        (
            'collateral_superficial_veins',
            "collateral (nonvaricose) superficial veins present",
        ),
        ('leg_swollen', "entire leg swollen"),
        (
            'localized_tenderness_on_deep_venuous_system',
            "localized tenderness along the deep venous system",
        ),
        (
            'pitting_edema_on_symptomatic_leg',
            "pitting edema, confined to symptomatic leg",
        ),
        (
            'paralysis_paresis_immobilization_in_lower_extreme',
            "paralysis, paresis, or "
            "recent plaster immobilization of the lower extremity",
        ),
        ('previous_dvt', 'previously documented DVT'),
        (
            'alternative_to_dvt_diagnosis',
            "alternative diagnosis to DVT as likely or more likely",
        ),
    ]

    output = r"""
    The criteria for the Wells' Criteria for Deep Vein Thrombosis (DVT)
        score are listed below:

       1. Active cancer (treatment or palliation within 6 months): No = 0
        points, Yes = +1 point
       2. Bedridden recently >3 days or major surgery within 12 weeks: No = 0
        points, Yes = +1 point
       3. Calf swelling >3 cm compared to the other leg (measured 10 cm below
        tibial tuberosity): No = 0 points, Yes = +1 point
       4. Collateral (nonvaricose) superficial veins present: No = 0 points,
        Yes = +1 point
       5. Entire leg swollen: No = 0 points, Yes = +1 point
       6. Localized tenderness along the deep venous system: No = 0 points,
        Yes = +1 point
       7. Pitting edema, confined to symptomatic leg: No = 0 points,
        Yes = +1 point
       8. Paralysis, paresis, or recent plaster immobilization of
        the lower extremity: No = 0 points, Yes = +1 point
       9. Previously documented DVT: No = 0 points, Yes = +1 point
       10. Alternative diagnosis to DVT as likely or more likely:
        No = 0 points, Yes = -2 points

    The total score is calculated by summing the points for each criterion.\n\n
    """

    # Initializing points and output explanation
    score = 0
    output += "The current Well's DVT Score is 0.\n"

    count = 0

    while count < len(parameters):
        param_name = parameters[count][0]

        param_value = input_parameters.get(param_name)

        # If parameter is missing, assume it as False
        if param_value is None:
            output += (
                f"The issue,'{parameters[count][1]},' is missing from the "
                f"patient note and so the value is assumed "
                f"to be absent from the patient. "
            )
            input_parameters[param_name] = False
            param_value = False

        else:
            param_value_name = 'absent' if not param_value else 'present'
            output += (
                f"From the patient's note, the issue, '"
                f"{parameters[count][1]},' is {param_value_name}. "
            )

        if param_name == 'bedridden_for_atleast_3_days':
            count += 1
            continue
        if param_name == 'major_surgery_in_last_12_weeks':
            if (
                input_parameters['bedridden_for_atleast_3_days']
                or input_parameters['major_surgery_in_last_12_weeks']
            ):
                output += (
                    f"Based on the Well's DVT rule, at least one of the "
                    f"issues, 'bedridden recently >3 days' or "
                    f"'major surgery within 12 weeks' must be true for this "
                    f"criteria to be met for the score to increase by 1. "
                    f"Because this is the case, we incease the score by "
                    f"one making the total {score} + 1 = {score + 1}.\n"
                )
                score += 1
            else:
                output += (
                    f"Based on the Well's DVT rule, at least one of the "
                    f"issues, 'bedridden recently >3 days' or "
                    f"'major surgery within 12 weeks' must be true for this "
                    f"criteria to be met for the score "
                    f"to increase by 1. This is not the case for this "
                    f"patient, and so the score remains unchanged at "
                    f"{score}.\n"
                )
            count += 1
            continue

        # Score calculation
        if param_value:
            if param_name == 'alternative_to_dvt_diagnosis':
                output += (
                    f"By the Well's DVT rule, we decrease the score "
                    f"by 2 and so total is {score} - 2 = {score - 2}.\n"
                )
                score -= 2
                count += 1
                continue
            else:
                output += (
                    f"By Well's DVT rule, a point should be given, "
                    f"and so we increment the score by one, "
                    f"making the total {score} + 1 =  {score + 1}.\n"
                )
                score += 1
        elif param_value is False:
            output += (
                f"By the Well's DVT rule, a point should not be given, "
                f"and so the score remains unchanged "
                f"and so total remains at {score}.\n"
            )

        count += 1

    output += f"The Well's DVT score for the patient is {score}.\n"

    return {"Explanation": output, "Answer": score}


if __name__ == "__main__":
    # Defining test cases
    test_cases = [
        {
            "active_cancer": False,
            "bedridden_for_atleast_3_days": False,
            "major_surgery_in_last_12_weeks": False,
            "calf_swelling_3cm": False,
            "collateral_superficial_veins": True,
            "leg_swollen": False,
            "localized_tenderness_on_deep_venuous_system": False,
            "pitting_edema_on_symptomatic_leg": False,
            "paralysis_paresis_immobilization_in_lower_extreme": False,
            "previous_dvt": True,
            "alternative_to_dvt_diagnosis": False,
        },
    ]

    # Iterate the test cases and print the results
    for i, input_variables in enumerate(test_cases, 1):
        print(f"Test Case {i}: Input = {input_variables}")
        result = compute_wells_criteria_dvt_explanation(input_variables)
        print(result)
        print("-" * 50)
