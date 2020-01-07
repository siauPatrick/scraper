from scraper.spiders import fifa


def execute(args):
    fifa.execute(args.outfile, args.format)
