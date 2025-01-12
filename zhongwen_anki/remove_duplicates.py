import csv


def remove_duplicates(input_file, output_file):
    """
    Reads a TSV file, removes duplicate rows based on the first column,
    keeping the newest occurrence, and writes the result to a new TSV file.
    """
    seen = set()  # To track unique values in the first column
    rows_output = []

    with open(input_file, "r", encoding="utf-8") as f_in:
        reader = list(csv.reader(f_in, delimiter="\t"))

        # Check for a header
        header = reader[0] if reader else None

        # Iterate through rows in reverse order
        for row in reversed(reader[1:] if header else reader):
            if row[0] not in seen:
                seen.add(row[0])
                rows_output.append(row)

        # Reverse the results to maintain original order
        rows_output.reverse()

        if header:
            rows_output.insert(0, header)

    # Write out the results, preserving tab separation
    with open(output_file, "w", newline="", encoding="utf-8") as f_out:
        writer = csv.writer(f_out, delimiter="\t")
        writer.writerows(rows_output)


if __name__ == "__main__":
    input_path = r'../data/20241216_zhongwen_input.tsv'
    output_path = r'../data/20241216_zhongwen_input_.tsv'
    remove_duplicates(input_path, output_path)
    print(f"Duplicates removed. Output saved to: {output_path}")
