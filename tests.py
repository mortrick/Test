testint = 22 # Int
testintb = 21000000 # Int
testintc = 109699439.5615 # float
testfloat = 22.22 # float
teststring = 'asdasdasd'
testlist = ['mineable']
testtime = "2020-02-14T18:30:36.000Z"
strange = 3.279999737232541e-05



# print(teststring.index(":"))
# print(str(strange)[:7])
# print(type(strange))

# def setobj(obj):
#     if type(obj) == int:
#         return str(obj)
#     if type(obj) == float:
#         if len(str(obj)) >= 10:
#             return str(obj)[:8]
#         else:
#             return str(obj)
#     if type(obj) == str:
#         if "T" in obj and ":" in obj:
#             newobj = obj.replace("T", " ")
#             newobjstr = str(newobj)[:19]
#             return "'" + newobjstr + "'"
#         else:
#             return str("'" + obj + "'")
#     if type(obj) == list:
#         if obj == []:
#             return 'null'
#         newobj = obj[0]
#         return "'" + newobj +"'"




def setobj(obj):
    if not obj:
        return str('null')
    if obj == 'None':
        return str('null')
    elif type(obj) == int:
        return str(obj)
    elif type(obj) == float:
        if len(str(obj)) >= 12:
            newstr = str(obj)[:12]
            if newstr[-1] == ".":
                newstr.replace(".", "")
                return str(newstr)
            else:
                return str(newstr)
        elif str(obj)[-1] == ".":
            newobj = obj.replace(".", "")
            return newobj
        else:
            return str(obj)
    elif type(obj) == str:
        if "T" in obj and ":" in obj:
            newobj = obj.replace("T", " ")
            newobjstr = str(newobj)[:19]
            return str("'" + newobjstr + "'")
        elif str(obj)[-1]==".":
            newobj = obj.replace(".", "")
            return newobj
        else:
            return str("'" + obj + "'")
    elif type(obj) == list:
        if obj == []:
            return str('null')
        newobj = obj[0]
        return str("'" + newobj +"'")
    else:
        return str(obj)





def test(n):
    a = n%5
    print(a)
    return a



def to_bin(n):
    if n == None:
        return None
    bits=[]
    while (n>0):
        a = int(float(n%2))
        bits.append(a)
        n=(n-a)/2
        st='';
        if not bits:
            st = '0'
        for j in reversed(bits):
            st=st+str(j)
    return st


print(to_bin(127))

# test(23)

