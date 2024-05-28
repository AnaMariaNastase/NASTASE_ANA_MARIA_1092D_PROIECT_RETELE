import socket
import threading
import sqlite3
import json

clients = []

def handle_client(client_socket):
    try:
        while True:
            request = client_socket.recv(1024).decode()
            if not request:
                break
            request = json.loads(request)
            action = request.get('action')
            if action == 'select':
                student_ids = request.get('student_ids')
                response = select_students(student_ids)
                client_socket.send(json.dumps(response).encode())
                clients.append((client_socket, student_ids))
            elif action == 'update':
                student_id = request.get('student_id')
                name = request.get('name')
                age = request.get('age')
                major = request.get('major')
                update_student(student_id, name, age, major)
                notify_clients(student_id, name, age, major)
                client_socket.send(json.dumps({'status': 'success', 'message': 'Student updated successfully.'}).encode())
            elif action == 'delete':
                student_id = request.get('student_id')
                delete_student(student_id)
                notify_clients(student_id, None, None, None)
                client_socket.send(json.dumps({'status': 'success', 'message': 'Student deleted successfully.'}).encode())
            elif action == 'insert':
                student_id = request.get('student_id')
                name = request.get('name')
                age = request.get('age')
                major = request.get('major')
                if student_exists(student_id):
                    response = {'status': 'error', 'message': f'Student with ID {student_id} already exists.'}
                else:
                    insert_student(student_id, name, age, major)
                    response = {'status': 'success', 'message': f'Student {name} with ID {student_id} inserted successfully.'}
                client_socket.send(json.dumps(response).encode())
    except Exception as e:
        print(f"Error handling client: {e}")
        client_socket.send(json.dumps({'status': 'error', 'message': str(e)}).encode())
        
    finally:
        client_socket.close()

def student_exists(student_id):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM students WHERE student_id = ?", (student_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def select_students(student_ids):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    query = "SELECT * FROM students WHERE student_id IN ({})".format(','.join('?' * len(student_ids)))
    cursor.execute(query, student_ids)
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_student(student_id, name, age, major):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO students (student_id, name, age, major) VALUES (?, ?, ?, ?)", (student_id, name, age, major))
    conn.commit()
    conn.close()

def delete_student(student_id):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
    conn.commit()
    conn.close()

def insert_student(student_id, name, age, major):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (student_id, name, age, major) VALUES (?, ?, ?, ?)", (student_id, name, age, major))
    conn.commit()
    conn.close()

def notify_clients(student_id, name, age, major):
    for client, student_ids in clients:
        if student_id in student_ids:
            notification = {'student_id': student_id, 'name': name, 'age': age, 'major': major}
           
            client.send(json.dumps(notification).encode())
            


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    print("Server started on port 9999")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


start_server()
