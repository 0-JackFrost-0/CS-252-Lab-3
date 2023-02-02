from hamming_code import *
received_data = ['111', '100', '110', '110', '000', '100', '000', '001', '111', '000', '000', '000', '001', '000']
rec_data = ''
for strn in received_data:
    rec_data = rec_data + strn
print(rec_data)
packets = [rec_data[21*i:21*i+21] for i in range(len(rec_data)//21)]
print(packets)
packets_ = []
for i in range(len(packets)):
    packets_.append([int(char) for char in packets[i]])
print(packets_)
out = get_output(packets)
print(f"Message received is: {out}")