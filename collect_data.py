# modified from sentdex's pygta5
import numpy as np
from grabscreen import grab_screen
import cv2
import time
from getkeys import key_check
import os

# Input map - Magnitude of each integer is press confidence
# [W, A, S, D, SPACE, SHIFT, CTRL, Pointer_X, Pointer_Y]
#  0  1  2  3  4      5      6     7          8

starting_value = 1
save_directory = 'C:/Users/rfhpecka/Developer/CSGOBot_training_data/phase1/'
file_name_format = 'training_data-{}.npy'
samples_per_file = 100
log_print_interval = 100

while True:
    file_name = (save_directory + file_name_format).format(starting_value)

    if os.path.isfile(file_name):
        print('File exists, moving along', starting_value)
        starting_value += 1
    else:
        print('File does not exist, starting fresh!', starting_value)
        
        break


def user_input_to_output(keys, mouse_x, mouse_y): # TODO: Dont use so many hardcoded strings here
    '''
    Convert keys and mouse state to a ...multi-hot... array based on the input map above
    '''
    output = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    if 'W' in keys:
        output[0] = 1
    if 'A' in keys:
        output[1] = 1
    if 'S' in keys:
        output[2] = 1
    if 'D' in keys:
        output[3] = 1
    if " " in keys:
        output[4] = 1
    if "SHIFT" in keys:
        output[5] = 1
    if "CTRL" in keys:
        output[6] = 1

    output[7] = mouse_x
    output[8] = mouse_y

    return output


def main(file_path, starting_index):
    file_index = starting_index
    training_data = []
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)

    # last_time = time.time()
    paused = False
    print('STARTING!!!')
    while True:
        
        if not paused:
            screen = grab_screen(region=(0, 40, 1600, 920))
            # last_time = time.time()
            # resize to something a bit more acceptable for a CNN
            screen = cv2.resize(screen, (240, 135))
            # run a color convert:
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            
            keys, mouse_x, mouse_y = key_check()
            output = user_input_to_output(keys, mouse_x, mouse_y)
            training_data.append([screen, output])

            #print('loop took {} seconds'.format(time.time()-last_time))
            # last_time = time.time()
            # cv2.imshow('window',cv2.resize(screen,(240,135)))
            # cv2.moveWindow('window', 1602, 550)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

            if len(training_data) % log_print_interval == 0:
                print(len(training_data))
                
            if len(training_data) == samples_per_file:
                np.save(file_path.format(file_index), training_data)
                print('SAVED')
                training_data = []
                file_index += 1
                    
        keys = key_check()[0]
        if 'P' in keys:
            if paused:
                paused = False
                print('unpaused!')
                time.sleep(1)
            else:
                print('Pausing!')
                paused = True
                time.sleep(1)


main(file_name, starting_value)
