from django.shortcuts import render, redirect
from .models import CalculateInfo
# Create your views here.


def calculator(request):
    print(request.POST, request.method)
    if len(request.POST) == 0:
        stack = [0]
        info = CalculateInfo(stack, 0, True)
        return get_response(request, info)

    if 'button' not in request.POST or 'output' not in request.POST or 'stack' not in request.POST or 'entering' not in request.POST:
        info = CalculateInfo([], 0, True, "Missing parameters")
        return get_response(request, info)

    button = request.POST['button']
    output = request.POST['output']
    try:
        output = int(output)
    except Exception as e:
        print(e)
        info = CalculateInfo([], 0, True, "Invalid parameters")
        return get_response(request, info)

    if request.POST['entering'] == 'True' or request.POST['entering'] == 'False':
        entering = False if request.POST['entering'] == 'False' else True
    else:
        info = CalculateInfo([], 0, True, "Invalid parameters")
        return get_response(request, info)

    stack = []
    for i in request.POST['stack'].split(','):
        try:
            stack.append(int(i))
        except Exception as e:
            print(e)
            info = CalculateInfo([], 0, True, "Invalid parameters")
            return get_response(request, info)

    if len(stack) > 3:
        info = CalculateInfo([], 0, True, "Invalid parameters")
        return get_response(request, info)

    info = CalculateInfo(stack, output, entering)
    value = get_btn_value(button)
    if value == "plus":
        plus(info)
    elif value == "minus":
        minus(info)
    elif value == "times":
        times(info)
    elif value == "divide":
        divide(info)
    elif value == "push":
        push(info)
        info.op = 'push'
    elif value in list(range(10)):
        input_num(info, value)
        info.op = 'num'
    else:
        info.errmsg = "Invalid parameters"

    return get_response(request, info)


def get_response(request, info: CalculateInfo):
    if info.errmsg is not None and len(info.errmsg) > 0:
        return render(request, 'error.html', {"errmsg": info.errmsg})
    else:
        print(info.to_dict())
        return render(request, 'calculator.html', info.to_dict())


def get_btn_value(button):
    try:
        return int(button)
    except:
        return button


def input_num(info: CalculateInfo, btn_value: int):
    stack = info.stack
    print("input", info.to_dict(), btn_value)
    if info.entering:
        curr = stack.pop()
        if curr == 0:
            curr = btn_value
        else:
            curr = curr * 10 + btn_value

        info.output = curr
        stack.append(curr)
    else:
        stack.append(btn_value)
        info.entering = True
        info.output = btn_value


def push(info: CalculateInfo):
    if len(info.stack) == 3:
        info.errmsg = "Stack overflow"
    else:
        info.stack.append(0)
        info.output = 0


def plus(info: CalculateInfo):
    if len(info.stack) < 2:
        info.errmsg = "Stack underflow"
    else:
        info.output = info.stack[-2] + info.stack[-1]
        info.save_output()


def minus(info: CalculateInfo):
    if len(info.stack) < 2:
        info.errmsg = "Stack underflow"
    else:
        info.output = info.stack[-2] - info.stack[-1]
        info.save_output()


def times(info: CalculateInfo):
    if len(info.stack) < 2:
        info.errmsg = "Stack underflow"
    else:
        info.output = info.stack[-2] * info.stack[-1]
        info.save_output()


def divide(info: CalculateInfo):
    if len(info.stack) < 2:
        info.errmsg = "Stack underflow"
    else:
        x = info.stack[-2]
        y = info.stack[-1]
        if y == 0:
            info.errmsg = "Divide by zero"
        else:
            info.output = x // y
            info.save_output()
