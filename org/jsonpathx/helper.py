import json
import re
import ply_paser.parser

def index_helper(data, index, res):
    for dd in data:
        if not isinstance(dd, list):
            res.append(data[index])
            break
        else:
            index_helper(dd, index, res)


def range_helper(data, start, end, res):
    for dd in data:
        if not isinstance(dd, list):
            res.append(data[start: end])
            break
        else:
            range_helper(dd, start, end, res)


def filter_helper(data, key, value, op, res):
    if not isinstance(data, dict):
        for dd in data:
            filter_helper(dd, key, value, op, res)
    else:
        if op == '==':
            if data.get(key, None) == value:
                res.append([data])
        elif op == '!=':
            if data.get(key, None) != value:
                res.append([data])
        elif op == '<':
            if data.get(key, None) < value:
                res.append([data])
        elif op == '>':
            if data.get(key, None) > value:
                res.append([data])
        elif op == '<=':
            if data.get(key, None) <= value:
                res.append([data])
        elif op == '>=':
            if data.get(key, None) >= value:
                res.append([data])
        elif op == ' HAS ':
            if value in data.get(key, None):
                res.append([data])
        elif op == ' NOTHAS ':
            if value not in data.get(key, None):
                res.append([data])


def recursive_descent_helper(key, data, res):
    if isinstance(data, list):
        for dd in data:
            recursive_descent_helper(key, dd, res)

    if isinstance(data, dict):
        for k, value in data.items():
            if k == key:
                res.append(value)
            else:
                recursive_descent_helper(key, data.get(k), res)


def json_xpath(data, xpath):
    if "(" in xpath and ")" in xpath:
        func_name, arg_expr = xpath.split("(")
        arg_expr = arg_expr[:-1]
        values = json_xpath(data, arg_expr.strip())

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
        if len(data) > 0:
            return data
        return None

    tokens = re.split("[/]", xpath)

    for token in tokens:
        if token == "*":
            # data = [v for k, v in data.items()] if isinstance(data, dict) else data
            data = data

        elif "#" in token:

            path, index = token.split("#")
            if not path:
                if ":" not in token:
                    index = int(index)
                    global result
                    res = []
                    index_helper(data, index, res)
                    data = res
                else:
                    if not isinstance(data, list):
                        raise TypeError("range operator must work on lists")
                    start, end = index.split(":")
                    start = int(start) if start else 0
                    end = int(end) if end else len(data)
                    res = []
                    range_helper(data, start, end, res)
                    data = res

                continue

            getByKey = json_xpath(data, path.strip())
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

        elif ".." in token:
            key = token[2:]
            res = []
            recursive_descent_helper(key, data, res)
            data = res


        elif "[" in token and "]" in token:

            path, remain = token.split("[")
            filter_expr = remain[:-1]
            if path:
                withoutFilter = json_xpath(data, path.strip())
            else:
                withoutFilter = data
            filter_match = re.match(r'(.+)(==|!=|<|>|<=|>=| HAS | NOTHAS )(.+)', filter_expr)
            if filter_match:
                key = filter_match.group(1)
                op = filter_match.group(2)
                value = filter_match.group(3)

                if value.isdigit():
                    value = int(value)
                res = []
                filter_helper(withoutFilter, key, value, op, res)
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
                if (isinstance(dd, list)):
                    res.append([d.get(token, None) for d in dd if isinstance(d, dict)])
                else:
                    res.extend([dd.get(token, None) if isinstance(dd, dict) else None])
            data = res

        if data is None:
            break
    
    if len(data) > 0:
        return data
    return None


def visualize(json_data):
    return json_data

def convert(source, query):
    result = None
    former_lhs = None
    assert type(query) == tuple or query == '$' or query == '*'
    if query == '$':
        return source
    elif query == '*':
        return 
    
    rel = query[0]
    lhs = query[1]
    if type(lhs) == tuple:
            lhs = convert(source, lhs)
    elif lhs == '$' or '@':
            former_lhs = lhs
            lhs = source
    rhs = trans(lhs, query[2])
    try:
        if rel == 'c' and former_lhs != '@':            
            if type(rhs) == str:
                if rhs == '*':
                    result = lhs
                else:
                    result = lhs[rhs]
            elif type(rhs) == list:
                result = [lhs[i] for i in rhs]
            elif type(rhs) == int:
                result = lhs[rhs]
                
            
        elif rel == '=':
            result = lhs.index(rhs)

        elif rel == '!':
            result = [index for index, value in enumerate(lhs) if value != rhs]
        
        elif rel == '<':
            result = [index for index, value in enumerate(lhs) if value < rhs]

        elif rel == 'l':
            result = [index for index, value in enumerate(lhs) if value <= rhs]

        elif rel == '>':
            result = [index for index, value in enumerate(lhs) if value > rhs]

        elif rel == 'g':
            result = [index for index, value in enumerate(lhs) if value >= rhs]

        elif rel == 's' or former_lhs == '@':
            result = [item[rhs] for item in lhs]
        
        else:
            print("Error")

        return result
    except Exception as e:
        print(e)
        return "Error occurs"

def trans(lhs, rhs):
    if type(rhs) == tuple:
        if rhs[0] == ':':
            assert type(rhs[1]) == int
            assert type(rhs[2]) == int
            assert rhs[2] > rhs[1]
            return list(range(rhs[1], rhs[2], 1))
        else:
            return convert(lhs, rhs)
    elif type(rhs) == list:
        return rhs
    elif type(rhs) == str:
        return rhs
    elif type(rhs) == int:
        return rhs
    else:
        print("Error: %s" % rhs)
        return


def jsonx_path_lalr(source, query):
    parser = parser.JsonPathXParser()
    parser.build()
    res = parser.parser.parse(query)
    return convert(source, res)