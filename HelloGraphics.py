import sys
image_width = 256;
image_height = 256;

print("P3\n%s %s\n255\n" % (image_width, image_height));
# The P3 means the colours are in ASCII
# Then dimensions are image_width by image_height large
# Max colour of 255

def print_stderr(*a):
    print(*a, file = sys.stderr, end="")

for j in range(image_height-1, -1, -1):
    print_stderr("\rScanlines remaining: %s " % j)
    sys.stderr.flush()
    for i in range(0, image_width):
        r = i/(image_width-1)
        g = j/(image_height-1)
        b = 0.25

        ir = int(255.999 * r)
        ig = int(255.999 * g)
        ib = int(255.999 * b)

        print("%s %s %s\n" % (ir, ig, ib))
print_stderr("\nDone.\n")
