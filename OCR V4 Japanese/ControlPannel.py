import socketio
sio = socketio.Client()
sio.connect('http://localhost:5000')
while True:
 user_input = input("Enter something: ")





 if user_input:
        


        data = {'message': user_input }

        sio.emit('transferControl', data)

        