"""Train a lightweight cost-sensitive EcoSafe routing baseline."""
import argparse
import json
import pickle

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_predict


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--csv', required=True)
    p.add_argument('--features', nargs='+', required=True)
    p.add_argument('--target', default='oracle_escalate')
    p.add_argument('--out', required=True)
    p.add_argument('--fn-weight', type=float, default=3.0)
    a = p.parse_args()

    d = pd.read_csv(a.csv).dropna(subset=a.features + [a.target])
    X = d[a.features].to_numpy()
    y = d[a.target].astype(int).to_numpy()
    if len(set(y)) < 2:
        raise SystemExit('Router target needs both escalation classes')

    model = LogisticRegression(max_iter=2000, class_weight={0: 1.0, 1: a.fn_weight})
    cv = StratifiedKFold(5, shuffle=True, random_state=20260927)
    prob = cross_val_predict(model, X, y, cv=cv, method='predict_proba')[:, 1]
    pred = (prob >= 0.5).astype(int)
    report = {
        'auc': float(roc_auc_score(y, prob)),
        'classification_report': classification_report(y, pred, output_dict=True),
        'features': a.features,
        'fn_weight': a.fn_weight,
    }
    model.fit(X, y)
    with open(a.out, 'wb') as f:
        pickle.dump({'model': model, 'features': a.features, 'report': report}, f)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
