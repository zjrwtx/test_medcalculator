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
- rewrite function free_water_deficit_explanation
- translation

Date: March 2025
"""

from camel.toolkits.medcalc_bench.utils.age_conversion import (
    age_conversion_explanation,
)
from camel.toolkits.medcalc_bench.utils.rounding import round_number
from camel.toolkits.medcalc_bench.utils.unit_converter_new import (
    conversion_explanation,
)
from camel.toolkits.medcalc_bench.utils.weight_conversion import (
    weight_conversion_explanation,
)


def free_water_deficit_explanation(input_variables):
    r"""
    Calculates the patient's LDL cholestrol concentration and generates a
    detailed explanatory text.

    Parameters:
        input_variables (dict): A dictionary containing the following
        key-value pairs:
            - "sex" (str): The patient's gender, which can be either "Male"
            or "Female".
            - "age" (array): The patient's albumin concentration in the
            format (value, unit).
                - Value (float): Age.
                - Unit (str): The unit can be "months", "years".
            - "weight" (tuple): The patient's weight information in the
            format (value, unit).
                - Value (float): The numerical weight measurement.
                - Unit (str): The unit of weight, which can be "lbs" (
                pounds), "g" (grams), or "kg" (kilograms).
            - "sodium" (array): The patient's bicarbonate level in the
            format (value, unit).
                - Value (float): The value of bicarbonate level.
                - Unit (str): The unit of bicarbonate level, eg. "mmol/L",
                "mEq/L", and so on.

    Returns:
        dict: Contains two key-value pairs:
            - "Explanation" (str): A detailed description of
            the calculation process.
            - "Answer" (float): The patient's LDL cholestrol concentration.

    Notes:
        - None

    Example:
        free_water_deficit_explanation({'sex': 'Female',
        'age': [17, 'years'],
        'weight': [63.0, 'kg'],
        'sodium': [141.0, 'mEq/L']})

        output: "{'Explanation': "The formula for computing the free water
        deficit is (total body water percentage) * (weight) * (sodium/140 -
        1), where the total body water percentage is a percentage expressed
        as a decimal, weight is in kg, and the sodium concentration is in
        mmol/L.\nThe patient's total body weight percentage is based on the
        patient's age and gender.\nThe patient is 17 years old. The
        patient's is a Female.\nThe patient is less than 18 years old and
        so the patient is a child. This means total body water percentage
        value is 0.6.\nThe patient's weight is 63.0 kg. The concentration
        of sodium is 141.0 mEq/L. We need to convert the concentration to
        mmol/L. Let's first convert the mass of sodium from mEq to mmol.
        The mass of sodium is 141.0 mEq. To convert from 141.0 mEq to mmol,
        convert from mEq to mmol. The compound 141.0 has a valence of 1,
        and so divide the valence by the value of mEq to get, 141.0 mEq/(1
        mEq/mmol) = 141.0 mmol sodium. The volume units is L so no volume
        conversion is needed. Hence, the concentration value of 141.0 mEq
        sodium/L converts to 141.0 mmol sodium/L. Plugging in these values
        into the equation, we get 0.6 * 63.0 * (141.0/140 - 1) = 0.27 L.
        The patient's free body water deficit is 0.27 L.\n",
        'Answer': 0.27}"
    """

    explanation = ""

    explanation += (
        "The formula for computing the free water deficit is "
        "(total body water percentage) * (weight) * (sodium/140 - 1), "
        "where the total body water percentage is a percentage expressed as "
        "a decimal, weight is in kg, and the sodium concentration is in "
        "mmol/L.\n"
    )

    age_exp, age = age_conversion_explanation(input_variables["age"])
    gender = input_variables["sex"]

    explanation += (
        "The patient's total body weight percentage is based on "
        "the patient's age and gender.\n"
    )
    explanation += age_exp
    explanation += f"The patient's is a {gender}.\n"

    if 0 <= age < 18:
        tbw = 0.6
        explanation += (
            "The patient is less than 18 years old and so the patient is a "
            "child. This means total body water percentage value is 0.6.\n"
        )
    elif 18 <= age < 65 and gender == "Male":
        tbw = 0.6
        explanation += (
            "The patient's age is between 18 and 64 and "
            "so the patient is an adult. For adult male's the total body "
            "water percentage value is 0.60.\n"
        )
    elif 18 <= age < 65 and gender == "Female":
        tbw = 0.5
        explanation += (
            "The patient's age is between 18 and 64 and "
            "so the patient is an adult. For adult female's the total body "
            "water percentage value is 0.50.\n"
        )
    elif age >= 65 and gender == "Male":
        tbw = 0.5
        explanation += (
            "The patient's age is greater than 64 years and so the patient "
            "is considered elderly. For elderly male's, "
            "the total body water percentage value is 0.50.\n"
        )
    elif age >= 65 and gender == "Female":
        tbw = 0.45
        explanation += (
            "The patient's age is greater than 64 years and so the patient "
            "is considered elderly. For elderly female's, the total body "
            "water percentage value is 0.45.\n"
        )

    weight_exp, weight = weight_conversion_explanation(
        input_variables["weight"]
    )
    explanation += weight_exp

    sodium_exp, sodium = conversion_explanation(
        input_variables["sodium"][0],
        "sodium",
        22.99,
        1,
        input_variables["sodium"][1],
        "mmol/L",
    )
    explanation += sodium_exp

    answer = round_number(tbw * weight * (sodium / 140 - 1))

    explanation += (
        f"Plugging in these values into the equation, "
        f"we get {tbw} * {weight} * ({sodium}/140 - 1) = {answer} L. "
    )
    explanation += f"The patient's free body water deficit is {answer} L.\n"

    return {"Explanation": explanation, "Answer": answer}


if __name__ == "__main__":
    # Defining test cases
    test_cases = [
        {
            'sex': 'Female',
            'age': [32, 'years'],
            'weight': [33.0, 'lbs'],
            'sodium': [134.0, 'mmol/L'],
        },
        {
            'sex': 'Female',
            'age': [17, 'years'],
            'weight': [63.0, 'kg'],
            'sodium': [141.0, 'mEq/L'],
        },
    ]

    # Iterate the test cases and print the results
    for i, input_variables in enumerate(test_cases, 1):
        print(f"Test Case {i}: Input = {input_variables}")
        result = free_water_deficit_explanation(input_variables)
        print(result)
        print("-" * 50)
