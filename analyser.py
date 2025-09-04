from ast import expr
import re

def find_matching_parentheses(expr, start):
    count = 1
    i = start + 1
    while i < len(expr) and count > 0:
        if expr[i] == '(':
            count += 1
        elif expr[i] == ')':
            count -= 1
        i += 1
    return i - 1

def split_arguments(arg_str):
    args = []
    current = ""
    paren_count = 0
    
    for char in arg_str:
        if char == '(':
            paren_count += 1
            current += char
        elif char == ')':
            paren_count -= 1
            current += char
        elif char == ',' and paren_count == 0:
            args.append(current.strip())
            current = ""
        else:
            current += char
    
    if current:
        args.append(current.strip())
    
    return args

def parse_expression(expr, functions):
    pattern = r'(f\.\w+)\('
    while True:
        match = re.search(pattern, expr)
        if not match:
            break
        func_name = match.group(1)
        start_pos = match.end()
        end_pos = find_matching_parentheses(expr, start_pos - 1)
        arg_str = expr[start_pos:end_pos]
        args = split_arguments(arg_str)
        
        if len(args) != 2:
            raise ValueError(f"函数 {func_name} 需要2个参数，但得到 {len(args)} 个")
        
        if func_name in functions:
            arg1_parsed = parse_expression(args[0], functions)
            arg2_parsed = parse_expression(args[1], functions)
            template = functions[func_name]
            replaced = template.replace('{x}', arg1_parsed).replace('{y}', arg2_parsed)
            func_call = expr[match.start():end_pos + 1]
            expr = expr.replace(func_call, replaced)
        else:
            raise ValueError(f"未知函数: {func_name}")
    
    return expr

def analyse(expr,functions):
        result = parse_expression(expr, functions)
        return result
