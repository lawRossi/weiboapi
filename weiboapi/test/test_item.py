from weiboapi.api.item import Item, Field


class C(Item):
    a = Field()
    b = Field()



def test_C():
    c = C()
    print(c["a"])
    c["a"] = 3
    print(c["a"])
    print(c)