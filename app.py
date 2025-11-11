import ipywidgets as widgets
from IPython.display import display, clear_output

student_name_input = widgets.Text(placeholder='Enter student name...')
student_major_input = widgets.Text(placeholder='Enter student major...')

add_student_button = widgets.Button(description='Add Student', button_style='success')
view_student_button = widgets.Button(description='View Student', button_style='success')
delete_select_button = widgets.Button(description='Delete Selected Student', button_style='success')

def on_add_student_clicked(b):
    name = student_name_input.value
    major = student_major_input.value

    if name and major:
        session = Session()
        new_student = Student(name=name, major=major)
        session.add(new_student)
        session.commit()
        session.close()

        with student_output:
            clear_output()
            print(f"Success! Added student: {name}")

        student_name_input = ''
        student_major_input = ''
    else:
        with student_output:
            clear_output()
            print("Error: Both name and email are required.")

def on_view_student_clicked(b):
    name = student_name_input.value
    major = student_major_input.value

    if name and major:
        session = Session()
        student = Student(name=name, major=major)
        session.view(student)
        session.commit()
        session.close()
        
        with student_output:
            clear_output()
            print(f"Success! Added student: {name}")

        student_name_input = ''
        student_major_input = ''
    else:
        with student_output:
            clear_output()
            print("Error: Both name and email are required.")

def on_delete_select_student_clicked(b):
    name = student_name_input.value
    major = student_major_input.value

    if name and major:
        session = Session()
        student = Student(name=name, major=major)
        session.delete(student)
        session.commit()
        session.close()
        
        with student_output:
            clear_output()
            print(f"Success! Added student: {name}")

        student_name_input = ''
        student_major_input = ''
    else:
        with student_output:
            clear_output()
            print("Error: Both name and email are required.")


add_student_button.on_click(on_add_student_clicked)
print("--- Add a New Student---")
display(student_name_input, student_major_input, add_student_button, student_output)

view_student_button.on_click(on_view_student_clicked)
print("--- View an Existing Student---")
display(student_name_input, student_major_input, view_student_button, student_output)

delete_select_button.on_click(on_delete_select_student_clicked)
print("--- Delete a Select Student---")
display(student_name_input, student_major_input, delete_select_button, student_output)
