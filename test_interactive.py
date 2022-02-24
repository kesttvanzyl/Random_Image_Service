import zmq
from time import sleep


def myZMQ_Test_Pub_Sub():
    """ A socket publisher and subscriber """
    # setting up a sending side to request a service
    # context variable
    context = zmq.Context()
    # setup the socket
    socket_snd = context.socket(zmq.PUB)
    # bind it to a socket, local this time, set to what ever you want to use
    socket_snd.bind('tcp://127.0.0.1:2001')  # local port for testing

    #  set up the socket to connect to the port for rec the reply
    socket_rec = context.socket(zmq.SUB)
    # connect the socket to the port (same as in the publisher)
    socket_rec.connect('tcp://127.0.0.1:2000')

    # setting up the socket option and listen
    socket_rec.setsockopt_string(zmq.SUBSCRIBE, "")

    while True:
        message = input("Please enter a message: ")
        # quit the test program
        if message == "quit":
            return
        # send the message to the TCP port
        socket_snd.send_pyobj(message)
        print('sent message:', message)
        # setting up the received message
        message_ret = socket_rec.recv_pyobj()
        print("Returned message:", message_ret)


if __name__ == '__main__':
    myZMQ_Test_Pub_Sub()

