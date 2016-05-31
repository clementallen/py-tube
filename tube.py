from sense_hat import SenseHat
import time, requests, config

start = time.time()
SCRIPT_DURATION = 7200 # 120 min

sense = SenseHat()
sense.clear()
sense.low_light = True

url = 'https://api.tfl.gov.uk/Line/mode/tube/Status?detail=False'
appId = config.APP_ID
apiKey = config.API_KEY
requestUrl = url + '&app_id=' + appId + '&app_key=' + apiKey

c = (255, 0, 30)
h = (255, 20, 147)
cl = (255, 255, 0)
j = (128, 128, 128)

colourGrid = [
    c, c, c, c, j,j,j,j,
    c, c, c, c, j,j,j,j,
    c, c, c, c, j,j,j,j,
    c, c, c, c, j,j,j,j,
    cl,cl,cl,cl,h,h,h,h,
    cl,cl,cl,cl,h,h,h,h,
    cl,cl,cl,cl,h,h,h,h,
    cl,cl,cl,cl,h,h,h,h,
]

def getStatusColour(status):
    if status is 10:
        return (0, 255, 0)
    elif status is 9:
        return (255, 255, 0)
    else:
        return (255, 0, 0)

def getStatusText(status):
    if status is 10:
        return 'a Good Service'
    elif status is 9:
        return 'Minor Delays'
    else:
        return 'Severe Delays'

def getStatus(lineNum, apiStatus):
    return apiStatus[lineNum]['lineStatuses'][0]['statusSeverity']

def centralLine(status):
    statusColour = getStatusColour(status)

    sense.set_pixel(0,0, statusColour)
    sense.set_pixel(1,0, statusColour)
    sense.set_pixel(2,0, statusColour)
    sense.set_pixel(3,0, statusColour)
    print('The Central line has ' + getStatusText(status))

def jubileeLine(status):
    statusColour = getStatusColour(status)

    sense.set_pixel(4,0, statusColour)
    sense.set_pixel(5,0, statusColour)
    sense.set_pixel(6,0, statusColour)
    sense.set_pixel(7,0, statusColour)
    print('The Jubilee line has ' + getStatusText(status))

def circleLine(status):
    statusColour = getStatusColour(status)

    sense.set_pixel(0,7, statusColour)
    sense.set_pixel(1,7, statusColour)
    sense.set_pixel(2,7, statusColour)
    sense.set_pixel(3,7, statusColour)
    print('The Circle line has ' + getStatusText(status))

def hammersmithLine(status):
    statusColour = getStatusColour(status)

    sense.set_pixel(4,7, statusColour)
    sense.set_pixel(5,7, statusColour)
    sense.set_pixel(6,7, statusColour)
    sense.set_pixel(7,7, statusColour)
    print('The Hammersmith line has ' + getStatusText(status))

def displayStatus():
    apiStatus = requests.get(requestUrl).json()
    centralLine(getStatus(1, apiStatus))
    jubileeLine(getStatus(5, apiStatus))
    circleLine(getStatus(4, apiStatus))
    hammersmithLine(getStatus(2, apiStatus))

sense.set_pixels(colourGrid)

try:
    while True:
        displayStatus()

        if time.time() > start + SCRIPT_DURATION:
            break

        print('\nWaiting 10 minutes before refreshing status\n')

        time.sleep(600)

finally:
    sense.clear()
