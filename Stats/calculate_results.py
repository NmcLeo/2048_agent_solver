import re
import matplotlib.pyplot as plt

p = '[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+'

numbers = []
max_reached = []
total_moves = []
time = []

with open('output_minimax_pruning_3.txt') as f:
    lines = f.readlines()

for line in lines:
    if re.search(p, str(line)) is not None:
        for catch in re.finditer(p, line):
            numbers.append(catch[0])

tile_stats = {
    "64": {"num_times": 0, "total_time": 0, "avg_time": 0, "min_time": 9999999, "max_time": 0, "total_steps": 0,
            "min_steps": 9999999,
            "avg_steps": 0, "max_steps": 0, "associated_times": [], "associated_steps": []},
    "128": {"num_times": 0, "total_time": 0, "avg_time": 0, "min_time": 9999999, "max_time": 0, "total_steps": 0,
            "min_steps": 9999999,
            "avg_steps": 0, "max_steps": 0, "associated_times": [], "associated_steps": []},
    "256": {"num_times": 0, "total_time": 0, "avg_time": 0, "min_time": 9999999, "max_time": 0, "total_steps": 0,
            "min_steps": 9999999,
            "avg_steps": 0, "max_steps": 0, "associated_times": [], "associated_steps": []},
    "512": {"num_times": 0, "total_time": 0, "avg_time": 0, "min_time": 9999999, "max_time": 0, "total_steps": 0,
            "avg_steps": 0, "min_steps": 9999999,
            "max_steps": 0, "associated_times": [], "associated_steps": []},
    "1024": {"num_times": 0, "total_time": 0, "avg_time": 0, "min_time": 9999999, "max_time": 0, "total_steps": 0,
             "avg_steps": 0, "min_steps": 9999999, "max_steps": 0, "associated_times": [], "associated_steps": []},
    "2048": {"num_times": 0, "total_time": 0, "avg_time": 0, "min_time": 9999999, "max_time": 0, "total_steps": 0,
             "avg_steps": 0, "min_steps": 9999999, "max_steps": 0, "associated_times": [], "associated_steps": []},
    "4096": {"num_times": 0, "total_time": 0, "avg_time": 0, "min_time": 9999999, "max_time": 0, "total_steps": 0,
             "avg_steps": 0, "min_steps": 9999999, "max_steps": 0, "associated_times": [], "associated_steps": []}}

for i in range(0, len(numbers) - 2, 3):
    tile_stats[numbers[i]]["num_times"] += 1

    tile_stats[numbers[i]]["total_time"] += float(numbers[i + 2])
    if float(numbers[i + 2]) < tile_stats[numbers[i]]["min_time"]:
        tile_stats[numbers[i]]["min_time"] = float(numbers[i + 2])
    if float(numbers[i + 2]) > tile_stats[numbers[i]]["max_time"]:
        tile_stats[numbers[i]]["max_time"] = float(numbers[i + 2])
    tile_stats[numbers[i]]["associated_times"].append(float(numbers[i + 2]))

    tile_stats[numbers[i]]["total_steps"] += int(numbers[i + 1])
    if int(numbers[i + 1]) < tile_stats[numbers[i]]["min_steps"]:
        tile_stats[numbers[i]]["min_steps"] = int(numbers[i + 1])
    if int(numbers[i + 1]) > tile_stats[numbers[i]]["max_steps"]:
        tile_stats[numbers[i]]["max_steps"] = int(numbers[i + 1])
    tile_stats[numbers[i]]["associated_steps"].append(int(numbers[i + 1]))

for hash1 in tile_stats:
    if tile_stats[hash1]["num_times"] != 0:
        tile_stats[hash1]["avg_time"] = tile_stats[hash1]["total_time"]/tile_stats[hash1]["num_times"]
        tile_stats[hash1]["avg_steps"] = tile_stats[hash1]["total_steps"] / tile_stats[hash1]["num_times"]
    else:
        tile_stats[hash1]["max_steps"] = None
        tile_stats[hash1]["min_steps"] = None
        tile_stats[hash1]["max_time"] = None
        tile_stats[hash1]["min_time"] = None

for hash1 in tile_stats:
    print(hash1 + ": " + str(tile_stats[hash1]["avg_steps"]))
# for hash1 in tile_stats:
#     print("\n\n")
#     print(hash1)
#     for hash2 in tile_stats[hash1]:
#         if hash2 != "associated_times" and hash2 != "associated_steps":
#             print(hash2 + ": " + str(tile_stats[hash1][hash2]))




# indexes = []
# for hash1 in tile_stats:
#     if tile_stats[hash1]["min_steps"]==None:
#         continue
#
#     plt.bar(indexes, tile_stats[hash1]["associated_steps"])
#     plt.xlim([0, len(indexes)+1])
#     plt.ylim(tile_stats[hash1]["min_steps"]-50, tile_stats[hash1]["max_steps"]+50)
#     plt.ylabel('Number of Steps')
#     plt.title("Steps Graph For " + hash1)
#     plt.show()
#
# x_axis = [hash1 for hash1 in tile_stats]
# y_axis = [tile_stats[hash1]["num_times"] for hash1 in tile_stats]
#
# for hash1 in tile_stats:
#     x_axis.append(hash1)
#     y_axis.append(tile_stats[hash1]["num_times"])
# plt.bar(x_axis, y_axis)
# plt.show()

# for hash1 in tile_stats:
#     if tile_stats[hash1]["min_steps"]==None:
#         continue
#     indexes = [int(i+1) for i in range(len(tile_stats[hash1]["associated_times"]))]
#     plt.plot(indexes, tile_stats[hash1]["associated_times"], 'ro')
#     plt.xlim([0, len(indexes)+1])
#     plt.ylim(int(tile_stats[hash1]["min_time"])-2, int(tile_stats[hash1]["max_time"])+2)
#     plt.ylabel('Time to Complete')
#     plt.title("Time Graph For " + hash1)
#     plt.show()