from math import degrees, atan
from time import sleep

from autopilot.control import keyboard, keys
from autopilot.elite import ship
from autopilot.vision import get_sun_percent, get_navpoint_offset, get_destination_offset


def x_angle(point=None):
    if not point or point['x'] == 0:
        return None
    result = degrees(atan(point['y'] / point['x']))
    if point['x'] > 0:
        return +90 - result
    else:
        return -90 - result


def align():
    # logging.debug('align')
    if not (ship().status.in_supercruise or ship().status.in_space):
        # logging.error('align=err1')
        raise Exception('align error 1')

    # logging.debug('align= speed 100')
    keyboard.tap(keys['SetSpeed100'])

    # logging.debug('align= avoid sun')
    while get_sun_percent() > 5:
        keyboard.press(keys['PitchUpButton'])
    keyboard.release(keys['PitchUpButton'])

    # logging.debug('align= find navpoint')
    off = get_navpoint_offset()
    while not off:
        keyboard.press(keys['PitchUpButton'])
        off = get_navpoint_offset()
    keyboard.release(keys['PitchUpButton'])

    # logging.debug('align= crude align')
    close = 3
    close_a = 18
    hold_pitch = 0.350
    hold_roll = 0.170
    ang = x_angle(off)
    while (off['x'] > close and ang > close_a) or (off['x'] < -close and ang < -close_a) or (off['y'] > close) or (
            off['y'] < -close):

        while (off['x'] > close and ang > close_a) or (off['x'] < -close and ang < -close_a):

            if off['x'] > close and ang > close:
                keyboard.hold(keys['RollRightButton'], hold=hold_roll)
            if off['x'] < -close and ang < -close:
                keyboard.hold(keys['RollLeftButton'], hold=hold_roll)

            if ship().status.starting_hyperspace:
                return
            off = get_navpoint_offset(last=off)
            ang = x_angle(off)

        ang = x_angle(off)
        while (off['y'] > close) or (off['y'] < -close):

            if off['y'] > close:
                keyboard.hold(keys['PitchUpButton'], hold=hold_pitch)
            if off['y'] < -close:
                keyboard.hold(keys['PitchDownButton'], hold=hold_pitch)

            if ship().status.starting_hyperspace:
                return
            off = get_navpoint_offset(last=off)
            ang = x_angle(off)

        off = get_navpoint_offset(last=off)
        ang = x_angle(off)

    # logging.debug('align= fine align')
    sleep(0.5)
    close = 50
    hold_pitch = 0.200
    hold_yaw = 0.400
    for i in range(5):
        new = get_destination_offset()
        if new:
            off = new
            break
        sleep(0.25)
    if not off:
        return
    while (off['x'] > close) or (off['x'] < -close) or (off['y'] > close) or (off['y'] < -close):

        if off['x'] > close:
            keyboard.hold(keys['YawRightButton'], hold=hold_yaw)
        if off['x'] < -close:
            keyboard.hold(keys['YawLeftButton'], hold=hold_yaw)
        if off['y'] > close:
            keyboard.hold(keys['PitchUpButton'], hold=hold_pitch)
        if off['y'] < -close:
            keyboard.hold(keys['PitchDownButton'], hold=hold_pitch)

        if ship().status.starting_hyperspace:
            return

        for i in range(5):
            new = get_destination_offset()
            if new:
                off = new
                break
            sleep(0.25)
        if not off:
            return


if __name__ == '__main__':
    sleep(5)
    align()
