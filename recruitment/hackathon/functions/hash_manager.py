import time


def check_hash(receivedHash):
    try:
        print(type(receivedHash))
        if receivedHash == "1473636383.373736-44-29":
            return 'You need to replace your_hash in the url with an actual hash - eg. 1473636383.373736-45-29'

        timeData = receivedHash.split("-")
        sum1 = timeData[1]
        sum2 = timeData[2]

        jointTime = timeData[0]
        finalHash = compute_hash(jointTime)

        hashSum1 = finalHash.split("-")[1]
        hashSum2 = finalHash.split("-")[2]

        strings = time.strftime("%Y,%m,%d,%H,%M,%S")
        t = strings.split(',')

        # if the hash sums match, check if the time of hash matches
        if sum1 == hashSum1 and sum2 == hashSum2:
            timeDifInSeconds = int(str(time.time()).split(".")[0]) - int(str(jointTime).split(".")[0])

            if timeDifInSeconds > -300 and timeDifInSeconds < 300:
                return 'success your hash worked - Please go to the HR Manager with code Z' + str(t[4]) + str(t[3]) + str(
                    t[2]) + str(t[1])
            else:
                return 'failed due to time mismatch - hash was stale - please generate a hash of a more recent time. Hash is ' + str(
                    timeDifInSeconds) + ' seconds stale'
        else:
            return "hash was incorrect"
    except:
        return "hash was invalid, please generate hash in the correct format"


def compute_hash(timeNow):
    timing = str(timeNow)
    timeData = timing.split(".")
    # print(timeData)

    sum = 0

    for x in range(0, len(str(timeData[0]))):
        sum = sum + int(timeData[0][x])
        # print(x)

    sumMil = 0
    for x in range(0, len(str(timeData[1]))):
        sumMil = sumMil + int(timeData[1][x])
        #print(x)

    #print(sum)
    #print(sumMil)

    return timing + "-" + str(sum) + "-" + str(sumMil)


