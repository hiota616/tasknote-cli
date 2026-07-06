import os

def meny():
    print('Select an action:')
    print('1 - Create a new note')
    print('2 - Edit an existing note')
    print('3 - Delete the note')
    print('0 - Close the program')

    try:
        mode = input()
    except Exception as error:
        print(f'An error occurred: {error}')
    else:
        return mode

def create_note(note):
    root = os.getcwd()
    note_file_path = os.path.join(root, 'notes.json')

    try:
        with open(note_file_path, 'a', encoding='utf-8') as note_file:
            note_file.write(note)
    
    except PermissionError:
        print('You do not have permission to create a note.')
    except OSError:
        print('System error while creating a note')