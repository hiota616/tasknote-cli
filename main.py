import os
import uuid
import json
from datetime import datetime


def meny():
    while True:
        print('Select an action:')
        print('1 - Create a new note')
        print('2 - Edit an existing note')
        print('3 - Delete the note')
        print('0 - Close the program')

        try:
            mode = int(input())
            if mode == 1:
                new_note = create_note()
                write_file_note(new_note)
        except Exception as error:
            print(f'An error occurred: {error}')
        else:
            return mode
    

def create_note():
    try:
        id = uuid.uuid4().hex
        title = input('Enter a note title: ')
        text_note = input('Enter the note text: ')
        created_at =  str(datetime.now())
        updated_at = None
        deadline = input('Please specify a deadline: ')
        status = 'in process'

        notes = {
            id: {
                'title': title,
                'text_note': text_note,
                'created_at': created_at,
                'updated_at': updated_at,
                'deadline': deadline,
                'status': status
            }
        }
    except Exception as error:
        print(f'An error occurred while creating the note: {error}')
        return {}
    else:
        return notes



def write_file_note(note):
    root = os.getcwd()
    note_file_path = os.path.join(root, 'notes.json')
    try:
        with open(note_file_path, 'a', encoding='utf-8') as note_file:
            json.dump(note, note_file)
    
    except PermissionError:
        print('You do not have permission to create a note.')
    except OSError:
        print('System error while creating a note')

def main():
    meny()


main()    