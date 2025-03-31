def get_address_index(address_name, address_data):
    for row in address_data:
        if address_name in row[2]:
            return int(row[0])
    return None

def get_distance(index1, index2, distance_data):
    distance = distance_data[index1][index2]
    if distance == '':
        distance = distance_data[index2][index1]
    return float(distance)
