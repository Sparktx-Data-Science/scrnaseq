library(optparse)
library(rsconnect)

option_list <- list(
    make_option(c("-r", "--appname")),
    make_option(c("-t", "--document"))
)
opt <- parse_args(OptionParser(option_list=option_list))

appname = opt$appname

rsconnect::addConnectServer(url="https://connect.sparkds.io", name="connect", quiet=TRUE)
rsconnect::connectApiUser(account=Sys.getenv("API_USER"), server="connect", apiKey=Sys.getenv("API_KEY"))
rsconnect::deployDoc(doc=opt$document, appName=appname, account=Sys.getenv("API_USER"), server="connect", launch.browser=FALSE)
