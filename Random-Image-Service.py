# Kestt van Zyl - CS 361 W2022, Project - Microservice
# Special thanks to Rich Brinkly
# created with https://www.youtube.com/watch?v=-_CXA8SZsOs&t=534s
# use in conjunction with a receiver / subscriber end interface using ZMQ messaging
# version 0.1.0  All rights Reserved - Not for open distribution

import zmq
from time import sleep
import string
import random
from datetime import datetime
import os
from pathlib import Path


def dog():
    dogs_folder_path = Path("C:/Users/kestt/OneDrive/4 Oregon State/CS 361/Random_Image_Service/dogs")
    rand_dog = random.choice(os.listdir(dogs_folder_path))

    rand_dog_path = os.path.join(dogs_folder_path, rand_dog)

    return rand_dog_path


def cat():
    cats_folder_path = Path("C:/Users/kestt/OneDrive/4 Oregon State/CS 361/Random_Image_Service/cats")
    rand_cat = random.choice(os.listdir(cats_folder_path))

    rand_cat_path = os.path.join(cats_folder_path, rand_cat)

    return rand_cat_path


def car():
    cars_folder_path = Path("C:/Users/kestt/OneDrive/4 Oregon State/CS 361/Random_Image_Service/cars")
    rand_car = random.choice(os.listdir(cars_folder_path))

    rand_car_path = os.path.join(cars_folder_path, rand_car)

    return rand_car_path


def house():
    houses_folder_path = Path("C:/Users/kestt/OneDrive/4 Oregon State/CS 361/Random_Image_Service/houses")
    rand_house = random.choice(os.listdir(houses_folder_path))

    rand_house_path = os.path.join(houses_folder_path, rand_house)

    return rand_house_path


def landscape():
    landscapes_folder_path = Path("C:/Users/kestt/OneDrive/4 Oregon State/CS 361/Random_Image_Service/landscapes")
    rand_landscape = random.choice(os.listdir(landscapes_folder_path))

    rand_landscape_path = os.path.join(landscapes_folder_path, rand_landscape)

    return rand_landscape_path


def rand_image(select=0):
    """
    Returns either a randomly selected dog image file,
    random cat image file,
    random car image file,
    random house image file,
    or random landscape image file
    """

    # doing some stuff because random.seed() is changing to not work with hashed input
    curr_time = datetime.now()      # get current time for seed
    random.seed(curr_time.strftime('%f'))   # use just the milliseconds in string format

    random_dog = dog()
    random_cat = cat()
    random_car = car()
    random_house = house()
    random_landscape = landscape()

    # debug below
    # print(random_dog, random_cat, random_car, random_house, random_landscape)

    if select == 0:
        return random_dog
    elif select == 1:
        return random_cat
    elif select == 2:
        return random_car
    elif select == 3:
        return random_house
    elif select == 4:
        return random_landscape


def myZMQ_Sub_Pub():
    """
    A listening function that runs in a continuous while loop
    When a valid message string is received, the appropriate response is sent
    over the sending port. (different than receiving)
    Proper message format; = return message
    "get_rand(dog)"  = a single random dog image file
    "get_rand(cat)"  = a single random cat image file
    "get_rand(car)"  = a single random car image file
    "get_rand(house)"  = a single random house image file
    "get_rand(landscape)" = a single random landscape image file
    "STOP_STOP" = will terminate the service and return a message
    """

    # subscriber to listen for a request over the TCP line
    # set up a context
    context = zmq.Context()
    #  set up the socket to connect to the port
    socket_rec = context.socket(zmq.SUB)
    # connect the socket to the port (same as in the publisher)
    socket_rec.connect('tcp://127.0.0.1:2001')  # receive on port 2001

    # setting up the socket option and listen
    socket_rec.setsockopt_string(zmq.SUBSCRIBE, "")

    # *******************************
    # testing to see if moving stuff out of the sending function works better

    # publisher side to reply to the request
    socket_snd = context.socket(zmq.PUB)
    # bind it to a socket, local this time, set to what ever you want to use
    socket_snd.bind('tcp://127.0.0.1:2000')  # sending on port 2000 local for testing

    # list of valid commands
    valid = ["get_rand_image(dog)", "get_rand_image(cat)", "get_rand_image(car)", "get_rand_image(house)",
             "get_rand_image(landscape)", "STOP_STOP"]

    # logic to read the messages, loop for as long as the program is running
    while True:

        # setting up the received message
        message = socket_rec.recv_pyobj()
        # print the message for debug
        # print('printing message', message)  #debug

        if message not in valid:
            # print("invalid message")    # debug
            invalid_message = 'invalid command, please try again'
            socket_snd.send_pyobj(invalid_message)

        if message == "get_rand_image(dog)":
            output = rand_image(0)
            # print('sending:', opt)  # debug
            # myZMQ_Pub(opt)
            socket_snd.send_pyobj(output)

        elif message == "get_rand_image(cat)":
            output = rand_image(1)
            # print('sending:', opt)  # debug
            # myZMQ_Pub(opt)
            socket_snd.send_pyobj(output)

        elif message == "get_rand_image(car)":
            output = rand_image(2)
            # print('sending:', opt)  # debug
            # myZMQ_Pub(opt)
            socket_snd.send_pyobj(output)

        elif message == "get_rand_image(house)":
            output = rand_image(3)
            # print('sending:', opt)  # debug
            socket_snd.send_pyobj(output)

        elif message == "get_rand_image(landscape)":
            output = rand_image(4)
            # print('sending:', opt)  # debug
            socket_snd.send_pyobj(output)

        # a way to stop to process deliberately
        elif message == "STOP_STOP":
            socket_snd.send_pyobj('Stopping service, good bye')
            break


if __name__ == '__main__':
    print("Random-Image-Service Ver 0.1.0 is running")
    # myZMQ_Pub()
    myZMQ_Sub_Pub()
    print("Random-Image-Service Ver 0.1.0 is stopping")
