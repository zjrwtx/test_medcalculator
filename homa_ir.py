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
- rewrite function compute_homa_ir_explanation
- translation

Date: March 2025
"""

from camel.toolkits.medcalc_bench.utils.rounding import round_number
from camel.toolkits.medcalc_bench.utils.unit_converter_new import (
    conversion_explanation,
)


def compute_homa_ir_explanation(input_variables):
    r"""
    Calculates the patient's Homeostatic Model Assessment for Insulin
    Resistance and generates a detailed explanatory text.

    Parameters:
        input_variables (dict): A dictionary containing the following
        key-value pairs:
            - "insulin" (array): The patient's insulin level in the
            format (value, unit).
                - Value (float): The value of insulin level.
                - Unit (str): The unit of insulin level, eg. "µIU/mL",
                "pmol/L", and so on.
            - "glucose" (array): The patient's blood glucose level in the
            format (value, unit).
                - Value (float): The value of blood glucose level.
                - Unit (str): The unit of blood glucose level,
                eg. "mmol/L", "mEq/L", and so on.

    Returns:
        dict: Contains two key-value pairs:
            - "Explanation" (str): A detailed description of
            the calculation process.
            - "Answer" (float): The patient's Homeostatic Model Assessment
            for Insulin Resistance.

    Notes:
        - None

    Example:
        compute_homa_ir_explanation({'insulin': [756.0, 'pmol/L'],
        'glucose': [97.3, 'mg/dL']})

        output: "{'Explanation': "The formula for computing HOMA-IR score is
        (insulin (µIU/mL) * glucose mg/dL)/405. \nThe concentration of
        glucose is 97.3 mg/dL. \nPlugging into the formula will give us
        756.0 * 97.3/405 = 181.627.
        Hence, the patient's HOMA-IR score is 181.627. \n", 'Answer': 181.627}"
    """

    explanation = (
        "The formula for computing HOMA-IR score is (insulin ("
        "µIU/mL) * glucose mg/dL)/405.\n"
    )

    insulin = input_variables["insulin"][0]

    if input_variables["insulin"][1] == "µIU/mL":
        explanation += f"The concentration of insulin is {insulin} µIU/mL.\n"

    elif input_variables["insulin"][1] == "pmol/L":
        insulin = input_variables["insulin"][0] * 6
        explanation += (
            f"The concentration of insulin is {insulin} pmol/L. "
            f"We to need convert the concentration of insulin to pmol/L, "
            f"by multiplying by the conversion factor of 6.0 µIU/mL/pmol/L. "
            f"This makes the insulin concentration "
            f"{input_variables['insulin'][0]} * 6 µIU/mL/pmol/L = {insulin} "
            f"µIU/mL.\n"
        )

    elif input_variables["insulin"][1] == "ng/mL":
        insulin = input_variables["insulin"][0] * 24.8
        explanation += (
            f"The concentration of insulin is {insulin} ng/mL. "
            f"We to need convert the concentration of insulin to µIU/mL, "
            f"by multiplying by the conversion factor 24.8 µIU/mL/ng/mL. "
            f"This makes the insulin concentration "
            f"{input_variables['insulin'][0]} * 24.8 µIU/mL/ng/mL = "
            f"{insulin} ng/mL.\n"
        )

    glucose_exp, glucose = conversion_explanation(
        input_variables["glucose"][0],
        "glucose",
        180.16,
        None,
        input_variables["glucose"][1],
        "mg/dL",
    )

    explanation += glucose_exp + "\n"

    answer = round_number((insulin * glucose) / 405)

    explanation += (
        f"Plugging into the formula will give us "
        f"{insulin} * {glucose}/405 = {answer}. "
        f"Hence, the patient's HOMA-IR score is {answer}. \n"
    )

    return {"Explanation": explanation, "Answer": answer}


if __name__ == "__main__":
    # Defining test cases
    test_cases = [{'insulin': [756.0, 'pmol/dL'], 'glucose': [97.3, 'mg/dL']}]

    # Iterate the test cases and print the results
    for i, input_variables in enumerate(test_cases, 1):
        print(f"Test Case {i}: Input = {input_variables}")
        result = compute_homa_ir_explanation(input_variables)
        print(result)
        print("-" * 50)
