def read_file(file_name):
    try:
        with open(file_name, "r") as fh:
            data = fh.read()
            return data
    except Exception as e:
        print(e)


def remove_attributes(record, indices):
    new_record = [i for j, i in enumerate(record) if j not in indices]
    return new_record
