import json

def find_value_paths(data, target_value):
    """
    Recursively search a nested JSON-like structure (dicts + lists)
    and return all paths where the value equals `target_value`.

    Returns:
        List of tuples: [(path_string, value), ...]
    """
    results = []

    def _search(obj, path):
        # If this is a dict, iterate through its keys/values
        if isinstance(obj, dict):
            for key, value in obj.items():
                new_path = f"{path}.{key}" if path else key
                # Check for direct value match
                if value == target_value:
                    results.append((new_path, value))
                # Recurse
                _search(value, new_path)

        # If this is a list, iterate through elements
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                new_path = f"{path}[{i}]"
                if item == target_value:
                    results.append((new_path, item))
                _search(item, new_path)

        # Primitive values (base case)
        else:
            # If the primitive itself matches, record the path
            if obj == target_value and path:
                results.append((path, obj))

    _search(data, "")
    return results


def find_value_paths_deduplicated(data, target_value):
    """
    Recursively search a nested JSON-like structure (dicts + lists)
    and return unique paths where the value equals `target_value`.
    """

    results = set()   # store (path, value) pairs to avoid duplicates

    def _search(obj, path):
        # dict case
        if isinstance(obj, dict):
            for key, value in obj.items():
                new_path = f"{path}.{key}" if path else key
                if value == target_value:
                    results.add((new_path, value))
                _search(value, new_path)

        # list case
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                new_path = f"{path}[{i}]"
                if item == target_value:
                    results.add((new_path, item))
                _search(item, new_path)

        # primitive case
        else:
            if obj == target_value and path:
                results.add((path, obj))

    _search(data, "")

    # Convert back to list for usability
    return list(results)



def main():
    func_no = 3
    match func_no:
        case 1:
            nested = {
                "a": {
                    "b": 10,
                    "c": [10, {"d": 20, "e": 10}]
                },
                "f": [{"g": 10}, {"h": 20}]
            }

            matches = find_value_paths_deduplicated(nested, 10)
            for path, val in matches:
                print(path, "=", val)

        case 2:
            with open("users.json") as file:
                data = json.load(file)

            for index, user in enumerate(data):
                if index > 3:
                    break
                print(find_value_paths_deduplicated(user, "Mastercard"))
        case 3:
            data1 = {
                "user": {
                    "profile": {
                        "name": "Alice",
                        "details": {
                            "bo": [[
                                {"age": 30, "location": {"city": "Boston"}},
                                {"projects": [{"title": "X"}, {"title": "Y", "city": "Miami"}]}
                            ]]}
                    }
                }
            }
            print(find_value_paths_deduplicated(data1, "Miami"))
            print(find_value_paths_deduplicated(data1, "X"))

        case 11:
            nested = {
                "a": {
                    "b": 10,
                    "c": [10, {"d": 20, "e": 10}]
                },
                "f": [{"g": 10}, {"h": 20}]
            }

            matches = find_value_paths(nested, 10)
            for path, val in matches:
                print(path, "=", val)

        case 12:
            with open("users.json") as file:
                data = json.load(file)

            for index, user in enumerate(data):
                if index > 3:
                    break
                print(find_value_paths(data, "Mastercard"))
        case 13:
            data1 = {
                "user": {
                    "profile": {
                        "name": "Alice",
                        "details": {
                            "bo": [[
                                {"age": 30, "location": {"city": "Boston"}},
                                {"projects": [{"title": "X"}, {"title": "Y", "city": "Miami"}]}
                            ]]}
                    }
                }
            }
            print(find_value_paths(data1, "Miami"))
            print(find_value_paths(data1, "X"))
        case _:  # Wildcard pattern for a default case
            print("no match")

if __name__ == "__main__":
    main()

