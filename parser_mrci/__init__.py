from parser_mrci.parser import Parser


def run():
    print('Parser is running')

    ticker_names = ['Brent Crude Oil(ICE)', 'Gas Oil(ICE)', 'Natural Gas(NYM)', 'Crude Oil(NYM)']
    target_columns = ['Mth', 'Date', 'Open', 'High', 'Low', 'Close']
    table_columns = ['Date', 'Open', 'High', 'Low', 'Close']

    parser = Parser(ticker_names=ticker_names,
                    target_columns=target_columns,
                    table_columns=table_columns
                    )
    parser.run()


if __name__ == '__main__':
    run()
