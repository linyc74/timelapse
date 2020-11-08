import cv2
import time
import arduino


def config_cam(cam_obj, param_vals):
    #              name            key
    param_keys = {'width'        : 3  ,
                  'height'       : 4  ,
                  'brightness'   : 10 ,
                  'contrast'     : 11 ,
                  'saturation'   : 12 ,
                  'hue'          : 13 ,
                  'gain'         : 14 ,
                  'exposure'     : 15 ,
                  'white_balance': 17 ,
                  'focus'        : 28 }

    for name in param_vals:
        cam_obj.set(param_keys[name], param_vals[name])


def get_cam_settings(cam):
    #               name            key
    param_keys = [('width        ', 3  ),
                  ('height       ', 4  ),
                  ('brightness   ', 10 ),
                  ('contrast     ', 11 ),
                  ('saturation   ', 12 ),
                  ('hue          ', 13 ),
                  ('gain         ', 14 ),
                  ('exposure     ', 15 ),
                  ('white_balance', 17 ),
                  ('focus        ', 28 )]

    for each_param in param_keys:
        (name, key) = each_param
        print(name + ': ' + str(cam.get(key)))

    print()


def initiate_serial(port, baudrate):

    try:
        ser = arduino.Serial(port, baudrate)
        # Always wait for a couple seconds to make sure the arduino is connected,
        #   otherwise following codes may get stuck
        time.sleep(2)

        return ser

    except:
        print('Serial port not connect.')
        return None


def main(cam_id, cam_param_vals, period, port, signal, prefix):

    # Initiate a camera object.
    cam = cv2.VideoCapture(cam_id)

    if not cam.isOpened():
        print('Camera not opened.')
        return

    # Configure the camera.
    config_cam(cam_obj=cam, param_vals=cam_param_vals)

    # Initiate a arduino object.
    # If not working, then ser = None
    ser = initiate_serial(port=port, baudrate=9600)

    time_zero = time.time()
    i = 0  # image id
    while True:

        # Read and show image
        ret, img = cam.read()
        cv2.imshow('Escherichia coli', img)

        elapsed_time = time.time() - time_zero

        if elapsed_time % period < 1:

            if not ser is None:
                ASCII = chr(signal) # Convert to ASCII
                ser.write(ASCII)
                time.sleep(1) # Wait for 1 second to ensure the arduino signal is properly sent

            i = i + 1 # image id
            minutes = int(elapsed_time/60)
            fname = prefix + '_' + str(i) + '_' + str(minutes) + '_min.jpg'
            cv2.imwrite(fname, img)

            # Pause for 1 second so the next iteration of the main loop will pass the specified period
            time.sleep(1)

        # Press ESC to break the main loop, terminating the timelapse
        k = cv2.waitKey(1)
        if k == 27: # 27 is ESC
            break

    # Properly close everything after the main loop is done
    cam.release()
    cv2.destroyAllWindows()

    if not ser is None:
        ser.close()


if __name__ == '__main__':
    cam_id = 0  # Usually 0 if there is only one USB camera connected
    cycle_period = 30  # seconds
    serial_port = 'COM3'  # The arduino port for Arduino UNO
    serial_signal = 1  # Should be an integer 0 ~ 127 (ASCII)
    filename_prefix = 'TimeLapsed'

    param_vals = {
        'width': 1280,
        'height': 720,
        'brightness': 150,
        'contrast': 100,
        'saturation': 120,
        'hue': 13,
        'gain': 100,
        'exposure': -3,
        'white_balance': 5000,
        'focus': 0
    }

    main(
        cam_id=cam_id,
        cam_param_vals=param_vals,
        period=cycle_period,
        port=serial_port,
        signal=serial_signal,
        prefix=filename_prefix)
