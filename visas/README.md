visas

Prompts, chatgpt:

Show me some JSON-formatted data on U.S. visa applications.
Can you show me data in the format used for ds-160?
DS-160 (Online Nonimmigrant Visa Application)
Include ISO-3166 alpha-3 formatted applicant nationality.
Include visa class code.
Generate 100 ds-160-style application records.  Include deeply nested structures for testing.  Provide elasticsearch-ready versions.

ds-160 directions:
Application ID: You will be given a unique application ID to access your form later. It's crucial to save this number.

Load the data into ES:
See:

/Users/blauerbock/workspaces/complete-guide-to-elasticsearch/run_elasticsearch_docker.md



I have a text file containing a list of deeply nested JSON objects.  The objects have keys associated with strings, numbers, objects/dicts and list, included nested lists.   Using Python, I want a function that can search each object recursively for a specific key.  If the key is found, I want the function to return the full path to the nested key as well as the value, whether the value is a string, dict, list or number.  The function must be able to correctly parse nested lists. 
 There should be no duplicates in the results, but a set should not be used to collect the results since the results may contain values that are unhashable, such as lists.
I also want to be able to provide a substring and have the function find keys that contain the substring.


Recursively search a nested JSON-like structure (dicts + lists)
and return all paths where the value equals `target_value`.
Returns: List of tuples: [(path_string, value), ...]
The target_value can be a string, number, list or dict/object.