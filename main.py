import os
import uuid
import json
from InquirerPy import inquirer
from datetime import datetime


def main_menu():
    mode = inquirer.select(
        message='Select an action:',
        choices=[
            {'name': 'Create a new note', 'value': 'create'},
            {'name': 'View notes', 'value': 'view'},
            {'name': 'Delete the note', 'value': 'delete'},
            {'name': 'Edit an existing note', 'value': 'edit'},
            {'name': 'Close the program', 'value': 'close'},
            ]
    ).execute()

    return mode


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
    print('VIEW MENU')
    view_mode = inquirer.select(
        message='Select an action:',
        choices=[
            {'name': 'Show "In Progress" status', 'value': 'in_process'},
            {'name': 'Show "Completed" status', 'value': 'done'},
            {'name': 'Show "Archive" status', 'value': 'archived'},
            {'name': 'View all notes', 'value': 'all'},
            {'name': 'Return to the main menu', 'value': 'return_to_main'},
            ]
    ).execute()

    return view_mode


def view_notes():
    notes = get_data()
    view_mode = view_menu()
    for key, values in notes.items():
        if view_mode == 'in_process':
            if values['status'] == view_mode:
                print_note(key, values)
        elif view_mode == 'done':
            if values['status'] == view_mode:
                print_note(key, values)
        elif view_mode == 'archived':
            if values['status'] == view_mode:
                print_note(key, values)
        elif view_mode == 'all':
            print_note(key, values)
        elif view_mode == 'return_to_main':
            break
    print('-' * 40)
                

def get_titles(notes):
    titles = []
    for key, values in notes.items():
        titles.append(values['title'])
    return titles


def search_note_by_title(notes, title):
    for key, values in notes.items():
        if values['title'] == title:
            return key

    print('The title is incorrect or is missing from the database.')
    return None


def delete_menu():
    print('DELETE MENU')
    notes = get_data()
    titles = get_titles(notes)
    titles.append({'name': 'Return to the main menu', 'value': 'return_to_main'})
    title_note = inquirer.select(
        message='Select which note to delete:',
        choices= titles
    ).execute()
    if title_note != 'return_to_main':
        delete_note(notes, title_note)
    

def delete_note(notes_data, title_name):
    note_id = search_note_by_title(notes_data, title_name)
    notes_data.pop(note_id)
    write_file_note(notes_data)
    print(f'The note "{title_name}" has been deleted from the database.')\
        

def edit_note_value(notes, id_note, change_value, new_data):
    notes[id_note][change_value] = new_data
    return notes


def edit_note_menu():
    print('EDIT MENU')
    notes = get_data()
    titles = get_titles(notes)

    title = inquirer.select(
        message='Select a note:',
        choices=titles
    ).execute()

    edit_mode = inquirer.select(
        message='Select an action:',
        choices=[
            {'name': 'Change the title', 'value': 'title'},
            {'name': 'Change the description', 'value': 'text_note'},
            {'name': 'Change the deadline', 'value': 'deadline'},
            {'name': 'Change the status', 'value': 'status'},
            {'name': 'Return to the main menu', 'value': 'return_to_main'}
            ]
    ).execute()

    note_id = search_note_by_title(notes, title)
    
    try:
        if edit_mode == 'title':
            new_data = input('Enter a new title: ')
            if not new_data:
                raise ValueError('Empty fields: Header')
        elif edit_mode == 'text_note':
            new_data = input('Enter a new description: ')
            if not new_data:
                raise ValueError('Empty fields: Description')
            
        elif edit_mode == 'deadline':
            new_data = input('Enter a new deadline: ')

        elif edit_mode == 'status':
            new_data = inquirer.select(
                message='Select a status:',
                choices=[
                    {'name': 'In the process', 'value': 'in_process'},
                    {'name': 'Done', 'value': 'done'},
                    {'name': 'Archive', 'value': 'archived'},
                ]
            ).execute()

        elif edit_mode == 'return_to_main':
            pass

        notes = edit_note_value(notes, note_id, edit_mode, new_data)
        notes[note_id]['updated_at'] = datetime.now().isoformat().split('T')
        write_file_note(notes)

    except ValueError as error:
        print(f'An error occurred while edit the note: {error}')


def main():
    while True:
        mode = main_menu()
        if mode == 'create':
            notes_file = get_data()

            if notes_file is None:
                print('Program stopped: notes data was not loaded.')
                break
            
            note = create_note(notes_file)
            if note is not None:
                write_file_note(note)
            else:
                pass
        elif mode == 'view':
            view_notes()
        elif mode == 'delete':
            delete_menu()
        elif mode == 'edit':
            edit_note_menu()
        elif mode == 'close':
            break

main()    