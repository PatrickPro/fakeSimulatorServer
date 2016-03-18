import os
import datetime
import pytz



for files in os.listdir("logs"):
    if not files.split("_")[0] in [".DS", "Done"]:
        print files + "  " + str(len(files.split("_")))
        print
        naive_date = datetime.datetime.fromtimestamp(int(files.split("_")[5])/1000).strftime('%Y-%m-%d %H:%M:%S')
        dt = naive_date
        unaware_est = datetime.datetime.strptime(dt,"%Y-%m-%d %H:%M:%S")
        localtz = pytz.timezone('Australia/Brisbane')
        aware_est = localtz.localize(unaware_est)
        if int(len(files.split("_"))) >= 7:
            newFileName = files.split("_")[1] + "_" + str(aware_est.strftime('%Y-%m-%d_%H.%M.%S')) + "_" + files.split("_")[6] + "_" + files.split("_")[7]
        else:
            newFileName = files.split("_")[1] + "_" + str(aware_est.strftime('%Y-%m-%d_%H.%M.%S'))
        os.rename(os.path.dirname(os.path.abspath(files))+"/logs/Done/"+files, os.path.dirname(os.path.abspath(files))+"/logs/"+newFileName+ ".csv")
        print "renamed " + files +" to " +newFileName