import os
import uuid
import json
from datetime import datetime


def main_menu():
    print('*' * 9)
    print('MAIN MENU')
    print('*' * 9)
    print('Select an action:')
    print('1 - Create a new note')
    print('2 - View notes')
    print('3 - Delete the note')
    print('4 - Edit an existing note')
    print('0 - Close the program')

    try:
        mode = int(input())
    except ValueError:
        print('Incorrect command.')
    else:
        return mode
    return None


def get_data():
    root = os.getcwd()
    note_file_path = os.path.join(root, 'notes.json')
    
    try:
        if os.path.isfile(note_file_path):
            with open(note_file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                if not isinstance(data, dict):
                    return None
                
                return data

        else:
            with open(note_file_path, 'w', encoding='utf-8') as json_file:
                json.dump({}, json_file)
                return {}

    except json.decoder.JSONDecodeError:
        return None
    except PermissionError:
        print('You do not have permission to view this note.')
        return None
    except OSError:
        print('System error while reading a note')
        return None
     

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


def create_note(notes):
    try:
        if isinstance(notes, dict):
            note_id = uuid.uuid4().hex
            title = input('Enter a note title: ')
            text_note = input('Enter the note text: ')
            if not title or not text_note:
                raise ValueError('Empty fields: Header or Text')
            created_at =  datetime.now().isoformat().split('T')
            updated_at = None
            deadline = input('Please specify a deadline: ')
            if not deadline:
                deadline = None
            status = 'in_process'

            notes[note_id] = {
                    'title': title,
                    'text_note': text_note,
                    'created_at': created_at,
                    'updated_at': updated_at,
                    'deadline': deadline,
                    'status': status
                }
        else:
            raise TypeError('The JSON file does not contain a dictionary')
    except TypeError as error:
        print(f'An error occurred while creating the note: {error}')
        return None
    except ValueError as error:
        print(f'An error occurred while creating the note: {error}')
        return notes
    else:
        return notes


def print_note(key, values):
    try:
        print('-' * 40)
        print(f'Post Title: {values['title']}')
        print(f'Note: {values['text_note']}')
        print(f'Date and time of creation: {values['created_at'][0]} at {values['created_at'][1]} ')
        if values['updated_at'] is not None:
            print(f'Date and time of last edited: {values['updated_at'][0]} at {values['updated_at'][1]}')
        print(f'Deadline: {values['deadline']}')
        print(f'Status: {values['status']}')

    except IndexError:
        print(f'The note "{values['title']}" was recorded incorrectly')
    

def view_menu():
    print('*' * 9)
    print('VIEW MENU')
    print('*' * 9)
    print('1 - Show "In Progress" status.')
    print('2 - Show "Completed" status.')
    print('3 - Show "Archive" status.')
    print('4 - View all notes.')
    print('0 - Return to the main menu.')
    try:
        view_mode = int(input())
    except ValueError:
        print('Incorrect command.')
    else:
        return view_mode
    return None
    

def view_notes():
    notes = get_data()
    view_mode = view_menu()
    for key, values in notes.items():
        if view_mode == 1:
            if values['status'] == 'in_process':
                print_note(key, values)
        elif view_mode == 2:
            if values['status'] == 'done':
                print_note(key, values)
        elif view_mode == 3:
            if values['status'] == 'archived':
                print_note(key, values)
        elif view_mode == 4:
            print_note(key, values)
        elif view_mode == 0:
            break
                

def find_title(notes, title):
    for key, values in notes.items():
        if values['title'] == title:
            return key
    
    print('The title is incorrect or is missing from the database.')
    return None

def delete_menu():
    print('*' * 9)
    print('DELETE MENU')
    print('*' * 9)
    try:
        title = input('Enter the title of the note you want to delete: ')
        if not title:
            raise ValueError('No title was entered.')
        return title
    except ValueError as error:
        print(error)


def delete_note():
    title_name = delete_menu()
    notes_data = get_data()
    note_id = find_title(notes_data, title_name)
    if note_id is not None:
        notes_data.pop(note_id)
        write_file_note(notes_data)

def main():
    while True:
        mode = main_menu()
        if mode == 1:
            notes_file = get_data()

            if notes_file is None:
                print('Program stopped: notes data was not loaded.')
                break
            
            note = create_note(notes_file)
            if note is not None:
                write_file_note(note)
            else:
                pass
        elif mode == 2:
            view_notes()
        elif mode == 3:
            delete_note()
        elif mode == 0:
            break

main()    