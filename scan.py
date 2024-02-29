from evdev import InputDevice, categorize, ecodes
from datetime import datetime, time
from config.config import db_config, Name

import RPi.GPIO as GPIO
import mysql.connector
import threading
import time

import I2C_LCD_driver

#Pin Number
BUZZER_PIN = 17
sensor_pin = 27
barcode_pin = 26

#Define Time
set_hour = 23
set_minute = 50

#Define Var
shift_pressed = False
employee_id = ''
status = ''

backlight_off = False
data_off = True
last_input_time = time.time()

#Define root
mylcd = I2C_LCD_driver.lcd()
scanner_device = '/dev/input/event0'
db_file = "/home/620locker/config/state_db.txt"

key_mapping = {
    # Lower: a-z
    30: 'a', 48: 'b', 46: 'c', 32: 'd', 18: 'e', 33: 'f',
    34: 'g', 35: 'h', 23: 'i', 36: 'j', 37: 'k', 38: 'l',
    50: 'm', 49: 'n', 24: 'o', 25: 'p', 16: 'q', 19: 'r',
    31: 's', 20: 't', 22: 'u', 47: 'v', 17: 'w', 45: 'x',
    21: 'y', 44: 'z',

    # Number: 0-9
    11: '0', 2: '1', 3: '2', 4: '3', 5: '4',
    6: '5', 7: '6', 8: '7', 9: '8', 10: '9',
}

# Init GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#GPIO Setup
GPIO.setup(sensor_pin, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(barcode_pin, GPIO.OUT)
pwm = GPIO.PWM(BUZZER_PIN, 100)
pwm.start(0)

#Scan Card Sound
def beep(times, delay_between_beeps=0.05, frequency=4000, duration=0.1):
    for _ in range(times):
        pwm.ChangeFrequency(frequency)
        pwm.ChangeDutyCycle(50)
        time.sleep(duration)
        pwm.ChangeDutyCycle(0)
        time.sleep(delay_between_beeps)

def write_to_file(filename, data):
    try:
        with open(filename, 'w') as file:
            for key, value in data.items():
                file.write(f"{key}:{value}\n")
        print(f"Data has been written to {filename} successfully.")
    except Exception as e:
        print(f"An error occurred while writing to {filename}: {e}")

# Read existing data from file
def read_from_file(filename):
    try:
        data = {}
        with open(filename, 'r') as file:
            for line in file:
                key, value = line.strip().split(':')
                data[key] = value
        print(f"Data read from {filename}:")
        print(data)
        return data
    except FileNotFoundError:
        print(f"The file {filename} does not exist.")
    except Exception as e:
        print(f"An error occurred while reading from {filename}: {e}")

road_data = read_from_file(db_file)

def toggle_value(data, key):
    global backlight_off
    global data_off
    global last_input_time

    if key in data:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        beep(1)

        if backlight_off:
            mylcd.backlight(1)
            backlight_off = False
            data_off =True

        if data_off:
            last_input_time = time.time()

        # Toggle the value
        if data[key] == '0':
            data[key] = '1'
            status = '출근'
            mylcd.lcd_display_string(f"IN: {key}", 1)
            mylcd.lcd_display_string(f"Welcome! {current_time}", 2)

        elif data[key] == '1':
            data[key] = '0'
            status = '퇴근'
            mylcd.lcd_display_string(f"OUT: {key}", 1)
            mylcd.lcd_display_string(f"GoodBye! {current_time}", 2)

        employee_id = Name[key]
        insert_query = "INSERT INTO wpqkf_log (employee_id, status, timestamp) VALUES (%s, %s, NOW())"
        cursor.execute(insert_query, (employee_id, status))
        connection.commit()

        print(f"직원 ID: {employee_id}, 상태: {status}")

        employee_id = ''
        status = ''
        key = ''

        write_to_file(db_file, road_data)
        read_from_file(db_file)

    else:
        print(f"Key '{key}' not found in the data.")
        beep(3)

def find_and_update_value(data):
    keys_to_update = [key for key, value in data.items() if value == '1']
    if not keys_to_update:
        print("No keys found with value '1'.")
    else:
        for key in keys_to_update:
            data[key] = '0'
            #write_to_file(db_file, data)
            #Record Server
            employee_id = Name[key]
            status = '퇴근'
            insert_query = "INSERT INTO wpqkf_log (employee_id, status, timestamp) VALUES (%s, %s, NOW())"
            cursor.execute(insert_query, (employee_id, status))
            connection.commit()

            print(f"Key '{key}' value updated to '0'.")

        print("24:00이 되어 출근 중인 모든 직원에게 퇴근 기록을 추가했습니다.")

    return data


#At 24:00 All Employee Leave Work
def check_time_and_update(cursor, connection):
    global road_data
    leave_toogle = True

    while True:
        current_time = datetime.now().time()
        #print(current_time)
        if leave_toogle and current_time.hour == set_hour and current_time.minute == set_minute:
            road_data = find_and_update_value(road_data)
            leave_toogle = False
            write_to_file(db_file, road_data)
        elif current_time.minute != set_minute:
            leave_toogle = True
        time.sleep(30)

#Read Barcode
def read_barcode(device_path, cursor, connection):
    global employee_id
    global shift_pressed
    global status 
    global backlight_off
    global data_off
    global last_input_time
    global road_data

    barcode = ''
    dev = InputDevice(device_path)

    while True:
        try:
            if GPIO.input(sensor_pin):
                GPIO.output(barcode_pin, False)
                event = dev.read_one()
                if event and event.type == ecodes.EV_KEY:
                    data = categorize(event)
                    if data.scancode == ecodes.KEY_LEFTSHIFT or data.scancode == ecodes.KEY_RIGHTSHIFT:
                        shift_pressed = data.keystate == 1

                    elif data.keystate == 1:
                        if data.scancode == ecodes.KEY_ENTER:
                            print("스캔된 바코드:", barcode)
                            mylcd.lcd_display_string("barcode!" ,2)
                            toggle_value(road_data, barcode)
                            barcode = ''

                        elif data.scancode in key_mapping:
                            char = key_mapping[data.scancode]
                            if shift_pressed:
                                char = char.upper()
                            barcode += char

            else:
                GPIO.output(barcode_pin, True)
                barcode = ''
                if time.time() - last_input_time >= 3:
                    if data_off:
                        data_off = False
                        mylcd.lcd_clear()
                    mylcd.backlight(0)
                    backlight_off = True

        except mysql.connector.Error as err:
            print(f"오류: {err}")

if __name__ == "__main__":
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        time_thread = threading.Thread(target=check_time_and_update, args=(cursor, connection))
        time_thread.start()

        #Loadding Screen
        mylcd.lcd_display_string("620-Locker", 1)
        mylcd.lcd_display_string("System Booting..", 2)
        time.sleep(2)
        mylcd.lcd_clear()

        read_barcode(scanner_device, cursor, connection)
    except Exception as e:
        print("Error:", e)
    finally:
        pass

if connection.is_connected():
        cursor.close()
        connection.close()
