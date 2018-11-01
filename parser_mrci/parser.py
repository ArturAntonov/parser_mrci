class Parser(object):

    def __init__(self, ticker_names, target_columns, table_columns) -> None:
        self._ticker_names = ticker_names
        self._target_columns = target_columns
        self._table_columns = table_columns

    def run(self):
        # Parse years data for root
        # years_html_paths = get_years_htmls(ohlc_page)
        # request_days_htmls(years_html_paths)

        # failed = []
        # #Parse days htmls and write csv
        # for year_html in get_years_htmls(ohlc_page):
        #     for day_html in get_days_htmls(year_html):
        #         _, failed_day = process_day_html(day_html)
        #         if len(failed):
        #             failed.append(failed_day)
        #     print 'year process COMPLETE'
        # print 'all day process COMPLETE'
        # print 'FAILED', failed
        pass
