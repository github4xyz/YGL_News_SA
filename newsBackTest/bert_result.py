

def calcReuslt(results):
    total = 0
    for i in range(len(results)):
        temp = float((f'{results[i][0]:.8f}'))
        total += temp
    result1 = total / (i+1)
    if result1 > 0.5:
        result2 = 1
    else:
        result2 = 0
        result1 = 1 - result1
    result1 = result1 * 100
    return result1, result2 


