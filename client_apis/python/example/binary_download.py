import sys
import struct
import socket
import pprint
import optparse 

# in the github repo, cbapi is not in the example directory
sys.path.append('../src/cbapi')

import cbapi 

def build_cli_parser():
    parser = optparse.OptionParser(usage="%prog [options]", description="Download a binary")

    # for each supported output type, add an option
    #
    parser.add_option("-c", "--cburl", action="store", default=None, dest="url",
                      help="CB server's URL.  e.g., http://127.0.0.1 ")
    parser.add_option("-a", "--apitoken", action="store", default=None, dest="token",
                      help="API Token for Carbon Black server")
    parser.add_option("-n", "--no-ssl-verify", action="store_false", default=True, dest="ssl_verify",
                      help="Do not verify server SSL certificate.")
    parser.add_option("-m", "--md5", action="store", default=None, dest="md5",
                      help="binary query")
    parser.add_option("-f", "--filename", action="store", default=None, dest="filename",
                      help="local filename to save the binary as")
    return parser

def main(argv):
    parser = build_cli_parser()
    opts, args = parser.parse_args(argv)
    if not opts.url or not opts.token or opts.md5 is None:
        print "Missing required param; run with --help for usage"
        sys.exit(-1)

    if opts.filename is None:
        opts.filename = "%s.zip" % (opts.md5,)

    # build a cbapi object
    #
    cb = cbapi.CbApi(opts.url, token=opts.token, ssl_verify=opts.ssl_verify)

    # perform a single binary search
    #
    binary = cb.binary(opts.md5)
    
    # open the file and write out the contents
    #
    open(opts.filename, "w").write(binary)

    print "-> Downloaded binary %s [%u bytes]" % (opts.md5, len(binary))

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
