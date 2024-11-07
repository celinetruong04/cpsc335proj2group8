import json

# Checks if the string is a valid time in HH:MM format
# input: string
# output: boolean
def valid_time(time_str):
    # checks if the length is 5 or 4
    if len(time_str) not in {5, 4}:
        return False
    # if the format is HH:MM or H:MM, the ':' should be in the right place
    if len(time_str) == 5 and time_str[2] != ':' or len(time_str) == 4 and time_str[1] != ':':
        return False
    
    time_hr = time_str.split(':')[0]
    time_min = time_str.split(':')[1]
    return 0 <= int(time_hr) < 24 and 0 <= int(time_min) < 60

# Interval function that returns the time interval in minutes
# Input: 2 strings
# Output: int
def interval(time1, time2):
    # Checks if the inputs are valid
    if not valid_time(time1) or not valid_time(time2):
        print("Interval Error")
        return None
    else:
        partsA = time1.split(':')
        partsB = time2.split(':')

        minA = int(partsA[0]) * 60 + int(partsA[1])
        minB = int(partsB[0]) * 60 + int(partsB[1])
        return minB - minA

# Function to calculate free intervals within the daily active period
# Input: 2 lists, int
# output: list
def get_free_intervals(busy_schedule, daily_active, duration):
    login, logout = daily_active
    free_intervals = []

    #Starting free interval from login to the first busy period
    if interval(login, busy_schedule[0][0]) >= duration:
        free_intervals.append([login, busy_schedule[0][0]])

    # Intermediate free intervals between busy times
    for i in range(len(busy_schedule) - 1):
        start, end = busy_schedule[i][1], busy_schedule[i + 1][0]
        if interval(start, end) >= duration:
            free_intervals.append([start, end])

    # Ending free interval from the last busy period to logout
    if interval(busy_schedule[-1][1], logout) >=  duration:
        free_intervals.append([busy_schedule[-1][1], logout])

    return free_intervals

# Helper to convert time in 'HH:MM' format to minutes
# Inputs: string HH:MM or H:MM
# Outputs: int
def time_to_minutes(t):
    h, m= map(int, t.split(':'))
    return h * 60 + m

# Helper to convert minutes to 'HH:MM' format
# Inputs: int
# Outputs: string "H:MM" or "HH:MM"
def minutes_to_time(minutes):
    return f"{minutes // 60}:{minutes % 60:02}"

# Function to find the common free intervals
def group_schedule(p1_s, p1_d, p2_s, p2_d, time):
    # Edge Case 1: Check if all time lists exist
    if not p1_s or not p1_d or not p2_s or not p2_d:
        return ["Edge Case 1"]
    
    # Edge Case 2: Check if the duration is valid
    if time < 1: return ["Edge Case 2"]

    # Edge Case 3: Validate each person's busy schedule intervals
    for time1, time2 in p1_s:
        if interval(time1, time2) < 0:
            return["Edge Case 3 - Schedule 1"]
    
    for time1, time2 in p2_s:
        if interval(time1, time2) < 0:
            return ["Edge Case 3 - Schedule 2"]

    # Edge Case 4: Validate working period intervals
    if interval (p1_d[0], p1_d[1]) < 0 or interval(p2_d[0], p2_d[1]) < 0:
        return ["Edge Case 4"]

    # Calculate free intervals within daily activity periods
    p1_free = get_free_intervals(p1_s, p1_d, time)
    p2_free = get_free_intervals(p2_s, p2_d, time)

    # Find common free intervals using two pointers
    common_free = []
    p1_pointer, p2_pointer = 0, 0

    # Loop runs until either pointer ends
    while p1_pointer < len(p1_free) and p2_pointer < len(p2_free):
        #Get the overlapping interval
        start = max(time_to_minutes(p1_free[p1_pointer][0]), time_to_minutes(p2_free[p2_pointer][0]))
        end = min(time_to_minutes(p1_free[p1_pointer][1]), time_to_minutes(p2_free[p2_pointer][1]))

        # Check if this interval meets the duration requirement
        if end - start >= time:
            # If the last common_free interval overlaps or touches this one, merge them
            if common_free and time_to_minutes(common_free[-1][1]) >= start:
                common_free[-1][1] = minutes_to_time(max(end, time_to_minutes(common_free[-1][1])))
            else:
                common_free.append([minutes_to_time(start), minutes_to_time(end)])

        # Move the pointer of the interval that finishes first
        if time_to_minutes(p1_free[p1_pointer][1]) < time_to_minutes(p2_free[p2_pointer][1]):
            p1_pointer += 1
        else:
            p2_pointer += 1
            
    return common_free

    # Main function for testing
def main():
    # Reads test cases from testcase.txt
    with open('testcase.txt', 'r') as file:
        data = json.load(file)
    
    # Open output.txt file in write mode
    with open('output.txt', 'w') as output_file:
        # Loop through all test cases
        for test_num, test_case in enumerate(data['test_cases']):
            output_file.write(f"Running Test Case {test_num + 1}...\n")

            # Extract elements for test case
            p1_schedule = test_case['p1_schedule']
            p1_daily = test_case['p1_daily']
            p2_schedule = test_case['p2_schedule']
            p2_daily = test_case['p2_daily']
            duration = test_case['duration']

            # Check the available meeting times using the group_schedule function
            avl_time = group_schedule(p1_schedule, p1_daily, p2_schedule, p2_daily, duration)

            # Extract expected result from the test case
            expected = test_case['expected']

            # Compare the actual result with the expected result and write the outcome to output.txt
            if avl_time == expected:
                output_file.write(f"Test Case {test_num + 1} passed\n")
            else:
                output_file.write(f"Test Case {test_num + 1} failed\n")
                output_file.write(f"Actual: {avl_time}\n")
                output_file.write(f"Expected: {expected}\n")
            
            output_file.write('-' * 50 + "\n")  # Separator for readability

    return 0

if __name__ == "__main__":
    main()
