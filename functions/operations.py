import os
from pandas.errors import ParserError
from PyQt6.QtWidgets import QFileDialog
from gui.elements import InfoWindow, ErrorWindow, SuccessWindow, Options
from functions import options
from PyQt6 import QtCore

def browse_file(filter, browser_bar, progress_bar):
    desktop_path = os.path.join(os.path.join(
        os.environ['USERPROFILE']), 'Desktop')
    file_path = QFileDialog.getOpenFileName(
        caption='Open file', directory=desktop_path, filter=filter)
    browser_bar.setText(file_path[0])
    progress_bar.setValue(0)

def filter(options, filter_type):
    if options[0].isChecked():
        filter_type('*.txt')
    elif options[3].isChecked():
        filter_type('*.xlsx')
    elif options[1].isChecked() or options[2].isChecked():
        filter_type('*.csv')
    else:
        info_window = InfoWindow(
            'Please select an option before browse your file'
        )
        info_window.show()
        info_window.move_center()

def show_error(e, message):
    error_window = ErrorWindow(
        f'{str(e)}\n{message}', 
    )
    error_window.show()
    error_window.move_center()

def show_info(message):
    info_window = InfoWindow(message)
    info_window.show()
    info_window.move_center()
    loop = QtCore.QEventLoop()
    info_window.destroyed.connect(loop.quit)
    loop.exec()

def show_success(message):
    success_window = SuccessWindow(message)
    success_window.show()
    success_window.move_center()
    loop = QtCore.QEventLoop()
    success_window.destroyed.connect(loop.quit)
    loop.exec()

def save_file(data, progress_bar):
    desktop_path = os.path.join(os.path.join(
        os.environ['USERPROFILE']), 'Desktop')
    file_path = QFileDialog.getSaveFileName(
        caption='Open file', directory=desktop_path, filter='*.txt')
    bar_metter = 1
    progress_bar.setRange(0, len(data))
    with open(file_path[0], "w") as final_file:
        for line in data:
            progress_bar.setValue(bar_metter)
            bar_metter += 1
            final_file.writelines(line)
    show_success('File successfully converted and saved')

def convert_process(file_name, options_list, progress_bar):
    if options_list[0].isChecked():
        try:
            data = options.process_1(file_name)
            save_file(data, progress_bar)
        except UnicodeDecodeError as e:
                show_error(e, 'Please select a valid txt file')
        except FileNotFoundError as e:
                show_error(e, 'Please select a file before convert')
        finally:
            options_list[0].setChecked(False)
    elif options_list[1].isChecked():
        try:
            data = options.process_2(file_name)
            save_file(data, progress_bar)
        except OSError as e:
            show_error(e, 'The file is currently open, please close it and try again')     
        except UnicodeDecodeError as e:
            show_error(e, 'Please select a valid csv file')
        except FileNotFoundError as e:
            show_error(e, 'Please select a file before convert')
        except KeyError as e:
            show_error(e, f'Missing column {e}, please select a valid file')
        except IndexError as e:
            show_error(e, f'There is an invalid field in retentions, please check the file')
        except TypeError as e:
            show_error(e, f'There is an invalid field in retentions.\nPossibly you modify the file and saved it, please use the raw file')        
    elif options_list[2].isChecked():
        try:
            data = options.process_3(file_name)
            save_file(data, progress_bar)
        except OSError as e:
            show_error(e, 'The file is currently open, please close it and try again')     
        except UnicodeDecodeError as e:
            show_error(e, 'Please select a valid csv file')
        except FileNotFoundError as e:
            show_error(e, 'Please select a file before convert')
        except KeyError as e:
            show_error(e, f'Missing column {e}, please select a valid file')   
    elif options_list[3].isChecked():
        try:
            show_info('The program will process retentions first and then perceptions\n Please save the files in that order')
            data = options.process_4_1(file_name)
            save_file(data, progress_bar)
            data = options.process_4_2(file_name)
            save_file(data, progress_bar)
        except OSError as e:
            show_error(e, 'The file is currently open, please close it and try again')
        except KeyError as e:
            show_error(e, f'Missing column {e}, please select a valid file')     
        except ParserError as e:
            show_error(e, 'Please select a valid xlsx file')      
        except ValueError as e:
            show_error(e, 'Please select a valid xlsx file')       
    else:
        show_info('Please select an option before convert your file')