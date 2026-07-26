def show(report, verdict):

    print("\nDECISION")
    print("-" * 50)

    print(f"Verdict    : {verdict['status']}")
    print(f"Grade       : {report['grade']}")
    print(f"Confidence  : {report['confidence']}%")