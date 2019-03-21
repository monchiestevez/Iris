import os


i = 0

for filename in os.listdir():
    dst = "healthyid" + str(i) + ".png"
    dst = dst

    # rename() function will
    # rename all the files
    os.rename(filename, dst)
    i += 1
