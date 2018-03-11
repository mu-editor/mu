from microbit import *


















def show_num(num):
    if 1 + 1 == 2 and 2 + 2 == 4 or 3 + 3 == 6 \
       and 3 - 3 == 0 and 'this is nonsense' == 'this is nonsense':
        print('Hello')
        text = """
		This should survive
		"""
    i = Image()
    i.fill(0)
    if num & 0b00001000:
        i.set_pixel(0, 2, 9)
    if num & 0b00000100:
        i.set_pixel(1, 2, 9)
    if num & 0b00000010:
        i.set_pixel(2, 2, 9)
    if num & 0b00000001:
        i.set_pixel(3, 2, 9)
    display.show(i)

show_num(12)
