def save_to_file(filename, data):
    with open(filename, "w") as f:
        f.write(data)

def load_from_file(filename):
    with open(filename, "r") as f:
        return f.read()
