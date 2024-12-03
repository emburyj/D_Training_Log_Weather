import zmq
import datetime
import time

def get_snapshot(data):
    activities = 0
    distance = 0
    time = 0
    elevation_gain = 0
    for activity in data:
        activity_date = datetime.datetime.strptime(activity['date'], '%Y-%m-%d').date()
        week_check = is_in_current_week(activity_date)
        if week_check:
            activities += 1
            distance += activity['distance']
            time += activity['duration']
            elevation_gain += activity['elevation']

    return {'activities': activities, 'distance': distance, 'duration': time, 'elevation': elevation_gain}

def is_in_current_week(date):
    today = datetime.date.today()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    end_of_week = start_of_week + datetime.timedelta(days=6)

    return start_of_week <= date <= end_of_week

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5558")

    print("Listening for requests...")
    while True:
        request = socket.recv_json()
        stats = get_snapshot(request['data'])
        print("Retrieving snapshot stats...")
        socket.send_json(stats)

if __name__ == '__main__':
    main()
