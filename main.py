from datetime import datetime
from pathlib import Path
from collections import Counter

LOG_FILE = Path('application.log')

def read_logs(file_path):
    records = []

    with file_path.open('r', encoding='utf-8') as file:
        for line in file:
            record = parse_line(line)

            if record is not None:
                records.append(record)
    return records


def parse_line(line):
    parts = line.split()

    if (len(parts) != 5):
        return None

    timestamp = parts[0] + " " + parts[1]
    method = parts[2]
    path = parts[3]
    status = parts[4]

    return {
        'timestamp': timestamp,
        'method': method,
        'path': path,
        'status': status
    }

def analyze_endpoints(records):
    endpoint_counter = Counter()

    for record in records:
        method = record['method']
        path = record['path']

        endpoint = (method, path)

        endpoint_counter[endpoint] += 1

    print(endpoint_counter)
    return endpoint_counter

def analyze_endpoint_by_status(records):
    endpoint_counter_by_status = {}

    for record in records:
        method = record['method']
        path = record['path']
        status = int(record['status'])

        endpoint = (method, path)

        if endpoint not in endpoint_counter_by_status:
            endpoint_counter_by_status[endpoint] = {
                "success": 0,
                "redirect": 0,
                "error": 0,
            }

        if 200 <= status < 300:
            endpoint_counter_by_status[endpoint]["success"] += 1
        if 300 <= status < 400:
            endpoint_counter_by_status[endpoint]["redirect"] += 1
        if 400 <= status < 600:
            endpoint_counter_by_status[endpoint]["error"] += 1

    print(endpoint_counter_by_status)
    return endpoint_counter_by_status

def analyze_endpoint_by_hour(records):
    endpoint_counter_by_hour = Counter()

    for record in records:
        method = record['method']
        path = record['path']
        timestamp = datetime.strptime(record['timestamp'], '%Y-%m-%d %H:%M:%S')

        hour = timestamp.replace(minute=0, second=0)

        endpoint = (hour, method, path)

        endpoint_counter_by_hour[endpoint] += 1

    print(endpoint_counter_by_hour)

    return endpoint_counter_by_hour


def main():
    records = read_logs(LOG_FILE)

    # for record in records:
    #     timestamp = datetime.strptime(record['timestamp'], '%Y-%m-%d %H:%M:%S')
    #     timestamps.append(timestamp)

    endpoint_counter = analyze_endpoint_by_hour(records)

    print("Статистика по endpoint-ам")

    for (hour, method, path), count in endpoint_counter.items():
        average_rps = count / 3600

        print(f"{hour} for {method} and {path}: {average_rps}")


if __name__ == '__main__':
    main()


# 2026-10-19 12:00:02 POST /api/order 201
# 2026-10-19 12:00:02
# POST

# list -> dict -> {
#     timestamp: ....
#     method: ....
#     path: ....
#     status:
# }


# {
#     "success":....(200-300)
#     "redirect":...(300-400)
#     "error":(400-600)
# }