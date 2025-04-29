import re


def generate_combinations(condition_str):
    if ' or ' not in condition_str:
        return [condition_str.strip()]

    # Split only at the first 'or' (assuming only one 'or' max)
    parts = condition_str.split(' or ')

    # Find where the 'or' was to isolate left and right expressions
    left_parts = parts[0].strip()
    right_parts = parts[1].strip()

    # Look for the last 'and' before 'or' and first 'and' after
    # So we can group the non-OR conditions separately
    left_segments = left_parts.split(' and ')
    right_segments = right_parts.split(' and ')

    # Identify the condition to split on OR
    left_or_part = left_segments[-1]
    right_or_part = right_segments[0]

    # Get the common parts before and after
    left_common = ' and '.join(left_segments[:-1]).strip()
    right_common = ' and '.join(right_segments[1:]).strip()

    results = []

    if left_common:
        results.append(f"{left_common} and {left_or_part} and {right_common}".strip(' and '))
        results.append(f"{left_common} and {right_or_part} and {right_common}".strip(' and '))
    else:
        results.append(f"{left_or_part} and {right_common}".strip(' and '))
        results.append(f"{right_or_part} and {right_common}".strip(' and '))

    return results


def extract_xpath_conditions_with_logical_operators(xpath):
    # Define the regex patterns for normal XPath conditions and contains conditions
    normal_pattern = r"@([a-zA-Z0-9_-]+)\s*=\s*['\"]([^'\"]+)['\"]"  # Handle both single and double quotes
    contains_pattern = r"contains\(\s*@([a-zA-Z0-9_-]+)\s*,\s*['\"]([^'\"]+)['\"]\s*\)"

    # List to hold extracted conditions
    extracted_info = []

    # Initialize the last operator
    last_operator = None

    # Clean the input XPath (remove extra spaces around operators)
    xpath = xpath.strip()

    # This pattern captures all conditions (with or without logical operators like 'and' or 'or')
    condition_operator_pattern = r"(contains\([^\)]+\)|@[\w-]+\s*=\s*['\"].*?['\"])|(\s*(and|or)\s*)"

    # Process the entire XPath expression
    matches = re.finditer(condition_operator_pattern, xpath)

    # Iterate over all the matches
    for match in matches:
        condition = match.group(1)  # Extract the condition part
        operator = match.group(3)

        # If we have a logical operator, update the last_operator
        if operator:
            last_operator = operator.strip()

        # Ensure the condition is valid before processing
        if condition:
            # Check for a normal condition (e.g., @class='button' or @class="button")
            normal_match = re.match(normal_pattern, condition)
            if normal_match:
                identifier = normal_match.group(1)
                value = normal_match.group(2)
                extracted_info.append({
                    'identifier': identifier,
                    'value': value,
                    'contains': False,
                    'operator': last_operator  # Attach the last operator before this condition
                })
                last_operator = None  # Reset after processing a normal condition

            # Check for a contains() condition (handles both single and double quotes)
            contains_match = re.match(contains_pattern, condition)
            if contains_match:
                identifier = contains_match.group(1)
                value = contains_match.group(2)
                extracted_info.append({
                    'identifier': identifier,
                    'value': value,
                    'contains': True,
                    'operator': last_operator  # Attach the last operator before this condition
                })
                last_operator = None  # Reset after processing a contains condition

    return extracted_info


def generate_chained_tags_calls(matches):
    if not matches:
        return ''

    # Start the method chain with the first match
    result = f'(clazz=\"{matches[0]}\")'

    # Add the child method chain for each subsequent match
    for match in matches[1:]:
        result += f'.child(clazz=\"{match}\")'

    return result


def generate_condition_method_calls(matches):
    identifiers = {'class': 'clazz', 'resource-id': 'resourceId', 'type': 'clazz', 'content-desc': 'desc',
                   'text': 'text'}
    identifiers_inside_contains = {'class': 'clazzMatches', 'resource-id': 'resMatches', 'type': 'clazzMatches',
                                   'content-desc': 'descContains', 'text': 'textContains'}

    current_conditions = []

    for condition in matches:
        # Add the condition to the current list, whether it's a simple condition or contains condition
        if condition['contains']:
            if identifiers_inside_contains[condition['identifier']] in ['content-desc', 'text']:
                current_conditions.append(
                    f'{identifiers_inside_contains[condition["identifier"]]}=\"{condition["value"]}\"')
            else:
                current_conditions.append(
                    f'{identifiers_inside_contains[condition["identifier"]]}=".*{re.escape(condition["value"])}$"')
        else:
            current_conditions.append(f'{identifiers[condition["identifier"]]}=\"{condition["value"]}\"')

    # Generate the final device.ui() call as a single string
    return f"({', '.join(current_conditions)})"


def xpath_converter(original_xpath):
    converted_mobly_xpath = []
    index = None
    index_pattern = r'\[(\d+)\]$'
    match = re.search(index_pattern, original_xpath)

    # Extract index if it's present in the XPath
    if match:
        index = match.group(1)
        xpath = re.sub(index_pattern, '', original_xpath)
        if xpath.startswith('(') and xpath.endswith(')'):
            # Remove the first and last characters (i.e., '(' and ')')
            xpath = xpath[1:-1]
    else:
        xpath = original_xpath

    print(f"XPath without index: {xpath}")
    print(f"Index: {index}")

    # First, capture the condition (inside [])
    condition_pattern = r'\[(.*?)\]$'

    condition_match = re.search(condition_pattern, xpath)
    condition = None
    if condition_match:
        condition = condition_match.group(1)  # Capture the condition inside []
        tags_wildcards = xpath.replace('[' + condition + ']', '')
    else:
        tags_wildcards = xpath

    print("Tags/Wildcards:", tags_wildcards)

    print(f"Condition: {condition}")
    if re.search(r'[a-zA-Z]', tags_wildcards.replace('//', '')):  # If there are alphabets, it's likely a tag
        if re.search(r'[^a-zA-Z.]', tags_wildcards.replace('//', '')):  # If anything else (like *, etc.), it's a
            # combination of tag and wildcard
            print("Tags/Wildcards: Combination of tags and wildcards")
        else:
            print("Tags/Wildcards: Tags only")
            # Split the string by the '//' delimiter, ignoring empty strings
            components = tags_wildcards.split('//')

            # Use a regular expression to match valid tags
            pattern = r'\S+\.\S+\.[A-Za-z]+'

            # Apply the regex pattern to filter and extract valid tags
            matches = [component for component in components if re.match(pattern, component)]

            print('separated tags', matches)
            print(generate_chained_tags_calls(matches))
            tags_mobly_xpath = generate_chained_tags_calls(matches)
            if condition:
                all_conditions_combinations = generate_combinations(condition)
                for combination in all_conditions_combinations:
                    extracted_conditions = extract_xpath_conditions_with_logical_operators(combination)
                    print(generate_condition_method_calls(extracted_conditions))
                    if index:
                        final_mobly_xpath = f"{tags_mobly_xpath}.child{generate_condition_method_calls(extracted_conditions)[:-1]}, index={index})"
                    else:
                        final_mobly_xpath = f"{tags_mobly_xpath}.child{generate_condition_method_calls(extracted_conditions)}"
                    converted_mobly_xpath.append(final_mobly_xpath)
            else:
                if index:
                    tags_mobly_xpath = tags_mobly_xpath[:-1] + f', index={index})'
                    converted_mobly_xpath.append(tags_mobly_xpath)
                else:
                    converted_mobly_xpath.append(tags_mobly_xpath)
            print(converted_mobly_xpath)
            return converted_mobly_xpath
    else:
        print("Tags/Wildcards: Wildcard only")


"""# print('\n\nRemember to include these afterward also. For now keeping it simple. Still I don't think it will be 
necessary until we switch to webview in mobile application then we will have to deal with div and such') # 
xpath_value = "//div[@id='header']" # x_path_maker(xpath_value)

"""
