import sys

import requests
import re


def write_buffer(existing_buffer_url, sheet_url):
    rows_regex = r"<td[\s\S]*?>([\w\.\/\;\s]*?)<\/"

    sheet_data = requests.get(sheet_url).text

    matches = re.finditer(rows_regex, sheet_data, re.MULTILINE)

    new_rows = ""
    for matchNum, match in enumerate(matches, start=1):
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            new_rows += match.group(groupNum)

    new_rows = set(new_rows.replace("\n", "").replace(";", "\n").split())

    existing_buffer_text = requests.get(existing_buffer_url).text

    if existing_buffer_text is not None and isinstance(existing_buffer_text, str) and len(existing_buffer_text) > 0:
        existing_buffer_text = set(existing_buffer_text.split("\n"))
        new_rows = set.union(new_rows, existing_buffer_text)

    new_file_contents = str()

    for item in new_rows:
        if len(item) > 0:
            definition_segments = item.split("/")
            # this fixes a bug in an older version of the dashboard app
            if len(definition_segments) > 2:
                item = definition_segments[-2] + "/" + definition_segments[-1]
            new_file_contents += item + "\n"

    if len(new_file_contents) > 0:
        f = open("buffered_feed", "w")
        f.write(new_file_contents)
        f.close()


if __name__ == "__main__":
    args = sys.argv
    globals()[args[1]](*args[2:])
