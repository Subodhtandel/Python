b="python"
try:
    assert a =="hello"
except AssertionError:
    print("error in assertion")
except:
    print("somting else")