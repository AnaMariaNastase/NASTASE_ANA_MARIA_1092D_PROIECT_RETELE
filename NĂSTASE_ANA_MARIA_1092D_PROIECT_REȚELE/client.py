import socket
import json

def send_request(action, data):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 9999))
    request = json.dumps({'action': action, **data})
    client.send(request.encode())
    response = client.recv(4096).decode()
    client.close()
    return json.loads(response)

def select_students(student_ids):
    return send_request('select', {'student_ids': student_ids})
    
def update_student(student_id, name, age, major):
    send_request('update', {'student_id': student_id, 'name': name, 'age': age, 'major': major})
    print(f"Student {name} with ID {student_id} updated successfully.")
    

def delete_student(student_id):
    send_request('delete', {'student_id': student_id})
    print(f"Student  with ID {student_id} deleted successfully.")

def insert_student(student_id, name, age, major):
    send_request('insert', {'student_id': student_id, 'name': name, 'age': age, 'major': major})
    print(f"Student {name} with ID {student_id} inserted successfully.")


if __name__ == "__main__":

 insert_student('s1', 'Ionescu Andreea', 20, 'Informatica')
 insert_student('s2', 'Ion Popescu', 24, 'Informatica')
 insert_student('s3', 'Andrei Mihai', 21, 'Cibernetica')
 insert_student('s4', 'Claudiu Pop', 19, 'Statistica')
 #student_ids_to_select = ['s1', 's2']
 #print(select_students(student_ids_to_select))
 #update_student('s1', 'George Popescu', 21, 'Informatica')
 #delete_student('s2')
 