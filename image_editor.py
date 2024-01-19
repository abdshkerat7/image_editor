#################################################################
# FILE : image_editor.py
# WRITER : your_name , your_login , your_id
# EXERCISE : intro2cs ex5 2022-2023
# DESCRIPTION: A simple program that...
# STUDENTS I DISCUSSED THE EXERCISE WITH: Bugs Bunny, b_bunny.
#								 	      Daffy Duck, duck_daffy.
# WEB PAGES I USED: www.looneytunes.com/lola_bunny
# NOTES: ...
#################################################################

##############################################################################
#                                   Imports                                  #
##############################################################################
from ex5_helper import *
import ex5_helper
from typing import Optional
import math
import sys


##############################################################################
#                                  Functions                                 #
##############################################################################


def separate_channels(image: ColoredImage) -> List[SingleChannelImage]:
    new_lst = []
    k = 0
    while k < len(image[0][0]):
        i = 0
        j = 0
        lst_in = []
        lst_out = []
        while i < len(image):
            lst_in.append(image[i][j][k])
            j += 1
            if j == len(image[0]):
                j = 0
                i += 1
                lst_out.append(lst_in)
                lst_in = []
        k += 1
        new_lst.append(lst_out)
    return new_lst


def combine_channels(channels: List[SingleChannelImage]) -> ColoredImage:
    new_lst = []
    j = 0
    while j < len(channels[0]):
        i = 0
        k = 0
        lst_in = []
        lst_out = []
        while k < len(channels[0][0]):
            lst_in.append(channels[i][j][k])
            i += 1
            if i == len(channels):
                i = 0
                k += 1
                lst_out.append(lst_in)
                lst_in = []
        j += 1
        new_lst.append(lst_out)
    return new_lst


def RGB2grayscale(colored_image: ColoredImage) -> SingleChannelImage:
    new_lst = []
    for i in range(len(colored_image)):
        lst_in = []
        for j in range(len(colored_image[0])):
            x = (colored_image[i][j][0] * .299)
            y = (colored_image[i][j][1] * .587)
            z = (colored_image[i][j][2] * .114)
            sum = x + y + z
            lst_in.append(round(sum))
        new_lst.append(lst_in)
    return new_lst



def blur_kernel(size: int) -> Kernel:
    lst1 = []
    x = 1/size**2
    for i in range(size):
        lst2 = []
        for j in range(size):
            lst2.append(x)
        lst1.append(lst2)
    return lst1

def helper_sum(image, kernel, center, row, col):
    sum = 0
    for i in range(len(kernel)):
        index_row = row-center+i
        for j in range(len(kernel)):
            index_col = col-center+j
            if index_row >= 0 and index_row < len(image):
                if index_col >= 0 and index_col < len(image[0]):
                    sum += image[index_row][index_col]
                else:
                    sum += image[row][col]
            else:
                sum += image[row][col]
    x = round(sum*kernel[0][0])
    return x


def helper_kerner(image, kernel, center):
    new_lst = []
    for i in range(len(image)):
        lst_in = []
        for j in range(len(image[0])):
            x = helper_sum(image, kernel, center, i, j)
            lst_in.append(x)
        new_lst.append(lst_in)
    return new_lst


def apply_kernel(image: SingleChannelImage, kernel: Kernel) -> SingleChannelImage:
    kernel_length = len(kernel)
    center = int(kernel_length/2)
    new_lst = helper_kerner(image, kernel, center)
    return new_lst



def find_op(image, y, x):
    x1 = x
    x2 = x
    y1 = y
    y2 = y
    if x % 1 != 0:
        x1 = int(x)
        x2 = x1 + 1
    if y % 1 != 0:
        y1 = int(y)
        y2 = y1 + 1
    cell = [(y1, x1),(y2, x1),(y1, x2),(y2, x2)]#a, b, c ,d
    a = image[int(cell[0][0])][int(cell[0][1])]

    if x2 < len(image[0]):
        c = image[int(cell[2][0])][int(cell[2][1])]
        if y2 >= len(image):
            b = a
            d = c
        else:
            b = image[int(cell[1][0])][int(cell[1][1])]
            d = image[int(cell[3][0])][int(cell[3][1])]
    else:
        b = image[int(cell[1][0])][int(cell[1][1])]
        c = a
        d = b
    return a,b,c,d


def helper_bilinear(x, y, a, b, c, d):
    opreation = a *(1-x)*(1-y)+b*y*(1-x)+c*x*(1-y)+d*x*y
    return round(opreation)


def bilinear_interpolation(image: SingleChannelImage, y: float, x: float) -> int:
    a, b, c, d = find_op(image, y, x)
    x = x%1
    y = y%1
    x = helper_bilinear(x, y, a, b, c, d)
    return x


def resize(image: SingleChannelImage, new_height: int, new_width: int) -> SingleChannelImage:
    new_image = []
    row = len(image) - 1
    col = len(image[0]) - 1
    if new_width == new_height:
        for j in range(new_width):
            in_image = []
            for i in range(new_height):
                if j == 0 and i == 0:
                    in_image.append(image[0][0])
                elif (j == new_width - 1) and (i == new_height - 1):
                    in_image.append(image[row][col])
                elif j == 0 and (i == new_height - 1):
                    in_image.append(image[0][col])
                elif (j == new_width - 1) and i == 0:
                    in_image.append(image[row][0])
                else:
                    x2 = (j / (new_height - 1)) * (len(image) - 1)
                    x1 = (i / (new_width - 1)) * (len(image[0]) - 1)
                    x = bilinear_interpolation(image, x2, x1)
                    in_image.append(x)
            new_image.append(in_image)
        return new_image
    else:
        for i in range(new_height):
            in_image = []
            for j in range(new_width):
                if j == 0 and i == 0:
                    in_image.append(image[0][0])
                elif (j == new_width - 1) and (i == new_height - 1):
                    in_image.append(image[row][col])
                elif j == 0 and (i == new_height - 1):
                    in_image.append(image[row][0])
                elif (j == new_width - 1) and i == 0:
                    in_image.append(image[0][col])
                else:
                    x2 = (j / (new_height - 1)) * (len(image) - 1)
                    x1 = (i / (new_width - 1)) * (len(image[0]) - 1)
                    x = bilinear_interpolation(image, x2, x1)
                    in_image.append(x)
            new_image.append(in_image)
        return new_image



def rotate_90(image: Image, direction: str) -> Image:
    rotat_image = []
    for i in range(len(image[0])):
        lst_in = []
        for j in range(len(image)):
            lst_in.append(image[j][i])
        if direction == 'R':
            lst_in = lst_in[::-1]
        rotat_image.append(lst_in)
    if direction == 'L':
        rotat_image = rotat_image[::-1]
    return rotat_image


def avg_helper(blurred_image, row, col, r):
    sum_num = 0
    z = 0
    for i in range(row - r, row + r + 1):

        for j in range(col - r, col + r + 1):

            if i >= 0 and i < len(blurred_image):
                if j >= 0 and j < len(blurred_image[0]):
                    sum_num += blurred_image[i][j]
                    z += 1
                else:
                    sum_num += blurred_image[row][col]
                    z += 1
            else:
                sum_num += blurred_image[row][col]
                z += 1
    x = sum_num / z
    return x



def get_edges(image: SingleChannelImage, blur_size: int, block_size: int, c: float) -> SingleChannelImage:
    blur = blur_kernel(blur_size)
    blurred_image = apply_kernel(image, blur)
    r = block_size // 2
    threshold = []
    for i in range(len(blurred_image)):
        lst_in = []
        for j in range(len(blurred_image[0])):
            x = avg_helper(blurred_image, i, j, r)
            x -= c
            lst_in.append(x)
        threshold.append(lst_in)
    new_image = []
    for i in range(len(blurred_image)):
        lst_in = []
        for j in range(len(blurred_image[0])):
            if blurred_image[i][j] > threshold[i][j]:
                lst_in.append(255)
            else:
                lst_in.append(0)
        new_image.append(lst_in)
    return new_image


def quantize(image: SingleChannelImage, N: int) -> SingleChannelImage:
    new_image = []
    for i in range(len(image)):
        lst = []
        for j in range(len(image[0])):
            x = round(math.floor(image[i][j]*N/256)*(255/(N-1)))
            lst.append(x)
        new_image.append(lst)
    return new_image


def quantize_colored_image(image: ColoredImage, N: int) -> ColoredImage:
    new_image = []
    for i in range(len(image)):
        x = quantize(image[i], N)
        new_image.append(x)
    return new_image

def play(image, n):
    new_image = []
    if n == 1:
        if isinstance(image[0][0], list):
            new_image = RGB2grayscale(image)
            return new_image
        else:
            print("it is not 3d")
            return image
    if n == 2:
        kernel_size = input("please enter the kernel size: ")
        if kernel_size.isdigit():
            x = int(kernel_size)
            if x > 0 and x%2 == 1:
                kernel_lst = blur_kernel(x)
                if isinstance(image[0][0], list):
                    for i in range(len(image)):
                        new_image.append(apply_kernel(image[i], kernel_lst))
                    return new_image
                else:
                    new_image = apply_kernel(image, kernel_lst)
                    return new_image
            else:
                print("the size is not > 0 or the size%2 != 1")
                return image
        else:
            print("the size is not int")
            return image
    if n == 3:
        two_num_from_user = input("please enter two numbers and between ,").split(',')
        if len(two_num_from_user) == 2:
            x1 = two_num_from_user[0]
            x2 = two_num_from_user[1]
            if x1.isdigit() and x2.isdigit():
                if int(x1) > 1 and int(x2) > 1:
                    new_image = resize(image, int(x1), int(x2))
                    return new_image
                else:
                    print("the numbers will be > 1")
                    return image
            else:
                print("the numbers will be int")
                return image
    if n == 4:
        direction_from_user = input("please enter the direction R or L")
        if direction_from_user == 'R':
            new_image = rotate_90(image, direction_from_user)
            return new_image
        if direction_from_user == 'L':
            new_image = rotate_90(image, direction_from_user)
            return new_image
        else:
            print("the direction will be R or L")
            return image
    if n == 5:
        three_num_from_user = input("please enter three numbers and between ,").split(',')
        if len(three_num_from_user) == 3:
            blur_size = three_num_from_user[0]
            block_size = three_num_from_user[1]
            c = three_num_from_user[2]
            if blur_size.isdigit() and block_size.isdigit():
                if int(blur_size) > 0 and int(block_size) > 0:
                    if isinstance(image[0][0], list):
                        img = RGB2grayscale(image)
                        new_image = get_edges(img, int(blur_size), int(block_size), float(c))
                        return new_image
                    else:
                        new_image = get_edges(image, int(blur_size), int(block_size), float(c))
                        return new_image
                else:
                    print("the numbers will be > 0")
            else:
                print("the numbers will be int")
    if n == 6:
        quantize_num = input("please enter the quantize number: ")
        if quantize_num.isdigit():
            if int(quantize_num) > 1:
                if isinstance(image[0][0], list):
                    new_image = quantize_colored_image(image, int(quantize_num))
                    return new_image
                else:
                    new_image = quantize(image, int(quantize_num))
                    return new_image
            else:
                print("the numbers will be > 1")
        else:
            print("the numbers will be int")
    if n == 7:
        ex5_helper.show_image(image)



if __name__ == '__main__':
    lst_choose = ['1','2','3','4','5','6','7','8']
    if len(sys.argv) == 2:
        image = ex5_helper.load_image(sys.argv[1])
        input_from_user = input("choose a number from 1 to 8 that: "
                                "1: "
                                "2: "
                                "3: "
                                "4: "
                                "5: "
                                "6: "
                                "7: "
                                "8: ")
        while input_from_user not in lst_choose:
            input_from_user = input("you will choose a number from 1 to 8 that: "
                                    "1: "
                                    "2: "
                                    "3: "
                                    "4: "
                                    "5: "
                                    "6: "
                                    "7: "
                                    "8: ")
        while input_from_user != '8':
            image = play(image, int(input_from_user))
            input_from_user = input("you can choose a number from 1 to 8 that: "
                                    "1: "
                                    "2: "
                                    "3: "
                                    "4: "
                                    "5: "
                                    "6: "
                                    "7: "
                                    "8: ")
    else:
        print("error")





