


def map_bls_data_with_ids():
    response = {
    "status": 200,
    "data": {
        "status": "REQUEST_SUCCEEDED",
        "responseTime": 153,
        "message": [],
        "Results": {
            "series": [
                {
                    "seriesID": "SUUR0000SA0",
                    "catalog": {
                        "series_title": "All items in U.S. city average, all urban consumers, chained, not seasonally adjusted",
                        "series_id": "SUUR0000SA0",
                        "seasonality": "Not Seasonally Adjusted",
                        "survey_name": "Chained Consumer Price Index for All Urban Consumers (C-CPI-U): U.S. city average",
                        "survey_abbreviation": "SU",
                        "measure_data_type": "All items",
                        "area": "U.S. city average",
                        "item": "All items",
                    },
                    "data": [
                        {
                            "year": "2022",
                            "period": "M12",
                            "periodName": "December",
                            "value": "165.974",
                            "footnotes": [{}],
                            "calculations": {
                                "net_changes": {},
                                "pct_changes": {
                                    "1": "-0.3",
                                    "3": "0.1",
                                    "6": "0.3",
                                    "12": "6.4",
                                },
                            },
                        },
                        {
                            "year": "2022",
                            "period": "M11",
                            "periodName": "November",
                            "value": "166.498",
                            "footnotes": [{}],
                            "calculations": {
                                "net_changes": {},
                                "pct_changes": {
                                    "1": "-0.1",
                                    "3": "0.7",
                                    "6": "1.8",
                                    "12": "7.0",
                                },
                            },
                        },
                    ],
                }
            ]
        },
    },
}

    # 1. Extract series block
    series_entry = {
        "catalog_id": response["data"]["Results"]["series"][0]["seriesID"],
        "catalog_title": response["data"]["Results"]["series"][0]["catalog"][
            "series_title"
        ],
        "seasonality": response["data"]["Results"]["series"][0]["catalog"][
            "seasonality"
        ],
        "survey_name": response["data"]["Results"]["series"][0]["catalog"][
            "survey_name"
        ],
        "measure_data_type": response["data"]["Results"]["series"][0]["catalog"][
            "measure_data_type"
        ],
        "area": response["data"]["Results"]["series"][0]["catalog"]["area"],
        "item": response["data"]["Results"]["series"][0]["catalog"]["item"],
    }

    # 2. Extract series_data block
    series_data_entries = []
    calculations_entries = []

    for idx, data_point in enumerate(response["data"]["Results"]["series"][0]["data"]):
        # Create series_data entry
        series_data_entry = {
            "series_id": idx + 1,  # Assume sequential IDs starting from 1
            "year": data_point["year"],
            "period": data_point["period"],
            "period_name": data_point["periodName"],
            "value": data_point["value"],
            "footnotes": data_point.get(
                "footnotes", [{}]
            ),  # Defaults to empty if missing
        }
        series_data_entries.append(series_data_entry)

        # Create calculations entry
        calculations_entry = {
            "series_data_id": idx + 1,  # Corresponds to series_data ID
            "pct_changes": data_point["calculations"].get("pct_changes", {}),
            "net_changes": data_point["calculations"].get("net_changes", {}),
        }
        calculations_entries.append(calculations_entry)

    # Final result: mapping into key-value pairs
    result = {
        "series": series_entry,
        "series_data": series_data_entries,
        "calculations": calculations_entries,
    }

    return result

