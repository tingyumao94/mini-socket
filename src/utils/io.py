def load_json(filename):
    with open(filename, "r") as f:
        return json.load(f)

def append_to_txt(ori_file, new_lines):
    with open(ori_file, 'a') as f:
        f.write(new_lines+'\n')
