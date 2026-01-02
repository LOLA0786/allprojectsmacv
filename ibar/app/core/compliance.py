COMPLIANCE = {
    "IN": {
        "MH": {
            "max_pour_ml": 60,
            "wallet_allowed": True
        },
        "KA": {
            "wallet_allowed": False
        }
    },
    "US": {
        "CA": {
            "max_pour_ml": 45,
            "wallet_allowed": True
        },
        "TX": {
            "max_pour_ml": 50,
            "wallet_allowed": True
        }
    },
    "EU": {
        "DEFAULT": {
            "max_pour_ml": 50,
            "wallet_allowed": True
        }
    }
}

def check(country, state, ml):
    rules = COMPLIANCE.get(country, {}).get(state) \
        or COMPLIANCE.get(country, {}).get("DEFAULT")

    if not rules or not rules["wallet_allowed"]:
        raise Exception("Wallet not permitted here")

    if ml > rules["max_pour_ml"]:
        raise Exception("Pour exceeds legal limit")
