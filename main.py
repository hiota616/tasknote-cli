import os
import uuid
import json
from datetime import datetime


def menu():
    print('Select an action:')
    print('1 - Create a new note')
    print('2 - View notes')
    print('3 - Delete the note')
    print('4 - Edit an existing note')
    print('0 - Close the program')

    try:
        mode = int(input())
    except Exception as error:
        print(f'An error occurred: {error}')
    else:
        return mode
    return None
        
def get_data():
    root = os.getcwd()
    note_file_path = os.path.join(root, 'notes.json')
    try:
        with open(note_file_path, 'r', encoding='utf-8') as json_file:
            if json_file:
                data = json.load(json_file)
    except PermissionError:
        print('You do not have permission to view this note.')
    except OSError:
        print('System error while reading a note')
    else:
        return data
    return {}


def create_note(notes):
    try:
        note_id = uuid.uuid4().hex
        title = input('Enter a note title: ')
        text_note = input('Enter the note text: ')
        created_at =  datetime.now().isoformat().split('T')
        updated_at = None
        deadline = input('Please specify a deadline: ')
        status = 'in_process'

        notes[note_id] = {
                'title': title,
                'text_note': text_note,
                'created_at': created_at,
                'updated_at': updated_at,
                'deadline': deadline,
                'status': status
            }

    except Exception as error:
        print(f'An error occurred while creating the note: {error}')
    finally:
        return notes


def view_notes():
    notes = get_data()
    print('-' * 40)
    for key, values in notes.items():
        print(f'Post Title: {values['title']}')
        print(f'Note: {values['text_note']}')
        print(f'Date and time of creation: {values['created_at'][0]} at {values['created_at'][1]} ')
        if values['updated_at'] is not None:
            print(f'Date and time of last edited: {values['updated_at'][0]} at {values['updated_at'][1]}')
        print(f'Deadline: {values['deadline']}')
        print(f'Status: {values['status']}')
        print('-' * 40)
    

# def delete_note(notes, id):


def write_file_note(note):
    root = os.getcwd()
    note_file_path = os.path.join(root, 'notes.json')
    try:
        with open(note_file_path, 'w', encoding='utf-8') as note_file:
            json.dump(note, note_file)
    
    except PermissionError:
        print('You do not have permission to create a note.')
    except OSError:
        print('System error while creating a note')


def main():
    while True:
        mode = menu()
        if mode == 1:
            notes_file = get_data()
            note = create_note(notes_file)
            write_file_note(note)
        elif mode == 2:
            view_notes()
        elif mode == 3:
            pass
        elif mode == 0:
            break

main()    