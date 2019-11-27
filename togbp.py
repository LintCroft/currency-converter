import os
import argparse
import requests

url = "https://api.exchangeratesapi.io/latest"
parser = argparse.ArgumentParser("Convert to GBP")
parser.add_argument("-i", "--input-amount", help="Amount to be converted to GBP", type=float)
parser.add_argument("-c", "--currency", help="Currency (defaults is PHP)", type=str.upper, default="PHP")
parser.add_argument("-r", "--show-refs", help="Display currency refs", action="store_true")
args = parser.parse_args()
rateFilename = args.currency+"_rate.txt"

def getCurrencyRef():
    reqJson = requests.get(url = url).json()
    try:
        ratesJson = reqJson["rates"]
        print("Supported currencies:")
        for key in sorted (ratesJson):
            print(key)
    except Exception:
        print(reqJson["Error"])
        exit()

def saveGbp(rate):
    f = open(rateFilename, "w")
    f.write(str(rate))
    f.close()

def readStoredGbp():
    if os.path.exists(rateFilename):
        try:
            f = open(rateFilename, "r")
            return float(f.readline())
        except IOError:
            print("Unable to read file")
            exit()
    else:
        print("Unable to find '{}'".format(rateFilename))
        exit() 

def runConversion():
    params = {"symbols":"GBP", "base":"{}".format(args.currency)}
    print("Fetching exchange rate for {}..".format(args.currency))
    gbpRate = ""
    reqJson = dict()
    try:
        reqJson = requests.get(url = url, params = params).json()
        gbpRate = reqJson["rates"]["GBP"]
        saveGbp(gbpRate)
    except Exception:
        if ("error" in reqJson.keys()):
            print(reqJson["error"])
        print("Error occurred whilst fetching exchange rate. Using locally stored {} to GBP rate..".format(args.currency))
        gbpRate = readStoredGbp()

    print("{} to GBP rate is £{}".format(args.currency, str(round(gbpRate, 2))))
    inputAmount = args.input_amount
    if not inputAmount:
        inputAmount = float(input("How much {} to convert to GBP?\n".format(args.currency)))
    print(str(round(inputAmount, 2)) + " " + args.currency + " is £" + str(round(gbpRate*inputAmount, 2)))

if (args.show_refs):
    getCurrencyRef();
else:
    runConversion()
input("Press enter..")
