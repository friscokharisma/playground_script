import pytest
import requests
import random
from openpyxl import Workbook
import datetime
import time
import inspect

# base_url = 'http://127.0.0.1:5000'
base_url = 'https://frisco-playground.up.railway.app'

# openpyxl initiation
workbook = Workbook()
sheet = workbook.active

sheet.title = "Test Result"

# ---------------------------------------------
# ctime = datetime.datetime.now()
# sheet.title = f"Test Report {ctime}"

sheet['A1'] = "No"
sheet['B1'] = "Test Case"
sheet['C1'] = "Data Test"
sheet['D1'] = "Status"
sheet['E1'] = "Execution time"
sheet['F1'] = "Time"
# ---------------------------------------------

test_results = {}

@pytest.fixture(scope="session", autouse=True)
def write_result_excel():
    num = 0
    yield
    for test_name, result in test_results.items():
        num+=1
        sheet.append([num, test_name, result['test_data'], result['result'], result['execution_time'], result['current_time']]) 
    workbook.save('TEST.xlsx')

new_id = None
same_random_value = None
update_value = None

def get_number():
    # global list_number
    list_number = []
    get_list = requests.get(f'{base_url}/items')
    response = get_list.json()
    for item in response['items']:
        number_string = item['name'].split()[-1]
        list_number.append(number_string)

    return list_number

def compare_number(random_value):
    list_number = get_number()
    while True:
        random_value = random.randint(0,100)
        if str(random_value) not in list_number:
            return random_value

def get_result(assert_message, message):
    if assert_message in message:
        result = "PASS"
    else:
        result = "FAIL"

    return result

def process_func_name(input_string):
    words = input_string.replace('_', ' ').split()
    remaining_words = words[1:] if len(words) > 1 else []
    processed_string = ' '.join(remaining_words)
    return processed_string

# def create_item(name, description):
#     return requests.post(f'{base_url}/create_item', name, description)

# def update_item(id, name, description):
#     return requests.put(f'{base_url}/update_item', id, name, description)

# ---------------------------------------------------------------------------
@pytest.mark.repeat(3)
def test_create_item_with_correct_value_of_request():
    global new_id
    global same_random_value

    random_number = random.randint(0, 100)
    random_value = compare_number(random_number)

    json_data = {"name": f"TESTING {random_value}","description": "Description testing"}

    same_random_value = random_value
    create_item = requests.post(f'{base_url}/create_item', json=json_data)

    start_time = time.time()
    response = create_item.json()
    end_time = time.time()
    duration = round(end_time - start_time, 4)
    # print(response)
    message = response['message']
    assert_message = 'Item created'
    current_time = datetime.datetime.now()

    new_id = response['item']['id']

    assert assert_message in message, "Message does not contain 'item created'"

    func_name = inspect.currentframe().f_code.co_name
    function_name = process_func_name(func_name)
    test_results[function_name] = {"result": get_result(assert_message, message), "test_data": str(json_data), "test_data": str(json_data), "execution_time": duration, "current_time": current_time}

# def test_create_item_fail():
#     random_number = random.randint(0, 100)
#     random_value = compare_number(random_number)
#     json_data = {"name": f"TESTING {random_value}","description": "X"}

#     create_item = requests.post(f'{base_url}/create_item', json=json_data)

#     start_time = time.time()
#     response = create_item.json()
#     end_time = time.time()
#     duration = round(end_time - start_time, 4)
#     # print(response)
#     message = response['message']
#     assert_message = 'Item created'
#     current_time = datetime.datetime.now()

#     assert assert_message in message, "Message does not contain 'item created'"

#     func_name = inspect.currentframe().f_code.co_name
#     function_name = process_func_name(func_name)
#     test_results[function_name] = {"result": get_result(assert_message, message), "test_data": str(json_data), "test_data": str(json_data), "execution_time": duration, "current_time": current_time}

def test_create_item_with_already_exist_value_of_requests():
    json_data = {"name": f"TESTING {same_random_value}","description": "Description testing"}

    create_item = requests.post(f'{base_url}/create_item', json=json_data)
    
    start_time = time.time()
    response = create_item.json()
    end_time = time.time()
    duration = round(end_time - start_time, 4)

    message = response['error']
    assert_message = 'already exist'
    current_time = datetime.datetime.now()

    assert assert_message in message, "Message does not contain 'already exist'"

    func_name = inspect.currentframe().f_code.co_name
    function_name = process_func_name(func_name)
    test_results[function_name] = {"result": get_result(assert_message, message), "test_data": str(json_data), "execution_time": duration, "current_time": current_time}

def test_create_item_with_invalid_value_of_name():
    random_number = random.randint(0,100)
    random_value = compare_number(random_number)
    json_data = {"name": f"TESTING! {random_value}","description": "Description testing"}

    create_item = requests.post(f'{base_url}/create_item', json=json_data)
    
    start_time = time.time()
    response = create_item.json()
    end_time = time.time()
    duration = round(end_time - start_time, 4)

    message = response['error']
    assert_message = 'Name must contain only letters, numbers and spaces'
    current_time = datetime.datetime.now()

    assert assert_message in message, "Message does not contain 'Name must contain only letters, numbers and spaces'"

    func_name = inspect.currentframe().f_code.co_name
    function_name = process_func_name(func_name)
    test_results[function_name] = {"result": get_result(assert_message, message), "test_data": str(json_data), "execution_time": duration, "current_time": current_time}

def test_create_item_with_value_of_name_length_less_than_3():
    json_data = {"name": f"X","description": "Description testing"}

    create_item = requests.post(f'{base_url}/create_item', json=json_data)
    
    start_time = time.time()
    response = create_item.json()
    end_time = time.time()
    duration = round(end_time - start_time, 4)

    message = response['error']
    assert_message = 'Name must be at least 3 characters long'
    current_time = datetime.datetime.now()

    assert assert_message in message, "Message does not contain 'Name must be at least 3 characters long'"

    func_name = inspect.currentframe().f_code.co_name
    function_name = process_func_name(func_name)
    test_results[function_name] = {"result": get_result(assert_message, message), "test_data": str(json_data), "execution_time": duration, "current_time": current_time}

def test_create_item_with_value_of_name_length_more_than_100():
    json_data = {"name": f"This is a test for checking max value length of this field is it correct the maximum value is one hundred","description": "Description testing"}

    create_item = requests.post(f'{base_url}/create_item', json=json_data)
    
    start_time = time.time()
    response = create_item.json()
    end_time = time.time()
    duration = round(end_time - start_time, 4)

    message = response['error']
    assert_message = 'Name must not exceed 100 characters long'
    current_time = datetime.datetime.now()

    assert assert_message in message, "Message does not contain 'NName must not exceed 100 characters long'"

    func_name = inspect.currentframe().f_code.co_name
    function_name = process_func_name(func_name)
    test_results[function_name] = {"result": get_result(assert_message, message), "test_data": str(json_data), "execution_time": duration, "current_time": current_time}

def test_create_item_with_empty_value_of_name():
    json_data = {"name": "","description": "Description testing"}

    create_item = requests.post(f'{base_url}/create_item', json=json_data)
    
    start_time = time.time()
    response = create_item.json()
    end_time = time.time()
    duration = round(end_time - start_time, 4)

    message = response['error']
    assert_message = 'Name is required'
    current_time = datetime.datetime.now()

    assert assert_message in message, "Message does not contain 'Name is required'"

    func_name = inspect.currentframe().f_code.co_name
    function_name = process_func_name(func_name)
    test_results[function_name] = {"result": get_result(assert_message, message), "test_data": str(json_data), "execution_time": duration, "current_time": current_time}

def test_create_item_with_invalid_value_of_description():
    random_number = random.randint(0,100)
    random_value = compare_number(random_number)
    json_data = {"name": f"TESTING {random_value}","description": "Description testing!"}

    create_item = requests.post(f'{base_url}/create_item', json=json_data)

    start_time = time.time()
    response = create_item.json()
    end_time = time.time()
    duration = round(end_time - start_time, 4)

    message = response['error']
    assert_message = 'Description must contain only letters, numbers and spaces'
    current_time = datetime.datetime.now()

    assert assert_message in message, "Message does not contain 'Description must contain only letters, numbers and spaces'"

    func_name = inspect.currentframe().f_code.co_name
    function_name = process_func_name(func_name)
    test_results[function_name] = {"result": get_result(assert_message, message), "test_data": str(json_data), "execution_time": duration, "current_time": current_time}

def test_create_item_with_value_of_description_length_less_than_3():
    random_number = random.randint(0,100)
    random_value = compare_number(random_number)
    json_data = {"name": f"TESTING {random_value}","description": "X"}

    create_item = requests.post(f'{base_url}/create_item', json=json_data)
    
    start_time = time.time()
    response = create_item.json()
    end_time = time.time()
    duration = round(end_time - start_time, 4)

    message = response['error']
    assert_message = 'Description must be at least 3 characters long'
    current_time = datetime.datetime.now()

    assert assert_message in message, "Message does not contain 'Description must be at least 3 characters long'"

    func_name = inspect.currentframe().f_code.co_name
    function_name = process_func_name(func_name)
    test_results[function_name] = {"result": get_result(assert_message, message), "test_data": str(json_data), "execution_time": duration, "current_time": current_time}

def test_create_item_with_value_of_description_length_more_than_100():
    random_number = random.randint(0,100)
    random_value = compare_number(random_number)
    json_data = {"name": f"TESTING {random_value}","description": "This is a test for checking max value length of this field is it correct the maximum value is one hundred"}

    create_item = requests.post(f'{base_url}/create_item', json=json_data)
    
    start_time = time.time()
    response = create_item.json()
    end_time = time.time()
    duration = round(end_time - start_time, 4)

    message = response['error']
    assert_message = 'Description must not exceed 100 characters long'
    current_time = datetime.datetime.now()

    assert assert_message in message, "Message does not contain 'Description must not exceed 100 characters long'"

    func_name = inspect.currentframe().f_code.co_name
    function_name = process_func_name(func_name)
    test_results[function_name] = {"result": get_result(assert_message, message), "test_data": str(json_data), "execution_time": duration, "current_time": current_time}

def test_create_item_with_empty_value_of_description():
    random_number = random.randint(0,100)
    random_value = compare_number(random_number)
    json_data = {"name": f"TESTING {random_value}","description": ""}

    create_item = requests.post(f'{base_url}/create_item', json=json_data)
    
    start_time = time.time()
    response = create_item.json()
    end_time = time.time()
    duration = round(end_time - start_time, 4)

    message = response['error']
    assert_message = 'Description is required'
    current_time = datetime.datetime.now()

    assert assert_message in message, "Message does not contain 'Description is required'"

    func_name = inspect.currentframe().f_code.co_name
    function_name = process_func_name(func_name)
    test_results[function_name] = {"result": get_result(assert_message, message), "test_data": str(json_data), "execution_time": duration, "current_time": current_time}

def test_update_item_with_correct_value_of_request():
    global update_value
    random_number = random.randint(0,100)
    random_value = compare_number(random_number)
    update_value = random_value
    json_data = {"name": f"TESTING {random_value}","description": "Description testing"}

    update_item = requests.put(f'{base_url}/update_item/{new_id}', json=json_data)
    
    start_time = time.time()
    response = update_item.json()
    end_time = time.time()
    duration = round(end_time - start_time, 4)

    message = response['message']
    assert_message = 'Item updated'
    current_time = datetime.datetime.now()

    assert assert_message in message, "Message does not contain 'Item updated'"

    func_name = inspect.currentframe().f_code.co_name
    function_name = process_func_name(func_name)
    test_results[function_name] = {"result": get_result(assert_message, message), "test_data": str(json_data), "execution_time": duration, "current_time": current_time}

def test_update_item_with_already_exist_value_of_requests():
    json_data = {"name": f"TESTING {update_value}","description": "Description testing"}

    update_item = requests.put(f'{base_url}/update_item/{new_id}', json=json_data)
    
    start_time = time.time()
    response = update_item.json()
    end_time = time.time()
    duration = round(end_time - start_time, 4)

    message = response['error']
    assert_message = 'already exist'
    current_time = datetime.datetime.now()

    assert assert_message in message, "Message does not contain 'already exist'"

    func_name = inspect.currentframe().f_code.co_name
    function_name = process_func_name(func_name)
    test_results[function_name] = {"result": get_result(assert_message, message), "test_data": str(json_data), "execution_time": duration, "current_time": current_time}

def test_update_item_with_invalid_value_of_name():
    random_number = random.randint(0,100)
    random_value = compare_number(random_number)
    json_data = {"name": f"TESTING! {random_value}","description": "Description testing"}

    update_item = requests.put(f'{base_url}/update_item/{new_id}', json=json_data)
    
    start_time = time.time()
    response = update_item.json()
    end_time = time.time()
    duration = round(end_time - start_time, 4)

    message = response['error']
    assert_message = 'Name must contain only letters, numbers and spaces'
    current_time = datetime.datetime.now()

    assert assert_message in message, "Message does not contain 'Name must contain only letters, numbers and spaces'"

    func_name = inspect.currentframe().f_code.co_name
    function_name = process_func_name(func_name)
    test_results[function_name] = {"result": get_result(assert_message, message), "test_data": str(json_data), "execution_time": duration, "current_time": current_time}

def test_update_item_with_value_of_name_length_less_than_3():
    json_data = {"name": f"X","description": "Description testing"}

    update_item = requests.put(f'{base_url}/update_item/{new_id}', json=json_data)
    
    start_time = time.time()
    response = update_item.json()
    end_time = time.time()
    duration = round(end_time - start_time, 4)

    message = response['error']
    assert_message = 'Name must be at least 3 characters long'
    current_time = datetime.datetime.now()

    assert assert_message in message, "Message does not contain 'Name must be at least 3 characters long'"

    func_name = inspect.currentframe().f_code.co_name
    function_name = process_func_name(func_name)
    test_results[function_name] = {"result": get_result(assert_message, message), "test_data": str(json_data), "execution_time": duration, "current_time": current_time}

def test_update_item_with_value_of_name_length_more_than_100():
    json_data = {"name": f"This is a test for checking max value length of this field is it correct the maximum value is one hundred","description": "Description testing"}

    update_item = requests.put(f'{base_url}/update_item/{new_id}', json=json_data)
    
    start_time = time.time()
    response = update_item.json()
    end_time = time.time()
    duration = round(end_time - start_time, 4)

    message = response['error']
    assert_message = 'Name must not exceed 100 characters long'
    current_time = datetime.datetime.now()

    assert assert_message in message, "Message does not contain 'Name must not exceed 100 characters long'"

    func_name = inspect.currentframe().f_code.co_name
    function_name = process_func_name(func_name)
    test_results[function_name] = {"result": get_result(assert_message, message), "test_data": str(json_data), "execution_time": duration, "current_time": current_time}

def test_update_item_with_empty_value_of_name():
    json_data = {"name": "","description": "Description testing"}

    update_item = requests.put(f'{base_url}/update_item/{new_id}', json=json_data)
    
    start_time = time.time()
    response = update_item.json()
    end_time = time.time()
    duration = round(end_time - start_time, 4)

    message = response['error']
    assert_message = 'Name is required'
    current_time = datetime.datetime.now()

    assert assert_message in message, "Message does not contain 'Name is required'"

    func_name = inspect.currentframe().f_code.co_name
    function_name = process_func_name(func_name)
    test_results[function_name] = {"result": get_result(assert_message, message), "test_data": str(json_data), "execution_time": duration, "current_time": current_time}

def test_update_item_with_invalid_value_of_description():
    random_number = random.randint(0,100)
    random_value = compare_number(random_number)
    json_data = {"name": f"TESTING {random_value}","description": "Description testing!"}

    update_item = requests.put(f'{base_url}/update_item/{new_id}', json=json_data)
    
    start_time = time.time()
    response = update_item.json()
    end_time = time.time()
    duration = round(end_time - start_time, 4)

    message = response['error']
    assert_message = 'Description must contain only letters, numbers and spaces'
    current_time = datetime.datetime.now()

    assert assert_message in message, "Message does not contain 'Description must contain only letters, numbers and spaces'"

    func_name = inspect.currentframe().f_code.co_name
    function_name = process_func_name(func_name)
    test_results[function_name] = {"result": get_result(assert_message, message), "test_data": str(json_data), "execution_time": duration, "current_time": current_time}

def test_update_item_with_value_of_description_length_less_than_3():
    random_number = random.randint(0,100)
    random_value = compare_number(random_number)
    json_data = {"name": f"TESTING {random_value}","description": "X"}

    update_item = requests.put(f'{base_url}/update_item/{new_id}', json=json_data)
    
    start_time = time.time()
    response = update_item.json()
    end_time = time.time()
    duration = round(end_time - start_time, 4)

    message = response['error']
    assert_message = 'Description must be at least 3 characters long'
    current_time = datetime.datetime.now()

    assert assert_message in message, "Message does not contain 'Description must be at least 3 characters long'"

    func_name = inspect.currentframe().f_code.co_name
    function_name = process_func_name(func_name)
    test_results[function_name] = {"result": get_result(assert_message, message), "test_data": str(json_data), "execution_time": duration, "current_time": current_time}

def test_update_item_with_value_of_description_length_more_than_100():
    random_number = random.randint(0,100)
    random_value = compare_number(random_number)
    json_data = {"name": f"TESTING {random_value}", "description": "This is a test for checking max value length of this field is it correct the maximum value is one hundred"}

    update_item = requests.put(f'{base_url}/update_item/{new_id}', json=json_data)
    
    start_time = time.time()
    response = update_item.json()
    end_time = time.time()
    duration = round(end_time - start_time, 4)

    message = response['error']
    assert_message = 'Description must not exceed 100 characters long'
    current_time = datetime.datetime.now()

    assert assert_message in message, "Message does not contain 'Description must not exceed 100 characters long'"

    func_name = inspect.currentframe().f_code.co_name
    function_name = process_func_name(func_name)
    test_results[function_name] = {"result": get_result(assert_message, message), "test_data": str(json_data), "execution_time": duration, "current_time": current_time}

def test_update_item_with_empty_value_of_description():
    random_number = random.randint(0,100)
    random_value = compare_number(random_number)
    json_data = {"name": f"TESTING {random_value}","description": ""}

    update_item = requests.put(f'{base_url}/update_item/{new_id}', json=json_data)
    
    start_time = time.time()
    response = update_item.json()
    end_time = time.time()
    duration = round(end_time - start_time, 4)

    message = response['error']
    assert_message = 'Description is required'
    current_time = datetime.datetime.now()

    assert assert_message in message, "Message does not contain 'Description is required'"

    func_name = inspect.currentframe().f_code.co_name
    function_name = process_func_name(func_name)
    test_results[function_name] = {"result": get_result(assert_message, message), "test_data": str(json_data), "execution_time": duration, "current_time": current_time}

def test_get_list_all():
    get_list_all = requests.get(f'{base_url}/items')
    
    start_time = time.time()
    response = get_list_all.json()
    end_time = time.time()
    duration = round(end_time - start_time, 4)

    assert_message = 'items'
    current_time = datetime.datetime.now()

    assert assert_message in response, "Data is empty"

    func_name = inspect.currentframe().f_code.co_name
    function_name = process_func_name(func_name)
    test_results[function_name] = {"result": get_result(assert_message, response),"test_data": " ", "execution_time": duration, "current_time": current_time}

def test_get_detail_item_with_correct_id():
    get_detail_item = requests.get(f'{base_url}/item/{new_id}')
    
    start_time = time.time()
    response = get_detail_item.json()
    end_time = time.time()
    duration = round(end_time - start_time, 4)

    message = response['item']
    assert_message = 'id'
    current_time = datetime.datetime.now()

    assert 'id' in message, "Id item not found"
    assert 'name' in message, "Id item not found"
    assert 'description' in message, "Id item not found"

    func_name = inspect.currentframe().f_code.co_name
    function_name = process_func_name(func_name)
    test_results[function_name] = {"result": get_result(assert_message, message),"test_data": f"id : {new_id}", "execution_time": duration, "current_time": current_time}

def test_get_detail_item_with_id_not_exist():
    get_detail_item = requests.get(f'{base_url}/item/100')
    
    start_time = time.time()
    response = get_detail_item.json()
    end_time = time.time()
    duration = round(end_time - start_time, 4)

    message = response['error']
    assert_message = 'Item not found'
    current_time = datetime.datetime.now()

    assert assert_message in message, "Id item found"

    func_name = inspect.currentframe().f_code.co_name
    function_name = process_func_name(func_name)
    test_results[function_name] = {"result": get_result(assert_message, message),"test_data": "id : 100", "execution_time": duration, "current_time": current_time}

def test_delete_item_with_correct_id():
    delete_item = requests.delete(f'{base_url}/delete_item/{new_id}')
    
    start_time = time.time()
    response = delete_item.json()
    end_time = time.time()
    duration = round(end_time - start_time, 4)

    message = response['message']
    assert_message = f'has been successfully deleted'
    current_time = datetime.datetime.now()

    assert assert_message in message, "Failed to delete item"

    func_name = inspect.currentframe().f_code.co_name
    function_name = process_func_name(func_name)
    test_results[function_name] = {"result": get_result(assert_message, message),"test_data": f"id : {new_id}", "execution_time": duration, "current_time": current_time}

def test_delete_item_with_id_already_deleted():
    delete_item = requests.delete(f'{base_url}/delete_item/{new_id}')
    
    start_time = time.time()
    response = delete_item.json()
    end_time = time.time()
    duration = round(end_time - start_time, 4)

    message = response['error']
    assert_message = f'Item not found'
    current_time = datetime.datetime.now()

    assert assert_message in message, "Failed to delete item"

    func_name = inspect.currentframe().f_code.co_name
    function_name = process_func_name(func_name)
    test_results[function_name] = {"result": get_result(assert_message, message),"test_data": f"id : {new_id}", "execution_time": duration, "current_time": current_time}

def test_delete_item_with_id_not_exist():
    delete_item = requests.delete(f'{base_url}/delete_item/100')
    
    start_time = time.time()
    response = delete_item.json()
    end_time = time.time()
    duration = round(end_time - start_time, 4)

    message = response['error']
    assert_message = f'Item not found'
    current_time = datetime.datetime.now()
   
    assert assert_message in message, "Failed to delete item"

    func_name = inspect.currentframe().f_code.co_name
    function_name = process_func_name(func_name)
    test_results[function_name] = {"result": get_result(assert_message, message),"test_data": "id : 100", "execution_time": duration, "current_time": current_time}

def test_delete_all_items():
    delete_all_item = requests.post(f'{base_url}/delete_all')
    
    start_time = time.time()
    response = delete_all_item.json()
    end_time = time.time()
    duration = round(end_time - start_time, 4)

    message = response['message']
    assert_message = f'All data has been deleted'
    current_time = datetime.datetime.now()
    
    assert assert_message in message, "Failed to delete all item"

    func_name = inspect.currentframe().f_code.co_name
    function_name = process_func_name(func_name)
    test_results[function_name] = {"result": get_result(assert_message, message),"test_data": " ", "execution_time": duration, "current_time": current_time}

def test_delete_all_items_with_already_deleted():
    delete_all_item = requests.post(f'{base_url}/delete_all')
    
    start_time = time.time()
    response = delete_all_item.json()
    end_time = time.time()
    duration = round(end_time - start_time, 4)

    message = response['message']
    assert_message = f'No items to delete'
    current_time = datetime.datetime.now()

    assert assert_message in message, "Failed to delete all item"

    func_name = inspect.currentframe().f_code.co_name
    function_name = process_func_name(func_name)
    test_results[function_name] = {"result": get_result(assert_message, message),"test_data": " ", "execution_time": duration, "current_time": current_time}