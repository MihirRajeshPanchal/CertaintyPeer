from certaintypeer.constants.certaintypeer import estimator

def get_certainity(text):
    return estimator.predict(text)[0]