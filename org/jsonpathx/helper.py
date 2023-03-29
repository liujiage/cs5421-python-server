import json
import re


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
        return data

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

    return data


def visualize(json_data):
    return json_data
