import DataGather
import DataParse
import DataAnalyze
import argparse as ap


def main():
    arg_parser = ap.ArgumentParser(description='')
    arg_parser.add_argument('--mode', '-m', choices=['gather', 'parse', 'analyze', 'all'], default='all', nargs='?',
                            help='gather, or parse, or analyze data, or do all three', action="store_true")
    arg_parser.add_argument('--help', '-h', help='usage options', action=arg_parser.print_help)
    args = arg_parser.parse_args()
    mode = args.mode
    if mode == 'all':
        dg = DataGather()
        dg.run()

        dp = DataParse()
        dp.run()

        da = DataAnalyze()
        da.run()
    elif mode == 'gather':
        dg = DataGather()
        dg.run()
    elif mode == 'parse':
        dp = DataParse()
        dp.run()
    elif mode == 'analyze':
        da = DataAnalyze()
        da.run()
    print(args)

