# _*_ coding: utf-8 _*_
# @Time : 2023/8/6 9:06
# @Author : Michael
# @File : multiply_movie.py
# @desc :
import random
import time
import turtle
import gc


def write(pen, s, x, y, font_size=16, color='black'):
    pen.penup()
    pen.goto(x, y)
    pen.pendown()
    pen.pencolor(color)
    pen.write(str(s), font=("Arial", font_size, "normal"))


def draw_line(pen, x1, y1, x2, y2, color='black', w=3):
    pen.pencolor(color)
    pen.penup()
    pen.goto(x1, y1)
    pen.width(w)
    pen.pendown()
    pen.goto(x2, y2)


class bit():
    def __init__(self, pen, n, x, y, w, h, font_size=16):
        self.pen = pen
        self.n = n
        self.x = x
        self.y = y
        self.mid_x = x + font_size / 2
        self.up_y = y + 2 * font_size
        self.down_y = y - font_size / 2
        self.font_size = font_size

    def draw(self):
        write(self.pen, self.n, self.x, self.y, self.font_size)


class number():
    def __init__(self, pen, num, width, height, x0, y0, font_size, first_num=False):
        self.num = num
        self.num_str = str(num)
        self.pen = pen
        self.width = width
        self.height = height
        self.x0 = x0
        self.y0 = y0
        self.first_num = first_num
        self.bits = [bit(self.pen, int(n), self.x0 - (len(self.num_str) - i) * self.width,
                         self.y0 + int(self.first_num) * self.height, self.width, self.height, font_size) for i, n in
                     enumerate(self.num_str)]
        self.cur_bit = len(self.num_str) - 1

    def draw(self):
        for i in range(len(self.bits)):
            self.bits[i].draw()


def show_multiple(num1, num2, width, height, x0=0, y0=0, font_size=30):
    pen = turtle.Turtle()
    turtle.screensize(1800, 1500)
    pen.hideturtle()
    pen.width(8)
    write(pen, '任意两个整数乘法计算演示\n\t\tby Michael阿明', x0 - 4 * width, y0 + 2 * height, font_size, color='blue')
    number1 = number(pen, num1, width, height, x0, y0, font_size, first_num=True)
    number2 = number(pen, num2, width, height, x0, y0, font_size)
    number1.draw()
    carry_height = number2.bits[0].y
    write(pen, 'x', number2.bits[0].x - width, carry_height, font_size)
    number2.draw()
    draw_line(pen, number2.bits[0].x - 4 * width, carry_height - height, number2.bits[-1].x + width,
              carry_height - height)
    carry = 0
    carry_info = [0, 0, 0, 0, '']
    sum_str = []
    h_offset = 2
    last_x, last_y = 0, 0
    for j, num2_bit in enumerate(number2.bits[::-1]):
        sum_str.append(str(num2_bit.n * num1) + '*' * j)
        for i, num1_bit in enumerate(number1.bits[::-1]):
            cross_line = [num2_bit.mid_x, num2_bit.up_y, num1_bit.mid_x, num1_bit.down_y]
            pen.speed(1)
            draw_line(pen, cross_line[0], cross_line[1], cross_line[2], cross_line[3], color='red')

            total = num1_bit.n * num2_bit.n + carry
            c, mod = divmod(total, 10)

            # 提示乘法
            msg1 = f'乘法:{num2_bit.n} x {num1_bit.n} = {num1_bit.n * num2_bit.n}'
            write(pen, msg1, x0, y0, font_size, color='red')
            # 提示进位
            if carry:
                if total // 10:
                    msg2 = f'{num1_bit.n * num2_bit.n} + 进位{carry} = {total}\n写下个位 {total % 10}\n进位{total // 10}'
                else:
                    msg2 = f'{num1_bit.n * num2_bit.n} + 进位{carry} = {total}\n写下个位 {total % 10}\n没有进位'
                write(pen, msg2, x0, y0 - 2 * height, font_size, color='red')

            # 写个位
            last_x, last_y = num2_bit.x - i * width, num2_bit.y - (h_offset + j) * height
            write(pen, mod, last_x, last_y, font_size)

            if carry:
                carry_info = [carry, last_x, carry_height - height, font_size // 2]
                write(pen, carry_info[0], carry_info[1], carry_info[2], carry_info[3], color='white')

            time.sleep(1)
            # 提示消失
            write(pen, msg1, x0, y0, font_size, color='white')
            if carry:
                write(pen, msg2, x0, y0 - 2 * height, font_size, color='white')

            carry = c

            if carry:
                last_x -= width
                carry_info = [carry, last_x, carry_height - height, font_size // 2]
                write(pen, carry, last_x, carry_height - height, font_size // 2, color='red')
            pen.speed(1)
            draw_line(pen, cross_line[0], cross_line[1], cross_line[2], cross_line[3], color='white')
        if carry:
            last_x = num2_bit.x - len(number1.bits) * width
            last_y = num2_bit.y - (h_offset + j) * height
            write(pen, carry, last_x, last_y, font_size)
            carry = 0
            write(pen, carry_info[0], carry_info[1], carry_info[2], carry_info[3], color='white')
            carry_info[0] = 0
    write(pen, '+', last_x - 2 * width, last_y, font_size)  # 写一个 + 号

    offset = len(number2.bits) + 2
    cur_height = carry_height - offset * height
    draw_line(pen, number2.bits[0].x - 4 * width, cur_height, number2.bits[-1].x + width, cur_height)

    max_len = max([len(s) for s in sum_str])
    sum_str = [x if len(x) == max_len else (max_len - len(x)) * '*' + x for x in sum_str]
    print(sum_str)
    carry = 0
    final_sum = ''
    last_x = 0
    turtle.speed(1)
    for i in reversed(range(max_len)):
        bits = [int(x[i]) for x in sum_str if x[i] != '*']
        if carry:
            write(pen, carry_info[0], carry_info[1], carry_info[2], carry_info[3], color='white')
        c, mod = divmod(sum(bits) + carry, 10)

        # 提示
        if carry:
            msg1 = f'竖式加法:{"+".join(str(x) for x in bits)}+进位{carry} = {sum(bits) + carry}'
        else:
            msg1 = f'竖式加法:{"+".join(str(x) for x in bits)} = {sum(bits)}'
        write(pen, msg1, x0, cur_height, font_size, color='red')

        final_sum = str(mod) + final_sum
        last_x = number2.bits[-1].x - (max_len - i - 1) * width
        write(pen, mod, last_x, cur_height - height, font_size)

        time.sleep(1)
        carry = c
        # 提示消失
        write(pen, msg1, x0, cur_height, font_size, color='white')

        if carry:
            carry_info = [carry, last_x - width, cur_height, font_size // 2]
            write(pen, carry, last_x - width, cur_height, font_size // 2, color='red')
    if carry:
        final_sum = str(carry) + final_sum
        write(pen, carry, last_x - width, cur_height - height, font_size)
        write(pen, carry_info[0], carry_info[1], carry_info[2], carry_info[3], color='white')
    print(int(final_sum))
    assert int(final_sum) == num1 * num2
    write(pen, '演示结束，你学会了吗？', x0, cur_height, font_size, color='blue')
    del pen
    gc.collect()
    turtle.done()


if __name__ == '__main__':
    # 产生随机数
    num1 = random.randint(2, 1000)
    num2 = random.randint(2, 1000)
    # num1, num2 = 999, 234
    start_time = time.time()
    pen = turtle.Turtle()
    turtle.screensize(1920, 1080)
    show_multiple(pen, num1, num2, 100, 100, 30, 100)
    end_time = time.time()
    print(f'一共花费时间：{end_time - start_time:.1f}秒')
    turtle.done()
