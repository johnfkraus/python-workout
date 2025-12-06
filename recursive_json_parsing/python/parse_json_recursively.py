import json
from typing import Any
# from dotmap import DotMap

def find_key_paths(data: Any, target_key: str|int|float):
    """
    Recursively search a nested JSON-like structure (dicts + lists)
    and return all paths where `target_key` is found, along with values.

    Returns:
        List of tuples: [(path_string, value), ...]
        Example path: "root.addresses[2].street"
    """
    print(type(data), type(target_key))
    results = []

    def _search(obj, path):
        if isinstance(obj, dict):
            for key, value in obj.items():
                new_path = f"{path}.{key}" if path else key
                if key == target_key:
                    results.append((new_path, value))
                _search(value, new_path)

        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                new_path = f"{path}[{i}]"
                _search(item, new_path)

        # Base case: primitives → ignore
        else:
            return

    _search(data, "")
    return results


# Load objects from a text file (one JSON object per line)
# with open("data.txt") as f:
#     objects = [json.loads(line) for line in f]
#
# # Search each object
# for idx, obj in enumerate(objects):
#     matches = find_key_paths(obj, "ADJUDICATION")
#     print(f"Object {idx}:")
#     for path, value in matches:
#         print("  Path:", path)
#         print("  Value:", value)

data0 = {
    "user": {
        "profile": {
            "name": "Alice",
            "details": [
                {1: "number_here"},
                {"age": 30, "location": {"city": "Boston"}},
                {"projects": [{"title": "X"}, {"title": "Y", "city": "Miami"}]}
            ]
        }
    }
}





def main():
    func_no = 1
    match func_no:
        case 1:
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
            results = find_key_paths(data1, "city")
            print(results)
            assert data1['user']['profile']['details']['bo'][0][0]['location']['city'] == "Boston"
            print(f"{data1['user']['profile']['details']['bo'][0][0]['location']['city'] == 'Boston'=}")
            print(f"{data1['user']['profile']['details']['bo'][0][1]['projects'][1]['city'] == 'Miami'=}")

        case 2:
            with open("users.json") as file:
                data = json.load(file)

            for index, user in enumerate(data):
                if index > 3:
                    break
                print(find_key_paths(data, "lat"))
        case 3:
            # test int as key, works!
            print(find_key_paths(data0, 1))

        case _:  # Wildcard pattern for a default case
            print("no match")

if __name__ == "__main__":
    main()