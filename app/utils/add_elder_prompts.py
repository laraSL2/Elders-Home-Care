ADD_ELDER_TEMPLATE = """
Convert the following elder profile information into a JSON format. Extract all relevant details and organize them into appropriate categories. The JSON structure should be flexible, with keys that accurately represent the information provided. Include all important details from the profile, such as personal information, medical information, social background, and any special notes or conditions.

Elder Profile:
 {elder_details}
 
Resident_ID:
{resident_id}

Resident_Name:
{resident_name}

Instructions:
1. Create a JSON object that encompasses all the information provided in the elder profile.
2. Use meaningful keys that accurately represent each piece of information.
3. Group related information into nested objects where appropriate.
4. Include all details present in the profile, even if they seem minor.
5. For lists of items (e.g., medical risks, history), use arrays in the JSON structure.
6. Ensure that dates, numbers, and boolean values are represented appropriately in the JSON format.
7. If there are any unclear or ambiguous parts in the profile, use your best judgment to represent them in the JSON structure.

Please provide the resulting JSON structure based on the given elder profile, formatted as follows:

```json
{{
     Profile: {{// Your JSON structure here}},
     Resident_ID: //Resident ID,
     Resident_Name://Resident Name
}}
```
"""