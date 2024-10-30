# Let's check the contents of the .txt file, as it might contain a hidden message.
txt_file_path = './df.zip'

with open(txt_file_path, 'r') as file:
    txt_content = file.read()

    print(txt_content)
