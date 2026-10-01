import json

with open("scripts/large_scale_stress_test_report.json", encoding="utf-8") as f:
    d = json.load(f)

failures = [r for r in d['detailed_results'] if r['Pass/Fail'] == 'FAIL']
for i, r in enumerate(failures[:2], 1):
    print(f"#{i} [{r['Test ID']}] {r['Category']} | Reason: {r.get('Failure Reason')}")
    print(f"   Query: {r['Query']}")
    print(f"   Expected Evidence: {r.get('Expected Evidence')}")
    ans = r['Generated Answer'].replace('\n', ' ')[:140]
    print(f"   Answer: {ans}")
    print()
