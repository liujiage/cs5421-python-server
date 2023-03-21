import json
import re


def helper(data, index, res):
    for dd in data:
        if not isinstance(dd, list):
            res.append(data[index])
            break
        else:
            helper(dd, index, res)


def helper(data, start, end, res):
    for dd in data:
        if not isinstance(dd, list):
            res.append(data[start: end])
            break
        else:
            helper(dd, start, end, res)


def recursive_descent(key, data, res):
    if isinstance(data, list):
        for dd in data:
            recursive_descent(key, dd, res)

    if isinstance(data, dict):
        for k, value in data.items():
            if k == key:
                res.append(value)
            else:
                recursive_descent(key, data.get(k), res)


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
                    helper(data, index, res)
                    data = res
                else:
                    if not isinstance(data, list):
                        raise TypeError("range operator must work on lists")
                    start, end = index.split(":")
                    start = int(start) if start else 0
                    end = int(end) if end else len(data)
                    res = []
                    helper(data, start, end, res)
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
            recursive_descent(key, data, res)
            data = res


        elif "[" in token and "]" in token:

            path, remain = token.split("[")
            filter_expr = remain[:-1]
            withoutFilter = json_xpath(data, path.strip())
            filter_match = re.match(r'(.+)(==|!=|<|>|<=|>=| HAS | NOTHAS )(.+)', filter_expr)
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
                    elif op == ' HAS ':
                        res.append([d for d in w if isinstance(d, dict) and value in d.get(key, None)])
                    elif op == ' NOTHAS ':
                        res.append([d for d in w if isinstance(d, dict) and value not in d.get(key, None)])
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


def visual(json_data):
    return json_data
