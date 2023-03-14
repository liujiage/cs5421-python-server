#!/usr/bin/env python
# coding: utf-8

# In[16]:


import json
import re

def json_xpath(json_data, xpath):
   
    
    try:
        data = json.loads(json_data)
    except ValueError:
        raise ValueError("Invalid JSON")
    
    # Split the XPath 
    tokens = xpath.split("/")
    
    for token in tokens:
        if token == "*":
            data = [v for k, v in data.items()] if isinstance(data, dict) else data
        
        #range support
        elif "#" in token:
            
            path, index = token.split("#")
            getByKey = json_xpath(json.dumps(data), path.strip())   
            if not ":" in token:
                index = int(index)
                data = getByKey[index] 
            else:
                if not isinstance(getByKey, list):
                    raise TypeError("range operator must work on lists")
                start, end = index.split(":")
                start = int(start) if start else 0
                end = int(end) if end else len(data)
                if end > len(data):
                    raise IndexError("index out of bounds")
                data = getByKey[start:end]
            
                
        
        # function support
        elif "(" in token and ")" in token:
            func_name, arg_expr = token.split("(")
            arg_expr = arg_expr[:-1]
            values = json_xpath(json.dumps(data), arg_expr.strip())    
            
            res = []
            for value in values:
                if func_name == "max":
                    try:
                        res.append(max(value));
                    except ValueError:
                        data = None
                elif func_name == "min":
                    try:
                        res.append(min(value));
                    except ValueError:
                        data = None
                else:
                    raise TypeError("Invalid function name")
            data = res                                

                
        elif "[" in token and "]" in token:
            
            path, remain = token.split("[")
            filter_expr = remain[:-1]
            withoutFilter = json_xpath(json.dumps(data), path.strip())
            filter_match = re.match(r'(.+)(==|!=|<|>|<=|>=)(.+)', filter_expr)
            if filter_match:
                key = filter_match.group(1)
                op = filter_match.group(2)
                value = filter_match.group(3)
                if value.isdigit():
                    value = int(value)  
                res = []
                for w in withoutFilter: 
                                  
                    if op == '==':
                        res.append([d for d in w if isinstance(d, dict) and d.get(key, None) == value])
                    elif op == '!=':
                        res.append([d for d in w if isinstance(d, dict) and d.get(key, None) != value])
                    elif op == '<':
                        res.append([d for d in w if isinstance(d, dict) and d.get(key, None) < value])
                    elif op == '>':
                        res.append([d for d in w if isinstance(d, dict) and d.get(key, None) > value])
                    elif op == '<=':
                        res.append([d for d in w if isinstance(d, dict) and d.get(key, None) <= value])
                    elif op == '>=':
                        res.append([d for d in w if isinstance(d, dict) and d.get(key, None) >= value])
                data = res
                                
            else:
                raise TypeError("wrong filter format")
            if not data:
                break
                
        
        else:
            if not isinstance(data, list):
                data = [data]             
            
            res = []
            for dd in data:
                if(isinstance(dd, list)):    
                    res.append([d.get(token, None) for d in dd if isinstance(d, dict)])
                else:
                    res.extend([dd.get(token, None) if isinstance(dd, dict) else None])                         
            data = res
                                      
        if data is None:
            break
    
    return data

# additional feature: and&, or|, count,







def main():

    # Test case 1: Key query
    json_data = '{"name": "Bre", "age": 25}'
    xpath = 'name'
    assert json_xpath(json_data, xpath) == ["Bre"]

    json_data = '[{"people": [{"name": "Bre", "age": 25}, {"name": "Stephane", "age": 30}]}, {"people": [{"name": "Bre1", "age": 26}, {"name": "Stephane1", "age": 31}]}]'
    xpath = 'people/name'
    assert json_xpath(json_data, xpath) == [['Bre', 'Stephane'], ['Bre1', 'Stephane1']]

    json_data = '{"people": [{"name": "Bre", "age": 25}, {"name": "Stephane", "age": 30}]}'
    xpath = 'people/name'
    assert json_xpath(json_data, xpath) == [['Bre', 'Stephane']]

    json_data = '{"people": {"name": "Bre", "age": 25}}'
    xpath = 'people/name'
    assert json_xpath(json_data, xpath) == ['Bre']

    # Test case 2: * query
    json_data = '{"people": [{"name": "Bre", "age": 25}, {"name": "Stephane", "age": 30}]}'
    xpath = 'people/*'
    assert json_xpath(json_data, xpath) == [[{"name": "Bre", "age": 25}, {"name": "Stephane", "age": 30}]]


    # Test case 3: index query
    json_data = '[{"people": [{"name": "Bre", "age": 25}, {"name": "Stephane", "age": 30}]}, {"people": [{"name": "Alice1", "age": 26}, {"name": "Stephane1", "age": 31}]}]'
    xpath = 'people#0/name'
    assert json_xpath(json_data, xpath) == ['Bre', 'Stephane']

    xpath = 'people#1/name#1'
    assert json_xpath(json_data, xpath) == 'Stephane1'

    # to get the first one you need to use #0, can't omit
    json_data = '{"people": [{"name": "Bre", "age": 25}, {"name": "Stephane", "age": 30}]}'
    xpath = 'people#0/name#1'
    assert json_xpath(json_data, xpath) == 'Stephane'


    # Test case 4: Function query
    json_data = '{"numbers": [1, 2, 3, 4, 5]}'
    xpath = 'max(numbers)'
    assert json_xpath(json_data, xpath) == [5]


    json_data = '[{"numbers": [1, 2, 3, 4, 5]}, {"numbers": [7, 8, 9, 10, 11]}] '
    xpath = 'min(numbers)'
    assert json_xpath(json_data, xpath) == [1, 7]


    # Test case 5: Filter query
    json_data = '{"people": [{"name": "Bre", "age": 25}, {"name": "Stephane", "age": 30}, {"name": "Nor", "age": 31}]}'
    xpath = 'people[name==Stephane]'
    assert json_xpath(json_data, xpath) == [[{'name': 'Stephane', 'age': 30}]]

    xpath = 'people[age==30]'
    assert json_xpath(json_data, xpath) ==  [[{'name': 'Stephane', 'age': 30}]]

    xpath = 'people[age!=25]'
    assert json_xpath(json_data, xpath) == [[{'name': 'Stephane', 'age': 30}, {'name': 'Nor', 'age': 31}]]

    xpath = 'people[age>25]'
    assert json_xpath(json_data, xpath) == [[{'name': 'Stephane', 'age': 30}, {'name': 'Nor', 'age': 31}]]

    json_data = '[{"people": [{"name": "Bre", "age": 25}, {"name": "Stephane", "age": 30}]}, {"people": [{"name": "Bre1", "age": 26}, {"name": "Stephane1", "age": 30}]}]'
    xpath = 'people[age>25]'
    assert json_xpath(json_data, xpath) == [[{'name': 'Stephane', 'age': 30}], [{'name': 'Bre1', 'age': 26}, {'name': 'Stephane1', 'age': 30}]]

    xpath = 'people[age!=30]'
    assert json_xpath(json_data, xpath) == [[{'name': 'Bre', 'age': 25}], [{'name': 'Bre1', 'age': 26}]]

    xpath = 'people[name != ZH]'
    assert json_xpath(json_data, xpath) == [[{'name': 'Bre', 'age': 25}, {'name': 'Stephane', 'age': 30}], [{'name': 'Bre1', 'age': 26}, {'name': 'Stephane1', 'age': 30}]]

    # Test case 6: Range query
    #currently not support syntax like people#0:2/name#1:2, the range must apply on the last token
    json_data = '{"people": [{"name": "Bre", "age": 25}, {"name": "Stephane", "age": 30}, {"name": "Nor", "age": 35}]}'
    xpath = 'people#0/name#1:3'
    assert json_xpath(json_data, xpath) == ['Stephane', 'Nor']

    json_data = '[{"people": [{"name": "Bre", "age": 25}, {"name": "Stephane", "age": 30}]}, {"people": [{"name": "Bre1", "age": 26}, {"name": "Stephane1", "age": 31}]}]'
    xpath = 'people#0:2'
    assert json_xpath(json_data, xpath) == [[{'name': 'Bre', 'age': 25}, {'name': 'Stephane', 'age': 30}], [{'name': 'Bre1', 'age': 26}, {'name': 'Stephane1', 'age': 31}]]

    json_data = '[{"people": [{"name": "Bre", "age": 25}, {"name": "Stephane", "age": 30}]}, {"people": [{"name": "Bre1", "age": 26}, {"name": "Stephane1", "age": 31}]}]'
    xpath = 'people#1/name#1:2'
    assert json_xpath(json_data, xpath) == ['Stephane1']

    # Test case 7: Error handling - invalid JSON
    json_data = '{name: "Bre", age: 25}'
    xpath = 'name'
    try:
        json_xpath(json_data, xpath)
    except ValueError as e:
        assert str(e) == "Invalid JSON"

if __name__ == '__main__':
    main()


