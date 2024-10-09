from pickle import load

with open("src\\model.pkl", "rb") as f:
    model = load(f)
    y_pred = model.predict([[329, 83, -567, -195, 50]])
    print(y_pred)