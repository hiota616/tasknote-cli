import os
import uuid
import json
from InquirerPy import inquirer
from datetime import datetime

def menu(message, options):
    selector = inquirer.select(
        message=message,
        choices=options
    ).execute()
    return selector


def get_data():
    root = os.getcwd()
    note_file_path = os.path.join(root, 'notes.json')
    
    try:
        if os.path.isfile(note_file_path):
            with open(note_file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                if not isinstance(data, dict):
                    raise ValueError('The notes file is corrupted. This is not a dictionary.')
                
                return data

        else:
            with open(note_file_path, 'w', encoding='utf-8') as json_file:
                json.dump({}, json_file)
                return {}
            
    except ValueError as error:
        print(f'An error occurred during recording: {error}')
        return None
    except json.decoder.JSONDecodeError:
        print('The file is corrupted or empty.')
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
    temp_file_path = os.path.join(root, 'temp_notes.json')
    try:
        if not isinstance(note, dict):
            raise ValueError("You're trying to save something other than a dictionary")
        with open(temp_file_path, 'w', encoding='utf-8') as temp_file:
            json.dump(note, temp_file, ensure_ascii=False, indent=4)

        os.replace(temp_file_path, note_file_path)
    
    except ValueError as error:
        print(f'An error occurred during recording: {error}')
    except PermissionError:
        print('You do not have permission to create a note.')
    except OSError:
        print('System error while creating a note')
    else:
        print('The changes have been successfully made!')


def create_note(notes):
    try:
        if isinstance(notes, dict):
            note_id = uuid.uuid4().hex
            title = input('Enter a note title: ')
            text_note = input('Enter the note text: ')
            if not title.strip() or not text_note.strip():
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
        return None
    else:
        return notes


def print_note(key, values):
    try:
        print('-' * 40)
        print(f"Post Title: {values['title']}")
        print(f"Note: {values['text_note']}")
        print(f"Date and time of creation: {values['created_at'][0]} at {values['created_at'][1]}")
        if values['updated_at'] is not None:
            print(f"Date and time of last edited: {values['updated_at'][0]} at {values['updated_at'][1]}")
        print(f"Deadline: {values['deadline']}")
        print(f"Status: {values['status']}")

    except KeyError as error:
        print(f'An error occurred while displaying the note: {error}')
    except IndexError as error:
        print(f"The note {values['title']} was recorded incorrectly")
    except TypeError as error:
        print(f'An error occurred while displaying the note: {error}')


def view_notes():
    notes = get_data()
    if notes is not None:
        print('VIEW MENU')
        view_mode = menu('Select an action:',
                [
                {'name': 'Show "In Progress" status', 'value': 'in_process'},
                {'name': 'Show "Completed" status', 'value': 'done'},
                {'name': 'Show "Archive" status', 'value': 'archived'},
                {'name': 'View all notes', 'value': 'all'},
                {'name': 'Return to the main menu', 'value': 'return_to_main'},
                ]
                )
        for key, values in notes.items():
            if view_mode == 'return_to_main':
                break
            elif view_mode == 'in_process':
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
            
        print('-' * 40)
    else:
        print('Notes data was not loaded.')
                

def get_titles(notes):
    keys_titles = []
    for key, values in notes.items():
        try:
            if not values['title']:
                raise ValueError(f'No title. ID: {key}')
            keys_titles.append((key, values['title']))
        except ValueError as error:
            print(f'An error occurred while creating the note: {error}')

    return keys_titles


def search_note_by_title(notes, title):
    for key, values in notes.items():
        if values['title'] == title:
            return key

    print('The title is incorrect or is missing from the database.')
    return None
    

def delete_note():
    print('DELETE MENU')
    try:
        notes = get_data()

        if notes is None:
            raise ValueError('Empty fields: Notes')
        
        if notes == {}:
            print('There are no notes in the database.')
        else:
            keys_titles = get_titles(notes)
            print(keys_titles)
            
            keys_titles.append({'name': 'Return to the main menu', 'value': 'return_to_main'})
            title_note = menu('Select which note to delete:', keys_titles)

            if title_note != 'return_to_main':
                note_id = search_note_by_title(notes, title_note)

                if note_id is None:
                    raise ValueError('Empty fields: id')
                
                clarification = menu('Are you sure you want to delete this note?', ['Yes', 'No'])

                if clarification == 'Yes':
                    notes.pop(note_id)
                    write_file_note(notes)
                
            
    except ValueError as error:
        print(f'An error occurred while creating the note: {error}')


def edit_note_value(notes, id_note, change_value, new_data):
    notes[id_note][change_value] = new_data
    return notes


def edit_note():
    print('EDIT MENU')
    notes = get_data()
    if notes is not None:
        titles = get_titles(notes)
        try:
            if not titles:
                raise ValueError(f'There are no notes that can be edited.')
            title = menu('Select a note:', titles)
            edit_mode = menu('Select an action:',
                    [
                    {'name': 'Change the title', 'value': 'title'},
                    {'name': 'Change the description', 'value': 'text_note'},
                    {'name': 'Change the deadline', 'value': 'deadline'},
                    {'name': 'Change the status', 'value': 'status'},
                    {'name': 'Return to the main menu', 'value': 'return_to_main'}
                    ]
                    )

            note_id = search_note_by_title(notes, title)
            if note_id is None:
                raise ValueError('Empty fields: id')

            if edit_mode != 'return_to_main':
            
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
                    new_data = menu('Select a status:',
                            [
                            {'name': 'In the process', 'value': 'in_process'},
                            {'name': 'Done', 'value': 'done'},
                            {'name': 'Archive', 'value': 'archived'},
                            ]
                            )

                notes = edit_note_value(notes, note_id, edit_mode, new_data)
                notes[note_id]['updated_at'] = datetime.now().isoformat().split('T')
                write_file_note(notes)

        except ValueError as error:
            print(f'An error occurred while edit the note: {error}')
    else:
        print('Notes data was not loaded.')


def main():
    while True:
        mode = menu('Select an action:',
            [
            {'name': 'Create a new note', 'value': 'create'},
            {'name': 'View notes', 'value': 'view'},
            {'name': 'Delete the note', 'value': 'delete'},
            {'name': 'Edit an existing note', 'value': 'edit'},
            {'name': 'Close the program', 'value': 'close'},
            ]
            )
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
            delete_note()
        elif mode == 'edit':
            edit_note()
        elif mode == 'close':
            break

main()    