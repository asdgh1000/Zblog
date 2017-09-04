
def get_pagintor(args):
    pagintor = {
        "page": args.get('page'),
        "page_size": args.get('page_size')
    }
    return pagintor