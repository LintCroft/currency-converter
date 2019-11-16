import argparse
import requests

parser = argparse.ArgumentParser("Convert to GBP")
parser.add_argument("inputAmount", help="Amount to be converted to GBP", type=float)
parser.add_argument("-c", "--currency", help="Currency (defaults is PHP)", type=str.upper, default="PHP")
parser.add_argument("-r", "--show-refs", help="Display currency refs", action="store_true")
args = parser.parse_args()
url = "https://api.exchangeratesapi.io/latest"

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

def runConversion():
    params = {"symbols":"GBP", "base":"{}".format(args.currency)}
    print("Fetching exchange rate for {}..".format(args.currency))
    reqJson = requests.get(url = url, params = params).json()
    try:
        print(reqJson["error"])
        exit()
    except Exception:
        pass
    gbpRate = reqJson["rates"]["GBP"]
    print("GBP to {} rate is £{}".format(args.currency, str(round(gbpRate, 2))))
    print(str(round(args.inputAmount, 2)) + " " + args.currency + " is £" + str(round(gbpRate*args.inputAmount, 2)))

if (args.show_refs):
    getCurrencyRef();
else:
    runConversion()
