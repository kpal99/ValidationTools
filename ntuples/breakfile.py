import sys

def breakfile(arg):
    filename = arg
    f = open(filename, "r")
    print f
    count = 0
    count_break=2
    filename_temp = filename.split('/')
    filename1 = filename_temp[1].split('.txt')
    for line in f.readlines():
        if count % count_break == 0:
            num_str = str(int(count/count_break))
            f1 = open(filename1[0] + '_' + num_str.zfill(3) + '.txt', "w")
        f1.writelines(line)
        #print line1[0]
        count += 1

if __name__ == '__main__':
    for arg in sys.argv[1:]:
        breakfile(arg)
