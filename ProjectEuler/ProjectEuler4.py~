import numpy as np;

def countDigits(num):
    digits = 0;
    if (num == 0):
        return 0;
    while(num / 10**digits):
        digits = digits + 1;
    return digits;
    
def reverse(num, digits):
    numbers = [];
    curDigit = 0;
    value = 0;
    
    while (curDigit < digits):
        numbers.append(num % 10);
        num = num / 10;
        curDigit = curDigit + 1;
    
    for number in numbers:
        value = value + number * 10**(curDigit - 1);
        curDigit = curDigit - 1;

    return value;

def isPalindrome(num):
    digits = countDigits(num);
    if (num == 0 or num == 1):
        return True;
    else:
        if (digits % 2): #num has an odd number of digits
            left = num / (10**(digits / 2 + 1));
        else:
            left = num / (10**(digits / 2));
        right = num % (10**(digits / 2));
        right = reverse(right, digits / 2);
        if (left == right):
            return True;
        else:
            return False;

def largestPalindromeProduct(min1, max1, min2, max2):
    range1 = np.arange(min1, max1 + 1)[::-1];
    range2 = np.arange(min2, max2 + 1)[::-1];
    iterations = 0;
    largest = 0;
    arg1 = 0;
    arg2 = 0;
    
    for num1 in range1:
        for num2 in range2:
            product = num1 * num2;
            if (isPalindrome(product)):
                if (product > largest):
                    largest = product;
                    arg1 = num1;
                    arg2 = num2;
            if (num2 < num2 - ((num1 + num2)/2)):
                break;
        if (num1 < num1 - ((num1 + num2)/2)):
            break;
        iterations = iterations + 1;
    
    return largest, arg1, arg2;
    

xmin = ymin = 10;
xmax = ymax = 99;
largest,num1,num2 = largestPalindromeProduct(xmin, xmax, ymin, ymax);
print "The largest palindrome product is %d = %d * %d" % (largest, num1, num2);

