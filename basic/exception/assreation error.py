b="python"
try:
    assert a=="python3"
except AssertionError:
    print("error in assertion")
except:
    print("somting else")