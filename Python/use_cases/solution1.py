import json

with open('dataset/training_session.json') as file:
    data = json.load(file)

def nested(value):
    """Handles the element which has more nested elements or iterable elements
    It prints sets and list elements directly and if the element contains dictionary,
    pass it to parser func"""
    if isinstance(value, (list, set)):   # set and list pass through
        for index,value in enumerate(value):
            print(index+1, end=") ")        #prints list or set by each element
            if hasattr(value, '__iter__') and not isinstance(value,str):    # if any element is further iterable(non string) then nested func again
                nested(value)
            else:print(value, end=" ")
    else: parser(value) # internal nested dictionary go to parser 

def parser(object):
    """Takes a dictionary object then prints elements inside  it, if those elements contains
    list or set pass it to nested func if they contain internal dict, just recursion"""
    for key, value in object.items():
        if hasattr(value, '__iter__') and not isinstance(value,str):
            print(key,"^^^^^" ,sep=":  ")
            nested(value)
        else:
            print(key," - ", value)
parser(data)