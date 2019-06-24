import requests
from xml.etree import ElementTree

# initial tracking ID, one of these numbers is incorrect
trackingID = "9505512251288297336033"
endIndex = len(trackingID) - 1
# start at the end
index = endIndex
# replace character at index with 0
replacement = 0
while replacement < 10:
    # replace the character
    temp = trackingID[:index] + str(replacement)
    # add trailing characters if any
    if index < endIndex:
        temp += trackingID[index +  1:]
    replacement += 1
    request = "http://production.shippingapis.com/ShippingAPI.dll ?API=TrackV2&XML=<TrackRequest USERID=\"014TEST06326\"><TrackID ID=\"" + temp + "\"></TrackID></TrackRequest>"
    print("Request to " + temp)
    result = requests.get(request)
    # parse result into a tree
    tree = ElementTree.fromstring(result.content)
    response = tree.tag
    # find the tracking info 
    trackinfo = tree.find("TrackInfo")
    error = trackinfo.find("Error")
    summ = trackinfo.find("TrackSummary")
    if summ is not None:
        summaryText = summ.text
    # We found a possible match?
    if error is None and summaryText != "The Postal Service could not locate the tracking information for your request. Please verify your tracking number and try again later.":
        print(response)
        print(trackinfo.tag + " : " + trackinfo.get("ID"))
        break
    # we're at the end, decrement index and keep trying
    if replacement == 10:
        replacement = 0        
        index -= 1

        


