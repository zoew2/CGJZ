import re
def ifvalid_sent_reg(raw_sen):
    pattern1 = re.compile("([\-])\\1\\1")
    pattern2 = re.compile("(.*\n){3,}")
    pattern3 = re.compile(".*\d.*\d.*\d.*\d.*\d.*\d.*\d.*\d.*\d.*\d.*\d")

    # return not (pattern1.match(raw_sen) or pattern2.match(raw_sen) or pattern3.match(raw_sen))
    return not (pattern2.match(raw_sen))

print(ifvalid_sent_reg("\ndfa\nthtr"))