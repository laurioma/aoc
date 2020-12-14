import sys
import re

pass_line = ""
pass_dict = dict()
valid = 0
with open(sys.argv[1]) as f:
    for line in f:
        if line.rstrip() == "":
            fields = pass_line.split();
            for i in range(len(fields)):
                pass_dict[fields[i][0:3]] = fields[i]
            pvalid = 1
            for key in pass_dict:
                if key == "byr":
                    res = re.search('byr:(\d{4}$)', pass_dict[key])
                    if (res):
                        byr = int(res.group(1));
                        print("byr",  res.group(1));
                        if (byr < 1920 or byr > 2002):
                            print ("BYR fail2!");
                            pvalid = 0
                            break;
                    else:
                        print ("BYR fail1!");
                        pvalid = 0
                        break;
                elif key == "iyr":
                    res = re.search('iyr:(\d{4}$)', pass_dict[key])
                    if (res):
                        iyr = int(res.group(1));
                        print("iyr",  res.group(1));
                        if (iyr < 2010 or iyr > 2020):
                            print ("iyr fail2!");
                            pvalid = 0
                            break;
                    else:
                        print ("iyr fail1!");
                        pvalid = 0
                        break;
                elif key == "eyr":
                    res = re.search('eyr:(\d{4}$)', pass_dict[key])
                    if (res):
                        eyr = int(res.group(1));
                        print("eyr",  res.group(1));
                        if (eyr < 2020 or eyr > 2030):
                            print ("eyr fail2!");
                            pvalid = 0
                            break;
                    else:
                        print ("eyr fail1!");
                        pvalid = 0
                        break;
                elif key == "hgt":
                    res = re.search('hgt:(\d+)(cm|in)$', pass_dict[key])
                    if (res):
                        hgt = int(res.group(1));
                        hgtg = res.group(2);
                        print("hgt",  res.group(1), "hgtg", hgtg);
                        if (hgtg == "cm"):
                            if (hgt < 150 or hgt > 193):
                                print ("hgt fail2!");
                                pvalid = 0
                                break;
                        else:
                            if (hgt < 59 or hgt > 76):
                                print ("hgt fail3!");
                                pvalid = 0
                                break;
                    else:
                        print ("hgt fail1!");
                        pvalid = 0
                        break;
                elif key == "hcl":
                    res = re.search('hcl:(#[0-9a-f]{6})$', pass_dict[key])
                    if (res):
                        print("hcl", res.group(1))
                    else:
                        print ("hcl fail1!", pass_dict[key])
                        pvalid = 0
                        break;
                elif key == "ecl":
                    res = re.search('ecl:(amb|blu|brn|gry|grn|hzl|oth)$', pass_dict[key])
                    if (res):
                        print("ecl:", res.group(1))
                    else:
                        print ("ecl fail1!", pass_dict[key])
                        pvalid = 0
                        break;
                elif key == "pid":
                    res = re.search('pid:(\d{9})$', pass_dict[key])
                    if (res):
                        print("pid:", res.group(1))
                    else:
                        print ("pid fail1!", pass_dict[key]);
                        pvalid = 0
                        break;
            if (len(pass_dict) == 8) or (len(pass_dict) == 7 and not "cid" in pass_dict):
                print ("FIELDS OK")
            else:
                print ("fields fail!")
                pvalid = 0
            print("Pass: ",  pass_dict, " " + fields[0][0:3], "len",  len(pass_dict), "cnt",  "cid" in pass_dict, " CHECK ",  pvalid)
            if pvalid:
                valid += 1
            
            pass_dict = dict()
            pass_line = ""
        else:
            pass_line += line.rstrip() + " "
#        numbers = re.search('()', line) 
print ("VALID ",  valid)