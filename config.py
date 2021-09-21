api_keys_config = {
    "DATA_REPORT_API" : {
        "expiration_in_days": "1",
        "roles": [
            {
                "index": ["asset-*"],
                "privileges": ["read", "write"],
            },
            {
                "index": ["test*"],
                "privileges": ["read", "write"],
            }
        ],
    },
    "CORGIS_UI" : {
        "expiration_in_days": 1,
        "roles": [{
            "index": ["asset_dev"],
            "previlages": ["read", "write"],
        }],
    }    
}