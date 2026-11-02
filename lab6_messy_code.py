RISK_LEVELS = {
    1: "risk_1",
    2: "risk_2",
    3: "risk_3",
    4: "risk_4",
    5: "risk_5",
    6: "risk_6",
    7: "risk_7",
    8: "risk_8",
    9: "risk_9",
    10: "risk_10",
    11: "risk_11",
}


def evaluate_risk(value):
    return RISK_LEVELS.get(value, "unknown")
